"""
Java counterpart to features.py's Python `ast`-based static analysis.

Same honesty principle: every feature is computed from a real parse of the
submitted Java source (via the `javalang` library, a real Java-grammar
parser, not a regex approximation), never guessed. The exact feature
definitions deliberately mirror features.py's Python heuristics (e.g. "two
index-like variable names used as array subscripts" is still just a naming
heuristic there too) so a submission's diagnosis doesn't quietly get more or
less scrutiny just because of the language it was written in.
"""
from __future__ import annotations

import javalang

from app.services.diagnosis.features import CodeFeatures, name_matches_heap_vocabulary

LOOP_TYPES = (javalang.tree.ForStatement, javalang.tree.WhileStatement, javalang.tree.DoStatement)
COMMON_PAIR_NAMES = {"left", "right", "l", "r", "i", "j", "lo", "hi", "start", "end"}
DICT_OR_SET_TYPES = {"HashMap", "HashSet", "TreeMap", "TreeSet", "LinkedHashMap", "LinkedHashSet"}
HEAP_TYPES = {"PriorityQueue"}
SORT_METHOD_NAMES = {"sort"}


def analyze_java_code(code: str, function_name: str) -> CodeFeatures:
    try:
        tree = javalang.parse.parse(code)
    except (javalang.parser.JavaSyntaxError, javalang.tokenizer.LexerError, IndexError):
        return CodeFeatures(0, 0, False, False, False, False, False, False, True)

    loc = len(code.splitlines())
    # Only recursion detection is scoped to the specific method (a call to
    # `function_name` from some unrelated helper wouldn't be recursion) --
    # every other feature scans the whole file, same as the Python analyzer,
    # so a heap/HashMap/etc. defined in a helper method or nested class still
    # counts instead of being invisible just because it isn't inlined into
    # the one method the harness calls.
    method = _find_method(tree, function_name)
    recursion_scope = method if method is not None else tree

    return CodeFeatures(
        loc=loc,
        max_loop_nesting=_max_loop_nesting(tree),
        uses_recursion=_uses_recursion(recursion_scope, function_name),
        uses_dict_or_set=_uses_class_creator(tree, DICT_OR_SET_TYPES),
        uses_two_index_vars=_uses_two_index_vars(tree),
        uses_sorted_or_sort=_uses_method_calls(tree, SORT_METHOD_NAMES),
        uses_heap=_uses_class_creator(tree, HEAP_TYPES) or _uses_heap_vocabulary(tree),
        has_early_return_in_loop=_has_return_inside_loop(tree),
        parse_error=False,
    )


def _find_method(tree, function_name: str):
    for _, node in tree:
        if isinstance(node, javalang.tree.MethodDeclaration) and node.name == function_name:
            return node
    return None


def _max_loop_nesting(scope) -> int:
    best = 0
    for path, node in scope:
        if isinstance(node, LOOP_TYPES):
            depth = 1 + sum(1 for p in path if isinstance(p, LOOP_TYPES))
            best = max(best, depth)
    return best


def _uses_recursion(scope, function_name: str) -> bool:
    for _, node in scope:
        if isinstance(node, javalang.tree.MethodInvocation) and node.member == function_name:
            return True
    return False


def _uses_class_creator(scope, type_names: set[str]) -> bool:
    for _, node in scope:
        if isinstance(node, javalang.tree.ClassCreator) and getattr(node.type, "name", None) in type_names:
            return True
        if isinstance(node, javalang.tree.ReferenceType) and node.name in type_names:
            return True
    return False


def _uses_method_calls(scope, method_names: set[str]) -> bool:
    for _, node in scope:
        if isinstance(node, javalang.tree.MethodInvocation) and node.member in method_names:
            return True
    return False


def _uses_two_index_vars(scope) -> bool:
    """Same naming heuristic as the Python version: are (at least) two
    common index-variable names both used as array subscripts?"""
    subscript_names = set()
    for _, node in scope:
        if isinstance(node, javalang.tree.MemberReference) and node.selectors:
            for sel in node.selectors:
                if isinstance(sel, javalang.tree.ArraySelector) and isinstance(sel.index, javalang.tree.MemberReference):
                    subscript_names.add(sel.index.member)
    return len(subscript_names & COMMON_PAIR_NAMES) >= 2


def _uses_heap_vocabulary(scope) -> bool:
    for _, node in scope:
        for attr in ("name", "member"):
            value = getattr(node, attr, None)
            if isinstance(value, str) and name_matches_heap_vocabulary(value):
                return True
    return False


def _has_return_inside_loop(scope) -> bool:
    for _, node in scope:
        if isinstance(node, LOOP_TYPES):
            for _, inner in node:
                if isinstance(inner, javalang.tree.ReturnStatement):
                    return True
    return False
