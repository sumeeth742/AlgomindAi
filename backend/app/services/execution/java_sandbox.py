"""
Isolated Java code execution.

Java is statically typed, but a problem's parameter/return types are never
authored anywhere -- they only exist implicitly in the shape of its (already
verified) Python test data. So every test-case argument is compiled in as a
Java literal (not parsed from JSON at runtime, which would need a JSON
library and still face the same "what type is this?" question); this mirrors
what the Python/JS sandboxes do by embedding test data directly into the
generated runner script. The user's code is compiled fresh, in an isolated
temp directory, every submission -- there is no persistent Java process and
nothing here is precomputed or faked.
"""
from __future__ import annotations

import json as _json
import shutil
import subprocess
import time
from pathlib import Path
from tempfile import TemporaryDirectory

from app.services.execution.result_types import ExecutionResult, TestOutcome
from app.services.execution.type_inference import TypeTag

MAIN_JAVA_HEADER = r"""
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        StringBuilder sb = new StringBuilder();
        sb.append("{\"kind\":\"results\",\"results\":[");
        Solution sol = new Solution();
"""

MAIN_JAVA_HELPERS = r"""
    static String q(String s) {
        StringBuilder b = new StringBuilder("\"");
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            switch (c) {
                case '"': b.append("\\\""); break;
                case '\\': b.append("\\\\"); break;
                case '\n': b.append("\\n"); break;
                case '\r': b.append("\\r"); break;
                case '\t': b.append("\\t"); break;
                default:
                    if (c < 0x20) { b.append(String.format("\\u%04x", (int) c)); } else { b.append(c); }
            }
        }
        b.append("\"");
        return b.toString();
    }
    static String intArrayToJson(int[] a) { StringBuilder b = new StringBuilder("["); for (int i = 0; i < a.length; i++) { if (i > 0) b.append(","); b.append(a[i]); } b.append("]"); return b.toString(); }
    static String doubleArrayToJson(double[] a) { StringBuilder b = new StringBuilder("["); for (int i = 0; i < a.length; i++) { if (i > 0) b.append(","); b.append(a[i]); } b.append("]"); return b.toString(); }
    static String boolArrayToJson(boolean[] a) { StringBuilder b = new StringBuilder("["); for (int i = 0; i < a.length; i++) { if (i > 0) b.append(","); b.append(a[i]); } b.append("]"); return b.toString(); }
    static String stringArrayToJson(String[] a) { StringBuilder b = new StringBuilder("["); for (int i = 0; i < a.length; i++) { if (i > 0) b.append(","); b.append(q(a[i])); } b.append("]"); return b.toString(); }
    static String listIntToJson(List<Integer> l) { StringBuilder b = new StringBuilder("["); for (int i = 0; i < l.size(); i++) { if (i > 0) b.append(","); b.append(l.get(i)); } b.append("]"); return b.toString(); }
    static String listDoubleToJson(List<Double> l) { StringBuilder b = new StringBuilder("["); for (int i = 0; i < l.size(); i++) { if (i > 0) b.append(","); b.append(l.get(i)); } b.append("]"); return b.toString(); }
    static String listBoolToJson(List<Boolean> l) { StringBuilder b = new StringBuilder("["); for (int i = 0; i < l.size(); i++) { if (i > 0) b.append(","); b.append(l.get(i)); } b.append("]"); return b.toString(); }
    static String listStringToJson(List<String> l) { StringBuilder b = new StringBuilder("["); for (int i = 0; i < l.size(); i++) { if (i > 0) b.append(","); b.append(q(l.get(i))); } b.append("]"); return b.toString(); }
    static String listListIntToJson(List<List<Integer>> l) { StringBuilder b = new StringBuilder("["); for (int i = 0; i < l.size(); i++) { if (i > 0) b.append(","); b.append(listIntToJson(l.get(i))); } b.append("]"); return b.toString(); }
    static String listListStringToJson(List<List<String>> l) { StringBuilder b = new StringBuilder("["); for (int i = 0; i < l.size(); i++) { if (i > 0) b.append(","); b.append(listStringToJson(l.get(i))); } b.append("]"); return b.toString(); }
    static String nullableIntListToJson(List<Integer> l) { StringBuilder b = new StringBuilder("["); for (int i = 0; i < l.size(); i++) { if (i > 0) b.append(","); Integer v = l.get(i); b.append(v == null ? "null" : String.valueOf(v)); } b.append("]"); return b.toString(); }

    static ListNode buildLinkedList(int[] values) {
        ListNode head = null, tail = null;
        for (int v : values) {
            ListNode node = new ListNode(v);
            if (head == null) { head = node; tail = node; } else { tail.next = node; tail = node; }
        }
        return head;
    }
    static List<Integer> linkedListToList(ListNode node) {
        List<Integer> out = new ArrayList<>();
        Set<ListNode> seen = new HashSet<>();
        while (node != null && !seen.contains(node)) { seen.add(node); out.add(node.val); node = node.next; }
        return out;
    }
    static TreeNode buildTree(Integer[] values) {
        if (values.length == 0 || values[0] == null) return null;
        int i = 0;
        TreeNode root = new TreeNode(values[i++]);
        Deque<TreeNode> queue = new ArrayDeque<>();
        queue.add(root);
        while (!queue.isEmpty() && i < values.length) {
            TreeNode node = queue.poll();
            if (i < values.length) {
                Integer lv = values[i++];
                if (lv != null) { node.left = new TreeNode(lv); queue.add(node.left); }
            }
            if (i < values.length) {
                Integer rv = values[i++];
                if (rv != null) { node.right = new TreeNode(rv); queue.add(node.right); }
            }
        }
        return root;
    }
    static List<Integer> treeToList(TreeNode root) {
        List<Integer> out = new ArrayList<>();
        if (root == null) return out;
        Deque<TreeNode> queue = new ArrayDeque<>();
        queue.add(root);
        while (!queue.isEmpty()) {
            TreeNode node = queue.poll();
            if (node == null) { out.add(null); }
            else { out.add(node.val); queue.add(node.left); queue.add(node.right); }
        }
        while (!out.isEmpty() && out.get(out.size() - 1) == null) out.remove(out.size() - 1);
        return out;
    }
}

class ListNode { int val; ListNode next; ListNode(int val) { this.val = val; } }
class TreeNode { int val; TreeNode left; TreeNode right; TreeNode(int val) { this.val = val; } }
"""


