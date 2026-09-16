"""
Isolated JavaScript (Node.js) code execution -- the same design goals as
sandbox.py's Python runner (separate OS process, wall-clock timeout, no
fabricated results), re-expressed for Node. Node's built-in `vm` module gives
the user's code its own V8 context with no `require`, so it has no path to
the filesystem or network by construction, not just by convention -- a
stronger property than the Python sandbox gets, which is worth noting rather
than overclaiming: `vm` contexts are not a hard security boundary against a
determined sandbox escape (V8 bugs, prototype-chain tricks reaching the outer
realm), only a real, meaningful barrier against ordinary code.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

from app.services.execution.result_types import ExecutionResult, TestOutcome

NODE_HELPERS = r"""
function _ListNode(val, next) { this.val = val; this.next = (next === undefined ? null : next); }
function _TreeNode(val, left, right) { this.val = val; this.left = (left === undefined ? null : left); this.right = (right === undefined ? null : right); }

function _buildLinkedList(values) {
  let head = null, tail = null;
  for (const v of values) {
    const node = new _ListNode(v);
    if (head === null) { head = node; tail = node; }
    else { tail.next = node; tail = node; }
  }
  return head;
}

function _linkedListToArray(node) {
  const out = [];
  const seen = new Set();
  while (node !== null && node !== undefined && !seen.has(node)) {
    seen.add(node);
    out.push(node.val);
    node = node.next;
  }
  return out;
}

function _buildTree(values) {
  values = values.slice();
  if (values.length === 0 || values[0] === null) return null;
  let i = 0;
  const root = new _TreeNode(values[i++]);
  const queue = [root];
  while (queue.length > 0 && i < values.length) {
    const node = queue.shift();
    if (i < values.length) {
      const lv = values[i++];
      if (lv !== null && lv !== undefined) { node.left = new _TreeNode(lv); queue.push(node.left); }
    }
    if (i < values.length) {
      const rv = values[i++];
      if (rv !== null && rv !== undefined) { node.right = new _TreeNode(rv); queue.push(node.right); }
    }
  }
  return root;
}

function _treeToArray(root) {
  if (root === null || root === undefined) return [];
  const out = [];
  const queue = [root];
  while (queue.length > 0) {
    const node = queue.shift();
    if (node === null || node === undefined) { out.push(null); }
    else { out.push(node.val); queue.push(node.left === undefined ? null : node.left); queue.push(node.right === undefined ? null : node.right); }
  }
  while (out.length > 0 && out[out.length - 1] === null) out.pop();
  return out;
}

function _applyArgTransforms(args, map) {
  args = args.slice();
  for (const key of Object.keys(map || {})) {
    const i = parseInt(key, 10);
    if (map[key] === "linked_list") args[i] = _buildLinkedList(args[i]);
    else if (map[key] === "binary_tree") args[i] = _buildTree(args[i]);
  }
  return args;
}

function _applyResultTransform(result, kind) {
  if (kind === "linked_list") return _linkedListToArray(result);
  if (kind === "binary_tree") return _treeToArray(result);
  return result;
}
"""

RUNNER_HEADER = r"""
'use strict';
const vm = require('vm');

""" + NODE_HELPERS

RUNNER_FOOTER_TEMPLATE = r"""

const USER_CODE = {user_code_js};
const FUNCTION_NAME = {function_name_js};
const TEST_ARGS = JSON.parse({test_args_js});
const IO_TRANSFORM = JSON.parse({io_transform_js});

const sandbox = {{ console: console, ListNode: _ListNode, TreeNode: _TreeNode }};
vm.createContext(sandbox);

const exportLine = "\n;globalThis.__algomind_fn = (typeof " + FUNCTION_NAME + " !== 'undefined') ? " + FUNCTION_NAME + " : undefined;\n";

let script;
try {{
  script = new vm.Script(USER_CODE + exportLine, {{ filename: 'submission.js' }});
}} catch (e) {{
  console.log(JSON.stringify({{ kind: 'compile_error', message: String((e && e.message) || e) }}));
  process.exit(0);
}}

