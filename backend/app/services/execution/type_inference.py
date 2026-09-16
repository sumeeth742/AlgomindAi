"""
Shape/type inference used to generate per-language starter code and (for
statically-typed languages) sandbox harnesses.

Problems are authored once, dynamically, in Python. To offer the same problem
in a statically-typed language like Java we need a real type for every
argument and the return value -- there is no per-language type annotation
stored anywhere, so it is inferred here from the actual JSON shape of a
problem's own test-case data (which was itself produced by executing the
reference solution, never invented). This keeps "every fact must be real"
intact: nothing about a problem's shape is guessed independently of its data.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TypeTag:
    kind: str  # "int" | "double" | "bool" | "string" | "list" | "null" | "unknown"
    element: "TypeTag | None" = None  # for kind == "list"


def infer_tag(value) -> TypeTag:
    if isinstance(value, bool):
        return TypeTag("bool")
    if isinstance(value, int):
        return TypeTag("int")
    if isinstance(value, float):
        return TypeTag("double")
    if isinstance(value, str):
        return TypeTag("string")
    if value is None:
        return TypeTag("null")
    if isinstance(value, list):
        if not value:
            # Element type is genuinely unknown from this sample alone -- `None`
            # means "defer to whatever a sibling sample's non-empty list says",
            # rather than guessing a depth here that a merge could never undo
            # (an empty list at the outer level looks identical whether the true
            # element type is int or list-of-int, so guessing either one is
            # wrong exactly half the time; deferring is the only safe choice).
            return TypeTag("list", None)
        element_tags = [infer_tag(v) for v in value if v is not None]
        if not element_tags:
            return TypeTag("list", None)
        merged = element_tags[0]
        for t in element_tags[1:]:
            merged = _merge(merged, t)
        return TypeTag("list", merged)
    return TypeTag("unknown")


def _merge(a: TypeTag, b: TypeTag) -> TypeTag:
    if a.kind == "list" and b.kind == "list":
        if a.element is None:
            return b
        if b.element is None:
            return a
        return TypeTag("list", _merge(a.element, b.element))
    if a.kind == b.kind:
        return a
    if {a.kind, b.kind} == {"int", "double"}:
        return TypeTag("double")
    return a  # divergent element types shouldn't occur in well-formed test data


def _resolve_unknown_depth(tag: TypeTag) -> TypeTag:
    """After merging, a list whose element is still `None` means every sample
    of it was empty -- there is no data anywhere to infer a depth from, so it
    falls back to a flat list of ints (the most common shape) as a last resort."""
    if tag.kind == "list":
        return TypeTag("list", _resolve_unknown_depth(tag.element) if tag.element is not None else TypeTag("int"))
    return tag


def merge_across_samples(values: list) -> TypeTag:
    """Infer one consistent tag for an argument (or the return value) across
    every sample seen for it, e.g. every test case's value at that position."""
    tags = [infer_tag(v) for v in values]
    merged = tags[0]
    for t in tags[1:]:
        merged = _merge(merged, t)
    return _resolve_unknown_depth(merged)
