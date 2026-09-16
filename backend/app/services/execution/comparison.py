"""Output comparison strategies (see Problem.output_comparison)."""


def _normalize_nested(value):
    if isinstance(value, list):
        return sorted(sorted(item) if isinstance(item, list) else item for item in value)
    return value


def outputs_match(actual, expected, mode: str = "exact") -> bool:
    if mode == "unordered_nested":
        try:
            return _normalize_nested(actual) == _normalize_nested(expected)
        except TypeError:
            return actual == expected
    return actual == expected