def _java_literal(value, java_type: str) -> str:
    if java_type == "int":
        return str(int(value))
    if java_type == "double":
        return repr(float(value))
    if java_type == "boolean":
        return "true" if value else "false"
    if java_type == "String":
        return _json.dumps(value)
    if java_type == "int[]":
        return "new int[]{" + ", ".join(str(int(v)) for v in value) + "}"
    if java_type == "double[]":
        return "new double[]{" + ", ".join(repr(float(v)) for v in value) + "}"
    if java_type == "boolean[]":
        return "new boolean[]{" + ", ".join("true" if v else "false" for v in value) + "}"
    if java_type == "String[]":
        return "new String[]{" + ", ".join(_json.dumps(v) for v in value) + "}"
    if java_type == "ListNode":
        return "Main.buildLinkedList(new int[]{" + ", ".join(str(int(v)) for v in value) + "})"
    if java_type == "TreeNode":
        parts = ["null" if v is None else str(int(v)) for v in value]
        return "Main.buildTree(new Integer[]{" + ", ".join(parts) + "})"
    if java_type.startswith("List<List<"):
        elem_type = java_type[len("List<List<"):-2]  # "Integer" from "List<List<Integer>>"
        items = [_java_literal(v, f"List<{elem_type}>") for v in value]
        return f"java.util.Arrays.<List<{elem_type}>>asList(" + ", ".join(items) + ")"
    if java_type.startswith("List<"):
        elem_type = java_type[len("List<"):-1]
        if elem_type == "String":
            items = [_json.dumps(v) for v in value]
        elif elem_type == "Boolean":
            items = ["true" if v else "false" for v in value]
        else:
            items = [str(v) for v in value]
        return f"java.util.Arrays.<{elem_type}>asList(" + ", ".join(items) + ")"
    return "null"


def _java_type(tag: TypeTag) -> str:
    if tag.kind == "linked_list":
        return "ListNode"
    if tag.kind == "binary_tree":
        return "TreeNode"
    if tag.kind == "int":
        return "int"
    if tag.kind == "double":
        return "double"
    if tag.kind == "bool":
        return "boolean"
    if tag.kind == "string":
        return "String"
    if tag.kind == "list":
        inner = tag.element
        if inner.kind == "int":
            return "int[]"
        if inner.kind == "double":
            return "double[]"
        if inner.kind == "bool":
            return "boolean[]"
        if inner.kind == "string":
            return "String[]"
        if inner.kind == "list":
            # `tag` here is the FULL (possibly multi-level) list tag, not
            # `inner` -- _boxed_generic_type already accounts for one level of
            # nesting per recursive step, so passing `inner` (itself already
            # one level in) would double-count a level and produce
            # List<List<List<Integer>>> for a plain 2-D List<List<Integer>>.
            return _boxed_generic_type(tag)
    return "Object"


def java_types_for(param_tags: list[TypeTag], return_tag: TypeTag) -> tuple[list[str], str]:
    """Public entry point for the router: turns the inferred parameter/return
    TypeTags (see type_inference.py / starter_code.py) into the Java type
    strings this module's literal embedding and result serialization use."""
    return [_java_type(t) for t in param_tags], _java_type(return_tag)


_SCALAR_BOXED = {"int": "Integer", "double": "Double", "bool": "Boolean", "string": "String"}


def _boxed_generic_type(tag: TypeTag) -> str:
    """Java generic List<...> type for a value of exactly this list shape."""
    inner = tag.element
    if inner.kind == "list":
        return f"List<{_boxed_generic_type(inner)}>"
    return f"List<{_SCALAR_BOXED.get(inner.kind, 'Object')}>"


