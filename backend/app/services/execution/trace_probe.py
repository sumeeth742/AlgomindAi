"""
Step-through execution tracing of a learner's own submitted code.

The concept-lesson visualizers (frontend/src/lib/visualizations.ts) animate a
hand-authored trace of the *reference* approach. That's useful for learning
the technique in the abstract, but when a learner's own code is wrong, what
actually helps is watching their own logic run against the exact input that
broke it -- not someone else's correct solution. This module gets that trace
by real introspection (Python's `sys.settrace`, a standard-library debugging
hook), never by re-deriving or guessing what the code "probably" does: every
line number and every variable value shown is what genuinely happened when
this exact code executed this exact input, inside the same sandboxed
subprocess model the rest of execution uses (see sandbox.py).

Python and JavaScript use genuinely different mechanisms, because there's no
single approach that works for both: Python uses `sys.settrace`, a real
CPython debugging hook that reports every line and every local variable as
the interpreter actually executes them. JavaScript has no equivalent
available here -- Node's inspector/debugger protocol was tried first and
found to be unreliable for this exact case (a synchronous, in-process
`Debugger.paused` handler doesn't actually halt V8 execution the way a real
attached debugger does; confirmed by testing before this file settled on a
different approach) -- so JavaScript instead uses source instrumentation: the
learner's function is parsed into a real AST (`espree`, via
`js_analyzer/instrument.js`) and a trace-recording call is spliced in before
every statement, using a scope stack to track exactly which variable names
are genuinely in scope at each point (so the generated code never references
a `let`/`const` before its real declaration, which would throw). Every value
shown is still the real, live value at that point in the *learner's own,
unmodified* logic -- instrumentation adds recording calls, it does not change
what the code computes.

Java uses JDI (Java Debug Interface) -- the same mechanism real Java
debuggers (jdb, IntelliJ, VS Code) are built on -- via a small standalone
driver program (`java_trace/TraceDriver.java`, compiled once and reused
across requests since its own source never depends on the submission being
traced). It launches the already-familiar `Main`/`Solution` pair (the exact
same generation code java_sandbox.py uses for a normal run, just compiled
with `-g` for local-variable debug info this one time) as a *debuggee* JVM,
sets a real breakpoint at the target method's first line via JDWP, and
single-steps through with a class filter scoped to `Solution` -- so it steps
genuinely *into* the method's own recursive calls (a real stack, with real
depth) while transparently skipping over JDK-internal calls like
`HashMap.put` without single-stepping through their bytecode (verified by
timing: a five-level recursive trace with an unrelated HashMap call completed
in about a second). Objects without special handling (a `HashMap`, an
`ArrayList`, a learner's own helper class) are described by invoking their
real `toString()` inside the debuggee via JDI -- an actual computed value,
not a fabricated summary, the same way a real debugger's variable pane falls
back to `toString()` for arbitrary objects.

All three language tracers are scoped to the target function's own lines
only, not into any helper function it calls, and capped at a step count so a
large or slow-but-correct input can't produce an unbounded trace or blow past
the sandbox timeout (Python's `sys.settrace` in particular adds real
per-line overhead; JDI single-stepping does too, though far less than
`sys.settrace` since JDK-internal frames are filtered out at the JVM level
rather than visited one bytecode at a time).
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

from app.config import settings
from app.services.execution.java_sandbox import _render_main_java
from app.services.execution.javascript_sandbox import NODE_HELPERS
from app.services.execution.sandbox import IO_TRANSFORM_HELPERS

MAX_TRACE_STEPS = 500
TRACE_TIMEOUT_SECONDS = max(settings.sandbox_timeout_seconds, 8.0)  # settrace/instrumentation add real overhead
JS_INSTRUMENT_SCRIPT = Path(__file__).parent / "js_analyzer" / "instrument.js"
JAVA_TRACE_DIR = Path(__file__).parent / "java_trace"
JAVA_TRACE_DRIVER_TIMEOUT_SECONDS = max(TRACE_TIMEOUT_SECONDS, 15.0)  # JVM launch + JDI attach adds real startup cost

TRACE_RUNNER_TEMPLATE = '''
import json
import socket
import sys

def _blocked_socket(*a, **kw):
    raise OSError("Network access is disabled in the ALGOMIND sandbox")

socket.socket = _blocked_socket

''' + IO_TRANSFORM_HELPERS + '''

USER_CODE = {user_code!r}
FUNCTION_NAME = {function_name!r}
CALL_ARGS = json.loads({args_json!r})
IO_TRANSFORM = json.loads({io_transform_json!r})
MAX_STEPS = {max_steps}

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

def _safe_value(v):
    if isinstance(v, _ListNode):
        return {{"__type__": "linked_list", "values": _linked_list_to_list(v)}}
    if isinstance(v, _TreeNode):
        return {{"__type__": "binary_tree", "values": _tree_to_list(v)}}
    try:
        json.dumps(v)
        # A deep copy, not the live object: dicts/lists get mutated in place
        # (seen[x] = i, results.append(...)) as execution continues, and every
        # step's snapshot is only serialized to JSON once at the very end --
        # storing a bare reference here means every step showing that
        # variable would display its FINAL state, not its state at that
        # point in time. Confirmed as a real bug: a hashmap-based two-sum's
        # `seen` dict showed all entries already present from step one.
        return copy.deepcopy(v)
    except TypeError:
        return repr(v)

STEPS = []
DEPTH = [0]
STEP_COUNT = [0]
TARGET_CODE = fn.__code__

def _local_tracer(frame, event, arg):
    if event == "line":
        if STEP_COUNT[0] >= MAX_STEPS:
            return None
        STEP_COUNT[0] += 1
        snapshot = {{k: _safe_value(v) for k, v in frame.f_locals.items() if not k.startswith("_")}}
        STEPS.append({{"line": frame.f_lineno, "depth": DEPTH[0], "locals": snapshot}})
    elif event == "return":
        DEPTH[0] -= 1
    return _local_tracer

def _global_tracer(frame, event, arg):
    if event == "call" and frame.f_code is TARGET_CODE:
        DEPTH[0] += 1
        return _local_tracer
    return None

import copy
call_args = copy.deepcopy(CALL_ARGS)
call_args = _apply_arg_transforms(call_args, IO_TRANSFORM.get("args"))

sys.settrace(_global_tracer)
try:
    result = fn(*call_args)
    status = "ok"
    error_message = None
except Exception as e:
    result = None
    status = "runtime_error"
    error_message = f"{{type(e).__name__}}: {{e}}"
finally:
    sys.settrace(None)

print(json.dumps({{
    "kind": "trace",
    "status": status,
    "error_message": error_message,
    "result": _safe_value(_apply_result_transform(result, IO_TRANSFORM.get("result"))) if status == "ok" else None,
    "steps": STEPS,
    "truncated": STEP_COUNT[0] >= MAX_STEPS,
}}))
'''


@dataclass
class TraceStep:
    line: int
    depth: int
    locals: dict


@dataclass
class TraceReport:
    supported: bool
    reason: str | None = None
    status: str | None = None
    error_message: str | None = None
    result: object = None
    steps: list[TraceStep] = field(default_factory=list)
    truncated: bool = False
    source_lines: list[str] = field(default_factory=list)


def trace_python_execution(code: str, function_name: str, args: list, io_transform: dict | None) -> TraceReport:
    source_lines = code.splitlines()
    script_source = TRACE_RUNNER_TEMPLATE.format(
        user_code=code, function_name=function_name,
        args_json=json.dumps(args),
        io_transform_json=json.dumps(io_transform or {}),
        max_steps=MAX_TRACE_STEPS,
    )

    with tempfile.TemporaryDirectory(prefix="algomind_trace_") as tmpdir:
        script_path = Path(tmpdir) / "tracer.py"
        script_path.write_text(script_source, encoding="utf-8")
        try:
            proc = subprocess.run(
                [sys.executable, "-I", str(script_path)],
                cwd=tmpdir, capture_output=True, text=True, timeout=TRACE_TIMEOUT_SECONDS,
            )
        except subprocess.TimeoutExpired:
            return TraceReport(
                supported=True, status="runtime_error",
                error_message=f"Tracing exceeded its {TRACE_TIMEOUT_SECONDS}s time limit -- this input may run too "
                              "long (or loop forever) to trace step by step, even though the real submission timeout differs.",
                source_lines=source_lines,
            )

        if proc.returncode != 0:
            return TraceReport(
                supported=True, status="runtime_error",
                error_message=proc.stderr.strip()[-2000:] or "Process exited with a non-zero status",
                source_lines=source_lines,
            )

        try:
            payload = json.loads(proc.stdout.strip().splitlines()[-1])
        except (json.JSONDecodeError, IndexError):
            return TraceReport(
                supported=True, status="runtime_error",
                error_message="Sandbox produced no parseable output: " + proc.stdout[-500:],
                source_lines=source_lines,
            )

        if payload["kind"] == "compile_error":
            return TraceReport(supported=True, status="runtime_error", error_message=payload["message"], source_lines=source_lines)

        steps = [TraceStep(line=s["line"], depth=s["depth"], locals=s["locals"]) for s in payload["steps"]]
        return TraceReport(
            supported=True, status=payload["status"], error_message=payload.get("error_message"),
            result=payload.get("result"), steps=steps, truncated=payload["truncated"], source_lines=source_lines,
        )
def _instrument_js(code: str, function_name: str) -> dict | None:
    node = shutil.which("node")
    if node is None or not JS_INSTRUMENT_SCRIPT.exists():
        return None
    try:
        proc = subprocess.run(
            [node, str(JS_INSTRUMENT_SCRIPT)],
            input=json.dumps({"code": code, "functionName": function_name}),
            capture_output=True, text=True, timeout=10, cwd=str(JS_INSTRUMENT_SCRIPT.parent),
        )
    except subprocess.TimeoutExpired:
        return None
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return None


JS_TRACE_COLLECTOR = r"""
const STEPS = [];
const MAX_STEPS = %(max_steps)d;
function __trace(line, depth, locals) {
  if (STEPS.length >= MAX_STEPS) return;
  const safeLocals = {};
  for (const k of Object.keys(locals)) {
    const v = locals[k];
    if (v instanceof _ListNode) { safeLocals[k] = { __type__: "linked_list", values: _linkedListToArray(v) }; continue; }
    if (v instanceof _TreeNode) { safeLocals[k] = { __type__: "binary_tree", values: _treeToArray(v) }; continue; }
    try { safeLocals[k] = JSON.parse(JSON.stringify(v === undefined ? null : v)); }
    catch (e) { safeLocals[k] = String(v); }
  }
  STEPS.push({ line: line, depth: depth, locals: safeLocals });
}
"""


def trace_javascript_execution(code: str, function_name: str, args: list, io_transform: dict | None) -> TraceReport:
    source_lines = code.splitlines()
    instrumented = _instrument_js(code, function_name)
    if instrumented is None:
        return TraceReport(supported=False, reason="JavaScript tracing is unavailable on this server (Node.js or its instrumenter was not found).")
    if not instrumented.get("ok"):
        return TraceReport(supported=True, status="runtime_error", error_message=instrumented.get("message", "Could not parse this code to trace it."), source_lines=source_lines)

    runner_source = (
        "'use strict';\nconst vm = require('vm');\n\n"
        + NODE_HELPERS
        + "\n"
        + (JS_TRACE_COLLECTOR % {"max_steps": MAX_TRACE_STEPS})
        + "\n"
        + f"const INSTRUMENTED_CODE = {json.dumps(instrumented['instrumented'])};\n"
        + f"const FUNCTION_NAME = {json.dumps(function_name)};\n"
        + f"const CALL_ARGS = JSON.parse({json.dumps(json.dumps(args))});\n"
        + f"const IO_TRANSFORM = JSON.parse({json.dumps(json.dumps(io_transform or {}))});\n\n"
        + "const sandbox = { console: console, ListNode: _ListNode, TreeNode: _TreeNode, __trace: __trace, __algomindDepth: 0 };\n"
        + "vm.createContext(sandbox);\n\n"
        + "const exportLine = \"\\n;globalThis.__algomind_fn = (typeof \" + FUNCTION_NAME + \" !== 'undefined') ? \" + FUNCTION_NAME + \" : undefined;\\n\";\n\n"
        + "let script;\n"
        + "try {\n"
        + "  script = new vm.Script(INSTRUMENTED_CODE + exportLine, { filename: 'submission.js' });\n"
        + "} catch (e) {\n"
        + "  console.log(JSON.stringify({ kind: 'compile_error', message: String((e && e.message) || e) }));\n"
        + "  process.exit(0);\n"
        + "}\n\n"
        + "try {\n"
        + "  script.runInContext(sandbox);\n"
        + "} catch (e) {\n"
        + "  console.log(JSON.stringify({ kind: 'compile_error', message: String((e && e.message) || e) }));\n"
        + "  process.exit(0);\n"
        + "}\n\n"
        + "const fn = sandbox.__algomind_fn;\n"
        + "if (typeof fn !== 'function') {\n"
        + "  console.log(JSON.stringify({ kind: 'compile_error', message: 'Function ' + FUNCTION_NAME + ' not defined' }));\n"
        + "  process.exit(0);\n"
        + "}\n\n"
        + "let result, status, errorMessage;\n"
        + "try {\n"
        + "  const callArgs = _applyArgTransforms(JSON.parse(JSON.stringify(CALL_ARGS)), IO_TRANSFORM.args || {});\n"
        + "  result = fn.apply(null, callArgs);\n"
        + "  result = _applyResultTransform(result, IO_TRANSFORM.result);\n"
        + "  status = 'ok';\n"
        + "} catch (e) {\n"
        + "  status = 'runtime_error';\n"
        + "  errorMessage = String((e && e.message) || e);\n"
        + "}\n\n"
        + "let safeResult = null;\n"
        + "if (status === 'ok') {\n"
        + "  if (result instanceof _ListNode) safeResult = { __type__: 'linked_list', values: _linkedListToArray(result) };\n"
        + "  else if (result instanceof _TreeNode) safeResult = { __type__: 'binary_tree', values: _treeToArray(result) };\n"
        + "  else { try { safeResult = JSON.parse(JSON.stringify(result === undefined ? null : result)); } catch (e2) { safeResult = String(result); } }\n"
        + "}\n\n"
        + "console.log(JSON.stringify({ kind: 'trace', status: status, error_message: errorMessage || null, result: safeResult, steps: STEPS, truncated: STEPS.length >= MAX_STEPS }));\n"
    )

    node = shutil.which("node")
    with tempfile.TemporaryDirectory(prefix="algomind_js_trace_") as tmpdir:
        script_path = Path(tmpdir) / "tracer.js"
        script_path.write_text(runner_source, encoding="utf-8")
        try:
            proc = subprocess.run(
                [node, str(script_path)], cwd=tmpdir, capture_output=True, text=True, timeout=TRACE_TIMEOUT_SECONDS,
            )
        except subprocess.TimeoutExpired:
            return TraceReport(
                supported=True, status="runtime_error",
                error_message=f"Tracing exceeded its {TRACE_TIMEOUT_SECONDS}s time limit.",
                source_lines=source_lines,
            )

        if proc.returncode != 0:
            return TraceReport(
                supported=True, status="runtime_error",
                error_message=proc.stderr.strip()[-2000:] or "Process exited with a non-zero status",
                source_lines=source_lines,
            )

        try:
            payload = json.loads(proc.stdout.strip().splitlines()[-1])
        except (json.JSONDecodeError, IndexError):
            return TraceReport(
                supported=True, status="runtime_error",
                error_message="Sandbox produced no parseable output: " + proc.stdout[-500:],
                source_lines=source_lines,
            )

        if payload["kind"] == "compile_error":
            return TraceReport(supported=True, status="runtime_error", error_message=payload["message"], source_lines=source_lines)

        steps = [TraceStep(line=s["line"], depth=s["depth"], locals=s["locals"]) for s in payload["steps"]]
        return TraceReport(
            supported=True, status=payload["status"], error_message=payload.get("error_message"),
            result=payload.get("result"), steps=steps, truncated=payload["truncated"], source_lines=source_lines,
        )


_java_driver_compiled = False


def _ensure_java_trace_driver_compiled() -> bool:
    """TraceDriver.java's own source never depends on the submission being
    traced, so it's compiled once (cached across requests) rather than per
    submission -- unlike Solution.java/Main.java, which genuinely change
    every time and must be compiled fresh."""
    global _java_driver_compiled
    if _java_driver_compiled:
        return True
    javac = shutil.which("javac")
    if javac is None:
        return False
    driver_source = JAVA_TRACE_DIR / "TraceDriver.java"
    driver_class = JAVA_TRACE_DIR / "TraceDriver.class"
    if driver_class.exists() and driver_class.stat().st_mtime >= driver_source.stat().st_mtime:
        _java_driver_compiled = True
        return True
    try:
        proc = subprocess.run([javac, str(driver_source)], cwd=str(JAVA_TRACE_DIR), capture_output=True, text=True, timeout=30)
    except subprocess.TimeoutExpired:
        return False
    _java_driver_compiled = proc.returncode == 0
    return _java_driver_compiled


def trace_java_execution(
    code: str, function_name: str, args: list, io_transform: dict | None,
    java_param_types: list[str], java_return_type: str,
) -> TraceReport:
    source_lines = code.splitlines()
    javac, java = shutil.which("javac"), shutil.which("java")
    if javac is None or java is None:
        return TraceReport(supported=False, reason="Java tracing is unavailable on this server (a JDK was not found).")
    if not _ensure_java_trace_driver_compiled():
        return TraceReport(supported=False, reason="Java tracing is unavailable on this server (the trace driver could not be compiled).")

    # -g: local-variable debug info. The normal (non-tracing) Java sandbox
    # doesn't need this and doesn't pay for it -- only tracing does, since JDI
    # can't report a local's *name* without it (confirmed while prototyping:
    # without -g, every step's locals came back empty with an
    # AbsentInformationException).
    main_java = _render_main_java(function_name, java_param_types, java_return_type, [args])
    solution_java = "import java.util.*;\nimport java.util.stream.*;\n\n" + code

    with tempfile.TemporaryDirectory(prefix="algomind_java_trace_") as tmpdir:
        (Path(tmpdir) / "Main.java").write_text(main_java, encoding="utf-8")
        (Path(tmpdir) / "Solution.java").write_text(solution_java, encoding="utf-8")

        try:
            compile_proc = subprocess.run(
                [javac, "-g", "-d", tmpdir, "Main.java", "Solution.java"],
                cwd=tmpdir, capture_output=True, text=True, timeout=20,
            )
        except subprocess.TimeoutExpired:
            return TraceReport(supported=True, status="runtime_error", error_message="Compilation exceeded its time limit.", source_lines=source_lines)

        if compile_proc.returncode != 0:
            return TraceReport(supported=True, status="runtime_error", error_message=compile_proc.stderr.strip()[-3000:], source_lines=source_lines)

        classpath = f"{JAVA_TRACE_DIR}{os.pathsep}{tmpdir}"
        try:
            proc = subprocess.run(
                [java, "-cp", classpath, "TraceDriver", tmpdir, function_name, str(MAX_TRACE_STEPS)],
                cwd=tmpdir, capture_output=True, text=True, timeout=JAVA_TRACE_DRIVER_TIMEOUT_SECONDS,
            )
        except subprocess.TimeoutExpired:
            return TraceReport(
                supported=True, status="runtime_error",
                error_message=f"Tracing exceeded its {JAVA_TRACE_DRIVER_TIMEOUT_SECONDS}s time limit.",
                source_lines=source_lines,
            )

        if proc.returncode != 0:
            return TraceReport(
                supported=True, status="runtime_error",
                error_message=proc.stderr.strip()[-2000:] or "The trace driver exited with a non-zero status",
                source_lines=source_lines,
            )

        try:
            payload = json.loads(proc.stdout.strip().splitlines()[-1])
        except (json.JSONDecodeError, IndexError):
            return TraceReport(
                supported=True, status="runtime_error",
                error_message="The trace driver produced no parseable output: " + proc.stdout[-500:],
                source_lines=source_lines,
            )

        if payload.get("driverError"):
            return TraceReport(supported=True, status="runtime_error", error_message=payload["driverError"], source_lines=source_lines)

        main_output = payload.get("mainOutput")
        if main_output is None:
            return TraceReport(supported=True, status="runtime_error", error_message="The traced program produced no result.", source_lines=source_lines)
        if main_output.get("kind") == "compile_error":
            return TraceReport(supported=True, status="runtime_error", error_message=main_output["message"], source_lines=source_lines)

        result_entry = main_output["results"][0]
        status = "ok" if result_entry["kind"] == "ok" else "runtime_error"
        steps = [TraceStep(line=s["line"], depth=s["depth"], locals=s["locals"]) for s in payload["steps"]]
        return TraceReport(
            supported=True, status=status,
            error_message=result_entry.get("message") if status != "ok" else None,
            result=result_entry.get("value"), steps=steps, truncated=payload["truncated"], source_lines=source_lines,
        )
