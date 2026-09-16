"""
Pure-Python linked-list / binary-tree <-> JSON conversions, used at SEED time
(normal in-process Python, to compute expected_output from a reference solution).

The sandbox runner (sandbox.py) needs the *same* conversions but runs in an
isolated subprocess that cannot import this package, so its RUNNER_TEMPLATE
embeds an equivalent copy inline. Keep the two in sync if you change either.
"""
from __future__ import annotations


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def build_linked_list(values: list):
    head = None
    tail = None
    for v in values:
        node = ListNode(v)
        if head is None:
            head = node
            tail = node
        else:
            tail.next = node
            tail = node
    return head


def linked_list_to_list(node) -> list:
    out = []
    seen = set()
    while node is not None and id(node) not in seen:
        seen.add(id(node))
        out.append(node.val)
        node = node.next
    return out


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(values: list):
    """LeetCode-style level-order list with `None` gaps, e.g. [3,9,20,None,None,15,7]."""
    values = list(values)
    if not values or values[0] is None:
        return None
    it = iter(values)
    root = TreeNode(next(it))
    queue = [root]
    while queue:
        node = queue.pop(0)
        try:
            lv = next(it)
        except StopIteration:
            break
        if lv is not None:
            node.left = TreeNode(lv)
            queue.append(node.left)
        try:
            rv = next(it)
        except StopIteration:
            break
        if rv is not None:
            node.right = TreeNode(rv)
            queue.append(node.right)
    return root


def tree_to_list(root) -> list:
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


def apply_arg_transforms(args: list, arg_transform_map: dict) -> list:
    args = list(args)
    for index_str, kind in (arg_transform_map or {}).items():
        i = int(index_str)
        if kind == "linked_list":
            args[i] = build_linked_list(args[i])
        elif kind == "binary_tree":
            args[i] = build_tree(args[i])
    return args


def apply_result_transform(result, kind: str | None):
    if kind == "linked_list":
        return linked_list_to_list(result)
    if kind == "binary_tree":
        return tree_to_list(result)
    return result