try {{
  script.runInContext(sandbox, {{ timeout: {vm_timeout_ms} }});
}} catch (e) {{
  console.log(JSON.stringify({{ kind: 'compile_error', message: String((e && e.message) || e) }}));
  process.exit(0);
}}

const fn = sandbox.__algomind_fn;
if (typeof fn !== 'function') {{
  console.log(JSON.stringify({{ kind: 'compile_error', message: 'Function ' + FUNCTION_NAME + ' not defined' }}));
  process.exit(0);
}}

const results = [];
for (const args of TEST_ARGS) {{
  try {{
    const callArgs = _applyArgTransforms(JSON.parse(JSON.stringify(args)), IO_TRANSFORM.args || {{}});
    let out = fn.apply(null, callArgs);
    out = _applyResultTransform(out, IO_TRANSFORM.result);
    results.push({{ kind: 'ok', value: out === undefined ? null : out }});
  }} catch (e) {{
    results.push({{ kind: 'runtime_error', message: String((e && e.message) || e) }});
  }}
}}

console.log(JSON.stringify({{ kind: 'results', results: results }}));
"""


def _node_executable() -> str | None:
    return shutil.which("node")


def run_javascript(
    code: str, function_name: str, test_args: list[list], io_transform: dict | None, timeout_s: float,
) -> ExecutionResult:
    node = _node_executable()
    if node is None:
        return ExecutionResult(
            status="RUNTIME_ERROR", runtime_ms=0.0,
            error_message="JavaScript execution is unavailable on this server (Node.js was not found).",
        )

    # A JSON-encoded JSON string is also valid JS string-literal source (its own
    # escaping already satisfies JS's), so this embeds the payload without needing
    # a second, JS-specific escaping pass.
    script_source = RUNNER_HEADER + RUNNER_FOOTER_TEMPLATE.format(
        user_code_js=json.dumps(code),
        function_name_js=json.dumps(function_name),
        test_args_js=json.dumps(json.dumps(test_args)),
        io_transform_js=json.dumps(json.dumps(io_transform or {})),
        vm_timeout_ms=int(timeout_s * 1000),
    )

    with tempfile.TemporaryDirectory(prefix="algomind_js_sandbox_") as tmpdir:
        script_path = Path(tmpdir) / "runner.js"
        script_path.write_text(script_source, encoding="utf-8")

        start = time.perf_counter()
        try:
            proc = subprocess.run(
                [node, "--no-addons", str(script_path)],
                cwd=tmpdir, capture_output=True, text=True, timeout=timeout_s,
            )
        except subprocess.TimeoutExpired:
            elapsed_ms = (time.perf_counter() - start) * 1000
            return ExecutionResult(status="TIMEOUT", runtime_ms=elapsed_ms,
                                    error_message=f"Exceeded {timeout_s}s time limit")

        elapsed_ms = (time.perf_counter() - start) * 1000

        if proc.returncode != 0:
            return ExecutionResult(
                status="RUNTIME_ERROR", runtime_ms=elapsed_ms,
                error_message=proc.stderr.strip()[-2000:] or "Process exited with a non-zero status",
            )

        try:
            payload = json.loads(proc.stdout.strip().splitlines()[-1])
        except (json.JSONDecodeError, IndexError):
            return ExecutionResult(
                status="RUNTIME_ERROR", runtime_ms=elapsed_ms,
                error_message="Sandbox produced no parseable output: " + proc.stdout[-500:],
            )

        if payload["kind"] == "compile_error":
            return ExecutionResult(status="COMPILE_ERROR", runtime_ms=elapsed_ms, error_message=payload["message"])

        outcomes = [
            TestOutcome(kind=r["kind"], value=r.get("value"), message=r.get("message"))
            for r in payload["results"]
        ]
        return ExecutionResult(status="EXECUTED", runtime_ms=elapsed_ms, outcomes=outcomes)
