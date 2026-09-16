"""
JavaScript counterpart to features.py's Python `ast`-based static analysis.

The submitted JavaScript is parsed into a real ESTree AST by `espree` (the
same parser ESLint itself uses -- see js_analyzer/parse.js), not approximated
with regexes. The AST comes back as JSON and is walked here in Python so the
feature *definitions* stay in one place rather than being re-implemented
separately per language; only the parsing step is language-specific.

Feature definitions deliberately mirror features.py's Python heuristics
(including their imprecision -- e.g. "two index-like variable names used as
array subscripts" is a naming heuristic there too) so a submission isn't
scored more or less strictly just because of the language it was written in.
Vanilla JavaScript has no built-in heap/priority-queue type, and the sandbox
disables `require` entirely, so a correct JS solution needing a heap is
necessarily hand-rolled. `uses_heap` therefore can't look for an import or a
`new PriorityQueue()` the way Python/Java can -- instead it recognizes a
heap's characteristic naming (heapify, sift-up/down, bubble-up/down,
percolate-up/down, MinHeap/MaxHeap), via the same vocabulary check
features.py and features_java.py use. This is a naming heuristic, not proof
of a real heap -- it can miss an oddly-named implementation -- but it's the
same kind of heuristic `uses_two_index_vars` already relies on, so it doesn't
hold JS to a different evidentiary standard than the other two languages.
"""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

from app.services.diagnosis.features import CodeFeatures, name_matches_heap_vocabulary

LOOP_TYPES = {"ForStatement", "WhileStatement", "DoWhileStatement", "ForInStatement", "ForOfStatement"}
COMMON_PAIR_NAMES = {"left", "right", "l", "r", "i", "j", "lo", "hi", "start", "end"}
DICT_OR_SET_CTORS = {"Map", "Set"}

_PARSE_SCRIPT = Path(__file__).parent / "js_analyzer" / "parse.js"


def analyze_js_code(code: str, function_name: str) -> CodeFeatures:
    payload = _parse_js(code)
    if payload is None or not payload.get("ok"):
        return CodeFeatures(0, 0, False, False, False, False, False, False, True)

    root = payload["ast"]
    loc = len(code.splitlines())
    # Only recursion detection is scoped to the specific function -- every
    # other feature scans the whole file, same as the Python analyzer, so a
    # heap/Map/etc. defined in a helper function or class still counts
    # instead of being invisible just because it isn't inlined into the one
    # function the harness calls.
    recursion_scope = _find_function(root, function_name) or root

    return CodeFeatures(
        loc=loc,
        max_loop_nesting=_max_loop_nesting(root),
        uses_recursion=_uses_recursion(recursion_scope, function_name),
        uses_dict_or_set=_uses_dict_or_set(root),
        uses_two_index_vars=_uses_two_index_vars(root),
        uses_sorted_or_sort=_uses_sort_calls(root),
        uses_heap=_uses_heap_vocabulary(root),
        has_early_return_in_loop=_has_return_inside_loop(root),
        parse_error=False,
    )


def _parse_js(code: str) -> dict | None:
    node = shutil.which("node")
    if node is None or not _PARSE_SCRIPT.exists():
        return None
    try:
        proc = subprocess.run(
            [node, str(_PARSE_SCRIPT)],
            input=json.dumps(code), capture_output=True, text=True, timeout=10,
            cwd=str(_PARSE_SCRIPT.parent),
        )
    except subprocess.TimeoutExpired:
        return None
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return None


def _iter_nodes(node, path: tuple = ()):
    """Yields (ancestor_path, node) for every real ESTree node (any dict
    carrying a "type" field) found anywhere under `node`, recursing through
    both dict values and lists."""
    if isinstance(node, dict):
        is_node = "type" in node
        if is_node:
            yield path, node
        new_path = path + (node,) if is_node else path
        for key, value in node.items():
            if key == "type":
                continue
            yield from _iter_nodes(value, new_path)
    elif isinstance(node, list):
        for item in node:
            yield from _iter_nodes(item, path)


def _find_function(root, function_name: str):
    for _, node in _iter_nodes(root):
        if node.get("type") == "FunctionDeclaration" and (node.get("id") or {}).get("name") == function_name:
            return node
        if node.get("type") == "VariableDeclarator" and (node.get("id") or {}).get("name") == function_name:
            init = node.get("init") or {}
            if init.get("type") in ("ArrowFunctionExpression", "FunctionExpression"):
                return init
    return None


def _max_loop_nesting(scope) -> int:
    best = 0
    for path, node in _iter_nodes(scope):
        if node.get("type") in LOOP_TYPES:
            depth = 1 + sum(1 for p in path if p.get("type") in LOOP_TYPES)
            best = max(best, depth)
    return best


def _uses_recursion(scope, function_name: str) -> bool:
    for _, node in _iter_nodes(scope):
        if node.get("type") == "CallExpression":
            callee = node.get("callee") or {}
            if callee.get("type") == "Identifier" and callee.get("name") == function_name:
                return True
    return False


def _uses_dict_or_set(scope) -> bool:
    for _, node in _iter_nodes(scope):
        if node.get("type") == "NewExpression":
            callee = node.get("callee") or {}
            if callee.get("type") == "Identifier" and callee.get("name") in DICT_OR_SET_CTORS:
                return True
        if node.get("type") == "ObjectExpression":
            return True
    return False


def _uses_two_index_vars(scope) -> bool:
    subscript_names = set()
    for _, node in _iter_nodes(scope):
        if node.get("type") == "MemberExpression" and node.get("computed"):
            prop = node.get("property") or {}
            if prop.get("type") == "Identifier":
                subscript_names.add(prop.get("name"))
    return len(subscript_names & COMMON_PAIR_NAMES) >= 2


def _uses_sort_calls(scope) -> bool:
    for _, node in _iter_nodes(scope):
        if node.get("type") == "CallExpression":
            callee = node.get("callee") or {}
            if callee.get("type") == "MemberExpression" and (callee.get("property") or {}).get("name") == "sort":
                return True
    return False


def _uses_heap_vocabulary(scope) -> bool:
    """Checks every Identifier node in scope -- this single node type covers
    function/class/variable names, object and class method names (when not
    computed), and non-computed member-expression properties (`.heapify()`),
    so it doesn't need to special-case each ESTree container separately."""
    for _, node in _iter_nodes(scope):
        if node.get("type") == "Identifier" and name_matches_heap_vocabulary(node.get("name")):
            return True
    return False


def _has_return_inside_loop(scope) -> bool:
    for _, node in _iter_nodes(scope):
        if node.get("type") in LOOP_TYPES:
            for _, inner in _iter_nodes(node):
                if inner.get("type") == "ReturnStatement":
                    return True
    return False
