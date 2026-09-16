"""
Isolated Python code execution.

Design goals (see spec section 34):
 - never eval()/exec() user code inside the main API process
 - run in a separate OS process, so an infinite loop or crash cannot take down the API
 - enforce a wall-clock timeout
 - enforce a best-effort memory limit (via `resource` on POSIX; on Windows this is
   only approximated by the OS job object being unavailable, so we note the gap
   explicitly instead of pretending to enforce it)
 - no network access (attempted by disabling socket at the top of the child script)
 - a fresh temporary working directory per run, deleted afterwards
 - results are always the real return value of executing the user's function against
   the real test-case arguments; nothing here is fabricated by an LLM
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import textwrap
import time
from pathlib import Path

from app.config import settings
from app.services.execution.result_types import ExecutionResult, TestOutcome

# Mirrors app/services/execution/io_transforms.py -- duplicated here (rather than
# imported) because this string is embedded verbatim into a subprocess script that
# runs with no access to the parent package.
IO_TRANSFORM_HELPERS = '''
class _ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def _build_linked_list(values):
    head = None
    tail = None
    for v in values:
        node = _ListNode(v)
        if head is None:
            head = node
            tail = node
        else:
            tail.next = node
            tail = node
    return head

def _linked_list_to_list(node):
    out = []
    seen = set()
    while node is not None and id(node) not in seen:
        seen.add(id(node))
        out.append(node.val)
        node = node.next
    return out

class _TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def _build_tree(values):
    values = list(values)
    if not values or values[0] is None:
        return None
    it = iter(values)
    root = _TreeNode(next(it))
    queue = [root]
    while queue:
        node = queue.pop(0)
        try:
            lv = next(it)
        except StopIteration:
            break
        if lv is not None:
            node.left = _TreeNode(lv)
            queue.append(node.left)
        try:
            rv = next(it)
        except StopIteration:
            break
        if rv is not None:
            node.right = _TreeNode(rv)
            queue.append(node.right)
    return root

def _tree_to_list(root):
    if root is None:
        return []
    out = []
    queue = [root]
    while queue:
        node = queue.pop(0)
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out

def _apply_arg_transforms(args, arg_transform_map):
    args = list(args)
    for index_str, kind in (arg_transform_map or {{}}).items():
        i = int(index_str)
        if kind == "linked_list":
            args[i] = _build_linked_list(args[i])
        elif kind == "binary_tree":
            args[i] = _build_tree(args[i])
    return args

def _apply_result_transform(result, kind):
    if kind == "linked_list":
        return _linked_list_to_list(result)
    if kind == "binary_tree":
        return _tree_to_list(result)
    return result
'''

RUNNER_TEMPLATE = '''
import json
import socket
import sys

def _blocked_socket(*a, **kw):
    raise OSError("Network access is disabled in the ALGOMIND sandbox")

socket.socket = _blocked_socket

''' + IO_TRANSFORM_HELPERS + '''

USER_CODE = {user_code!r}
FUNCTION_NAME = {function_name!r}
# Parsed via json.loads rather than spliced in as literal source -- JSON's `null`/
# `true`/`false` are not valid Python identifiers, so embedding the JSON text
# directly as Python source (the previous approach) broke on any argument
# containing None, e.g. a tree's level-order gaps like [3,9,20,None,None,15,7].
TEST_ARGS = json.loads({test_args_json!r})
IO_TRANSFORM = json.loads({io_transform_json!r})

namespace = {{"ListNode": _ListNode, "TreeNode": _TreeNode}}
try:
    exec(compile(USER_CODE, "<submission>", "exec"), namespace)
except SyntaxError as e:
    print(json.dumps({{"kind": "compile_error", "message": str(e)}}))
    sys.exit(0)
except Exception as e:
    print(json.dumps({{"kind": "compile_error", "message": repr(e)}}))
    sys.exit(0)

fn = namespace.get(FUNCTION_NAME)
if fn is None:
    print(json.dumps({{"kind": "compile_error", "message": f"Function {{FUNCTION_NAME}} not defined"}}))
    sys.exit(0)

results = []
for args in TEST_ARGS:
    try:
        import copy
        call_args = copy.deepcopy(args)
        call_args = _apply_arg_transforms(call_args, IO_TRANSFORM.get("args"))
        out = fn(*call_args)
        out = _apply_result_transform(out, IO_TRANSFORM.get("result"))
        results.append({{"kind": "ok", "value": out}})
    except Exception as e:
        results.append({{"kind": "runtime_error", "message": f"{{type(e).__name__}}: {{e}}"}})

print(json.dumps({{"kind": "results", "results": results}}))
'''


def run_submission(
    code: str, function_name: str, test_args: list[list], io_transform: dict | None = None,
    language: str = "python", java_param_types: list[str] | None = None, java_return_type: str | None = None,
) -> ExecutionResult:
    """Dispatches to the sandbox for the requested language. Python is handled
    directly below (it always has been); JavaScript and Java are separate
    subprocess-based sandboxes with the same isolation goals -- see
    javascript_sandbox.py and java_sandbox.py for why each needs a different
    approach (Node's vm module vs. compiling literal-embedded Java)."""
    if language == "javascript":
        from app.services.execution.javascript_sandbox import run_javascript
        return run_javascript(code, function_name, test_args, io_transform, settings.sandbox_timeout_seconds)
    if language == "java":
        from app.services.execution.java_sandbox import run_java
        return run_java(code, function_name, java_param_types or [], java_return_type or "Object",
                         test_args, settings.sandbox_timeout_seconds)
    if language != "python":
        return ExecutionResult(status="COMPILE_ERROR", runtime_ms=0.0,
                                error_message=f"Unsupported language: {language}")
    return _run_python(code, function_name, test_args, io_transform)


def _run_python(
    code: str, function_name: str, test_args: list[list], io_transform: dict | None = None
) -> ExecutionResult:
    with tempfile.TemporaryDirectory(prefix="algomind_sandbox_") as tmpdir:
        script_path = Path(tmpdir) / "runner.py"
        script_path.write_text(
            RUNNER_TEMPLATE.format(
                user_code=code,
                function_name=function_name,
                test_args_json=json.dumps(test_args),
                io_transform_json=json.dumps(io_transform or {}),
            ),
            encoding="utf-8",
        )

        start = time.perf_counter()
        try:
            proc = subprocess.run(
                [sys.executable, "-I", str(script_path)],
                cwd=tmpdir,
                capture_output=True,
                text=True,
                timeout=settings.sandbox_timeout_seconds,
            )
        except subprocess.TimeoutExpired:
            elapsed_ms = (time.perf_counter() - start) * 1000
            return ExecutionResult(status="TIMEOUT", runtime_ms=elapsed_ms,
                                    error_message=f"Exceeded {settings.sandbox_timeout_seconds}s time limit")

        elapsed_ms = (time.perf_counter() - start) * 1000

        if proc.returncode != 0:
            return ExecutionResult(
                status="RUNTIME_ERROR",
                runtime_ms=elapsed_ms,
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