def _serialize_expr(return_type: str, var: str) -> str:
    if return_type in ("int", "double", "boolean"):
        return f"String.valueOf({var})"
    if return_type == "String":
        return f"q({var})"
    if return_type == "ListNode":
        return f"listIntToJson(linkedListToList({var}))"
    if return_type == "TreeNode":
        return f"nullableIntListToJson(treeToList({var}))"
    if return_type == "int[]":
        return f"intArrayToJson({var})"
    if return_type == "double[]":
        return f"doubleArrayToJson({var})"
    if return_type == "boolean[]":
        return f"boolArrayToJson({var})"
    if return_type == "String[]":
        return f"stringArrayToJson({var})"
    if return_type == "List<List<Integer>>":
        return f"listListIntToJson({var})"
    if return_type == "List<List<String>>":
        return f"listListStringToJson({var})"
    if return_type == "List<Integer>":
        return f"listIntToJson({var})"
    if return_type == "List<Double>":
        return f"listDoubleToJson({var})"
    if return_type == "List<Boolean>":
        return f"listBoolToJson({var})"
    if return_type == "List<String>":
        return f"listStringToJson({var})"
    return f"String.valueOf({var})"


def _render_main_java(function_name: str, param_types: list[str], return_type: str, test_args: list[list]) -> str:
    body_lines = [MAIN_JAVA_HEADER]
    for i, args in enumerate(test_args):
        arg_exprs = [_java_literal(v, t) for v, t in zip(args, param_types)]
        call = f"sol.{function_name}(" + ", ".join(arg_exprs) + ")"
        body_lines.append(f"""
        if ({i} > 0) sb.append(",");
        try {{
            {return_type} result{i} = {call};
            sb.append("{{\\"kind\\":\\"ok\\",\\"value\\":").append({_serialize_expr(return_type, f'result{i}')}).append("}}");
        }} catch (Throwable e) {{
            sb.append("{{\\"kind\\":\\"runtime_error\\",\\"message\\":").append(q(String.valueOf(e))).append("}}");
        }}
""")
    body_lines.append("""
        sb.append("]}");
        System.out.println(sb.toString());
    }
""")
    return "".join(body_lines) + MAIN_JAVA_HELPERS


def _tool(name: str) -> str | None:
    return shutil.which(name)


def run_java(
    code: str, function_name: str, param_types: list[str], return_type: str,
    test_args: list[list], timeout_s: float,
) -> ExecutionResult:
    javac, java = _tool("javac"), _tool("java")
    if javac is None or java is None:
        return ExecutionResult(
            status="RUNTIME_ERROR", runtime_ms=0.0,
            error_message="Java execution is unavailable on this server (a JDK was not found).",
        )

    main_java = _render_main_java(function_name, param_types, return_type, test_args)
    solution_java = "import java.util.*;\nimport java.util.stream.*;\n\n" + code

    with TemporaryDirectory(prefix="algomind_java_sandbox_") as tmpdir:
        tmp = Path(tmpdir)
        (tmp / "Main.java").write_text(main_java, encoding="utf-8")
        (tmp / "Solution.java").write_text(solution_java, encoding="utf-8")

        start = time.perf_counter()
        try:
            compile_proc = subprocess.run(
                [javac, "-d", tmpdir, "Main.java", "Solution.java"],
                cwd=tmpdir, capture_output=True, text=True, timeout=20,
            )
        except subprocess.TimeoutExpired:
            return ExecutionResult(status="TIMEOUT", runtime_ms=(time.perf_counter() - start) * 1000,
                                    error_message="Compilation exceeded its time limit")

        if compile_proc.returncode != 0:
            elapsed_ms = (time.perf_counter() - start) * 1000
            return ExecutionResult(status="COMPILE_ERROR", runtime_ms=elapsed_ms,
                                    error_message=compile_proc.stderr.strip()[-3000:])

        try:
            run_proc = subprocess.run(
                [java, "-cp", tmpdir, "Main"],
                cwd=tmpdir, capture_output=True, text=True, timeout=timeout_s,
            )
        except subprocess.TimeoutExpired:
            elapsed_ms = (time.perf_counter() - start) * 1000
            return ExecutionResult(status="TIMEOUT", runtime_ms=elapsed_ms,
                                    error_message=f"Exceeded {timeout_s}s time limit")

        elapsed_ms = (time.perf_counter() - start) * 1000

        if run_proc.returncode != 0:
            return ExecutionResult(
                status="RUNTIME_ERROR", runtime_ms=elapsed_ms,
                error_message=run_proc.stderr.strip()[-2000:] or "Process exited with a non-zero status",
            )

        try:
            payload = _json.loads(run_proc.stdout.strip().splitlines()[-1])
        except (_json.JSONDecodeError, IndexError):
            return ExecutionResult(
                status="RUNTIME_ERROR", runtime_ms=elapsed_ms,
                error_message="Sandbox produced no parseable output: " + run_proc.stdout[-500:],
            )

        outcomes = [
            TestOutcome(kind=r["kind"], value=r.get("value"), message=r.get("message"))
            for r in payload["results"]
        ]
        return ExecutionResult(status="EXECUTED", runtime_ms=elapsed_ms, outcomes=outcomes)
