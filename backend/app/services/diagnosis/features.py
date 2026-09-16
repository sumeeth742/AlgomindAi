"""
Deterministic, evidence-producing static analysis of a submission.

Nothing here is invented: every value is either directly observed (execution
status, timing, hint count) or computed from the submitted source via Python's
own `ast` module. This is the evidence the diagnosis model and the rule layer
are allowed to cite (spec section 50: "Never invent evidence").
"""
from __future__ import annotations

import ast
from dataclasses import dataclass, asdict


# Some languages have no built-in heap/priority-queue type (JavaScript has
# neither a stdlib one nor one reachable from the sandbox, which disables
# `require` entirely), so a correct solution there is necessarily a hand-rolled
# heap. Detecting "import heapq" / "new PriorityQueue()" alone would silently
# never credit that hand-rolled implementation as heap usage in any language --
# this vocabulary check (shared by features.py, features_java.py, and
# features_js.py) fills that gap by recognizing a heap's characteristic naming
# (heapify, sift-up/down, bubble-up/down, percolate-up/down, MinHeap/MaxHeap)
# regardless of language. Like the two-index-variable heuristic below, this is
# a naming heuristic, not a semantic guarantee -- it can miss an oddly-named
# implementation, but it never claims something that isn't there.
HEAP_KEYWORDS = ("heap", "siftup", "siftdown", "bubbleup", "bubbledown", "percolateup", "percolatedown", "priorityqueue")


def name_matches_heap_vocabulary(name: str | None) -> bool:
    if not name:
        return False
    cleaned = name.lower().replace("_", "")
    return any(kw in cleaned for kw in HEAP_KEYWORDS)


@dataclass
class CodeFeatures:
    loc: int
    max_loop_nesting: int
    uses_recursion: bool
    uses_dict_or_set: bool
    uses_two_index_vars: bool
    uses_sorted_or_sort: bool
    uses_heap: bool
    has_early_return_in_loop: bool
    parse_error: bool


def analyze_code(code: str, function_name: str) -> CodeFeatures:
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return CodeFeatures(0, 0, False, False, False, False, False, False, True)

    loc = len(code.splitlines())
    max_nesting = _max_loop_nesting(tree)
    uses_recursion = _uses_recursion(tree, function_name)
    uses_dict_or_set = _uses_names(tree, {"dict", "set"}) or _has_dict_or_set_literal(tree)
    uses_two_index = _uses_two_index_vars(tree)
    uses_sorted = _uses_calls(tree, {"sorted"}) or _uses_attr_calls(tree, {"sort"})
    uses_heap = _uses_module(tree, "heapq") or _uses_heap_vocabulary(tree)
    has_early_return = _has_return_inside_loop(tree)

    return CodeFeatures(
        loc=loc,
        max_loop_nesting=max_nesting,
        uses_recursion=uses_recursion,
        uses_dict_or_set=uses_dict_or_set,
        uses_two_index_vars=uses_two_index,
        uses_sorted_or_sort=uses_sorted,
        uses_heap=uses_heap,
        has_early_return_in_loop=has_early_return,
        parse_error=False,
    )


def _max_loop_nesting(tree: ast.AST) -> int:
    best = 0

    def walk(node, depth):
        nonlocal best
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.For, ast.While)):
                best = max(best, depth + 1)
                walk(child, depth + 1)
            else:
                walk(child, depth)

    walk(tree, 0)
    return best


def _uses_recursion(tree: ast.AST, function_name: str) -> bool:
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            for inner in ast.walk(node):
                if isinstance(inner, ast.Call) and isinstance(inner.func, ast.Name):
                    if inner.func.id == function_name:
                        return True
    return False


def _uses_names(tree: ast.AST, names: set[str]) -> bool:
    return any(isinstance(n, ast.Name) and n.id in names for n in ast.walk(tree))


def _has_dict_or_set_literal(tree: ast.AST) -> bool:
    return any(isinstance(n, (ast.Dict, ast.Set)) for n in ast.walk(tree))


def _uses_calls(tree: ast.AST, names: set[str]) -> bool:
    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in names:
            return True
    return False


def _uses_attr_calls(tree: ast.AST, attrs: set[str]) -> bool:
    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr in attrs:
            return True
    return False


def _uses_module(tree: ast.AST, module: str) -> bool:
    for n in ast.walk(tree):
        if isinstance(n, ast.Import) and any(a.name == module for a in n.names):
            return True
        if isinstance(n, ast.ImportFrom) and n.module == module:
            return True
    return False


def _uses_heap_vocabulary(tree: ast.AST) -> bool:
    for n in ast.walk(tree):
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and name_matches_heap_vocabulary(n.name):
            return True
        if isinstance(n, ast.Name) and name_matches_heap_vocabulary(n.id):
            return True
        if isinstance(n, ast.Attribute) and name_matches_heap_vocabulary(n.attr):
            return True
    return False


def _uses_two_index_vars(tree: ast.AST) -> bool:
    """Heuristic: two int variables both used as list subscripts, e.g. left/right, i/j."""
    subscript_names = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Subscript) and isinstance(n.slice, ast.Name):
            subscript_names.add(n.slice.id)
        elif isinstance(n, ast.Subscript) and isinstance(getattr(n, "value", None), ast.Name):
            pass
    common_pair_names = {"left", "right", "l", "r", "i", "j", "lo", "hi", "start", "end"}
    return len(subscript_names & common_pair_names) >= 2


def _has_return_inside_loop(tree: ast.AST) -> bool:
    for n in ast.walk(tree):
        if isinstance(n, (ast.For, ast.While)):
            for inner in ast.walk(n):
                if isinstance(inner, ast.Return):
                    return True
    return False


def features_to_vector(cf: CodeFeatures) -> list[float]:
    """Fixed-order numeric encoding consumed by the scikit-learn model."""
    return [
        float(cf.loc),
        float(cf.max_loop_nesting),
        float(cf.uses_recursion),
        float(cf.uses_dict_or_set),
        float(cf.uses_two_index_vars),
        float(cf.uses_sorted_or_sort),
        float(cf.uses_heap),
        float(cf.has_early_return_in_loop),
    ]


FEATURE_NAMES = [
    "loc", "max_loop_nesting", "uses_recursion", "uses_dict_or_set",
    "uses_two_index_vars", "uses_sorted_or_sort", "uses_heap", "has_early_return_in_loop",
]
