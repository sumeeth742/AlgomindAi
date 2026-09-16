"""
Per-language starter code generation.

Every problem is authored once, in Python (see app/seed/problems_seed*.py).
Rather than hand-author a JavaScript and Java starter template for each of the
88 problems (which would need to be kept in sync by hand forever), the
signature for every other language is derived mechanically from data that
already exists and is already verified: the Python starter code's own
parameter names (parsed with `ast`, not guessed) and the real shape of the
problem's stored test-case arguments and expected output (computed by
executing the reference solution -- see seed_all.py). Nothing here invents
problem content; it only re-expresses an existing, verified signature in
another language's syntax.
"""
from __future__ import annotations

import ast

from app.services.execution.type_inference import TypeTag, merge_across_samples

# Verified against a real, installed toolchain on this server (see README's
# honest-scope notes) -- a language is only listed here once code has actually
# been compiled/run through it, not merely architected for.
SUPPORTED_LANGUAGES = ["python", "javascript", "java"]
LANGUAGE_LABELS = {"python": "Python", "javascript": "JavaScript", "java": "Java"}


def to_camel_case(snake_name: str) -> str:
    """Python problems are authored snake_case (see problems_seed*.py); JS and
    Java use camelCase by convention, so the generated starter code -- and the
    sandbox call that has to find the same symbol the user just implemented --
    both use this, not the raw Python name."""
    parts = snake_name.split("_")
    return parts[0] + "".join(p.capitalize() for p in parts[1:])


def function_name_for_language(function_name: str, language: str) -> str:
    if language == "python":
        return function_name
    return to_camel_case(function_name)


def extract_param_names(python_starter_code: str, function_name: str) -> list[str]:
    try:
        tree = ast.parse(python_starter_code)
    except SyntaxError:
        return []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            return [a.arg for a in node.args.args]
    return []


def infer_param_tags(test_case_args: list[list], io_transform: dict | None) -> list[TypeTag]:
    """One TypeTag per parameter position, merged across every test case so a
    single consistent type is used even if, say, one case's list happens to be
    empty and another's isn't."""
    if not test_case_args:
        return []
    arity = len(test_case_args[0])
    io_transform = io_transform or {}
    arg_overrides = io_transform.get("args", {})
    tags = []
    for i in range(arity):
        override = arg_overrides.get(str(i))
        if override == "linked_list":
            tags.append(TypeTag("linked_list"))
        elif override == "binary_tree":
            tags.append(TypeTag("binary_tree"))
        else:
            tags.append(merge_across_samples([args[i] for args in test_case_args]))
    return tags


def infer_return_tag(expected_outputs: list, io_transform: dict | None) -> TypeTag:
    io_transform = io_transform or {}
    result_override = io_transform.get("result")
    if result_override == "linked_list":
        return TypeTag("linked_list")
    if result_override == "binary_tree":
        return TypeTag("binary_tree")
    return merge_across_samples(expected_outputs)


def _js_type_hint(tag: TypeTag) -> str:
    if tag.kind == "linked_list":
        return "ListNode"
    if tag.kind == "binary_tree":
        return "TreeNode"
    if tag.kind == "int" or tag.kind == "double":
        return "number"
    if tag.kind == "bool":
        return "boolean"
    if tag.kind == "string":
        return "string"
    if tag.kind == "list":
        return _js_type_hint(tag.element) + "[]"
    return "*"


def generate_javascript_starter(function_name: str, param_names: list[str], param_tags: list[TypeTag], return_tag: TypeTag, io_transform: dict | None) -> str:
    io_transform = io_transform or {}
    needs_list_node = any(t.kind == "linked_list" for t in param_tags) or return_tag.kind == "linked_list"
    needs_tree_node = any(t.kind == "binary_tree" for t in param_tags) or return_tag.kind == "binary_tree"
    lines = []
    if needs_list_node:
        lines.append("// A ListNode class is provided: function ListNode(val, next) { this.val = val; this.next = (next === undefined ? null : next); }")
    if needs_tree_node:
        lines.append("// A TreeNode class is provided: function TreeNode(val, left, right) { this.val = val; this.left = (left === undefined ? null : left); this.right = (right === undefined ? null : right); }")
    lines.append("/**")
    for name, tag in zip(param_names, param_tags):
        lines.append(f" * @param {{{_js_type_hint(tag)}}} {name}")
    lines.append(f" * @return {{{_js_type_hint(return_tag)}}}")
    lines.append(" */")
    args_str = ", ".join(param_names)
    lines.append(f"function {to_camel_case(function_name)}({args_str}) {{")
    lines.append("    ")
    lines.append("}")
    return "\n".join(lines) + "\n"


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
            # `tag` (the full, possibly multi-level list) is passed here, not
            # `inner` -- see java_sandbox.py's identical helper for why passing
            # `inner` double-counts a nesting level.
            return _java_boxed_list_type(tag)
        return "Object[]"
    return "Object"


_SCALAR_BOXED = {"int": "Integer", "double": "Double", "bool": "Boolean", "string": "String"}


def _java_boxed_list_type(tag: TypeTag) -> str:
    """Java generic List<...> type for a value of exactly this list shape --
    kept in sync with java_sandbox.py's _boxed_generic_type, which the actual
    sandbox harness uses; this copy only affects the starter code text shown
    to the learner, so the two must agree or the shown signature would lie
    about what the harness actually calls."""
    inner = tag.element
    if inner.kind == "list":
        return f"List<{_java_boxed_list_type(inner)}>"
    return f"List<{_SCALAR_BOXED.get(inner.kind, 'Object')}>"


def generate_java_starter(function_name: str, param_names: list[str], param_tags: list[TypeTag], return_tag: TypeTag) -> str:
    params = ", ".join(f"{_java_type(t)} {n}" for t, n in zip(param_tags, param_names))
    return_java = _java_type(return_tag)
    comment = (
        "// Implement solve() inside this Solution class -- do not add a package or import\n"
        "// statement, and do not mark the class public. ListNode / TreeNode (if this problem\n"
        "// needs them) are already defined for you and can be used directly.\n"
    )
    return f"{comment}class Solution {{\n    public {return_java} {to_camel_case(function_name)}({params}) {{\n        \n    }}\n}}\n"
