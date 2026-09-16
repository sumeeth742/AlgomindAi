"""
Empirical time-complexity verification.

The existing brute-force nudge (diagnosis/engine.py's detect_brute_force) is
purely static: it counts nested loops. That's cheap and catches the common
case, but it's also easy to fool (e.g. two sequential loops instead of nested
ones can still be O(n^2) via repeated linear scans) and can't see anything
beyond loop *shape*. This module is a dynamic complement: it actually re-runs
the user's own passing solution against several progressively larger,
synthetically generated inputs of the same shape as the problem's real test
data, measures real wall-clock time for each, and fits how the time scales
with size. Nothing here is a canned or invented result -- every timing is a
real subprocess execution, and the "estimated complexity" is a plain log-log
growth-rate calculation over those real numbers, shown alongside the raw
samples so the estimate is never presented as more certain than it is.

Scope, stated honestly rather than silently: this only attempts problems
whose primary scaling dimension is a single flat list/string argument, or a
single scalar integer argument (e.g. factorial(n), count_primes(n)). Problems
needing scaled trees, linked lists, 2D grids, or multiple independently-sized
arguments are declined rather than given a fabricated or misleading probe --
building a correct synthetic generator for those shapes is real, separate
work. It also only runs for Python and JavaScript: Java's per-run compilation
cost (a fresh `javac` per submission, by design -- see java_sandbox.py) makes
four repeated timing runs impractically slow without a dedicated
multi-size-in-one-compile harness, which doesn't exist yet.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field

from app.services.execution.sandbox import run_submission
from app.services.execution.type_inference import TypeTag

SUPPORTED_LANGUAGES = ("python", "javascript")

# Roughly x4 per step -- enough spacing for the log-log growth rate to be
# meaningfully distinguishable from timing noise, without needing enormous
# inputs. Sizes may exceed a problem's stated constraints on purpose: judging
# asymptotic behavior requires observing growth past the range a problem
# guarantees a fast solution even matters for. The max (6400) was picked by
# actually timing a true (no-early-exit) O(n^2) Python loop at that size --
# it took ~2s, comfortably inside the per-run timeout with margin, so a
# quadratic solution gets a real, finished measurement instead of an
# uninformative timeout at the very size that would most clearly show it.
PROBE_SIZES = (100, 400, 1600, 6400)
# A single integer *value* (e.g. factorial(n), naive recursive fibonacci(n))
# is a completely different scale from an array/string *length* -- n=6400 is
# trivial for an array-length problem but recursive-fibonacci(6400) would
# never finish in this universe. Verified by timing naive recursive fib
# directly: fib(37) took ~2.6s, comfortably inside the per-run timeout, while
# still being large enough to show real exponential blowup if present.
SCALAR_PROBE_SIZES = (10, 20, 30, 37)
PROBE_TIMEOUT_SECONDS = 5.0
BASELINE_SIZE = 5  # a near-trivial run, used only to estimate fixed subprocess/startup overhead

# exponent-of-n this problem's stated expected_complexity implies, for
# comparison against the measured exponent. O(2^n)/O(n!) have no finite
# polynomial exponent -- they're handled separately (a timeout there is
# expected, not a red flag).
COMPLEXITY_EXPONENT = {
    "O(1)": 0.0, "O(log n)": 0.15, "O(n)": 1.0, "O(n log n)": 1.15,
    "O(n^2)": 2.0, "O(n^3)": 3.0,
}
EXPONENTIAL_LABELS = {"O(2^n)", "O(n!)"}


@dataclass
class ComplexitySample:
    size: int
    status: str
    runtime_ms: float | None = None


@dataclass
class ComplexityReport:
    supported: bool
    reason: str | None = None
    samples: list[ComplexitySample] = field(default_factory=list)
    estimated_exponent: float | None = None
    estimated_label: str | None = None
    likely_matches_expected: bool | None = None
    explanation: str = ""


def _find_scaling_arg(param_tags: list[TypeTag], io_transform: dict | None):
    """Returns (index, kind) for the one argument to scale, or None if this
    problem's shape isn't one this module knows how to scale synthetically."""
    io_transform = io_transform or {}
    if io_transform.get("args") or io_transform.get("result"):
        return None  # tree/linked-list structures -- not attempted here

    list_candidates = [i for i, t in enumerate(param_tags) if t.kind == "list" and t.element is not None and t.element.kind in ("int", "double")]
    string_candidates = [i for i, t in enumerate(param_tags) if t.kind == "string"]
    if list_candidates:
        return list_candidates[0], "int_list"
    if string_candidates:
        return string_candidates[0], "string"
    if len(param_tags) == 1 and param_tags[0].kind == "int":
        return 0, "scalar_int"
    return None


def _build_args_at_size(base_args: list, scaling_index: int, kind: str, size: int, is_float: bool) -> list:
    """Values are deliberately unique and drawn from a wide range, not
    resampled from the problem's own (usually tiny) real test data. Reusing
    real values was tried first and produced a real, confirmed bug: a small
    pool of repeated small numbers makes an accidental match (e.g. two values
    summing to `target`) astronomically likely within the first few elements
    of a large synthetic array, so a search-and-return-early algorithm exits
    almost immediately regardless of true array size -- brute-force and
    optimal solutions both measured as flat, indistinguishable "O(1)". Wide,
    unique, effectively-random values make an accidental early match
    negligible, forcing the near-worst-case traversal that's actually needed
    to observe true scaling."""
    args = list(base_args)
    if kind == "int_list":
        # Range must be wide relative to size^2, not just size: with n values,
        # there are ~n^2/2 pairs, so even a "wide-looking" range like +-5M
        # still makes a coincidental pairwise-sum match likely once n reaches
        # the tens of thousands (confirmed by testing -- it was silently
        # giving brute-force two-sum an early exit almost as fast as the
        # hashmap version, hiding the real O(n^2) behavior entirely). +-10^12
        # keeps expected accidental matches for any two elements well under
        # 1 even at the largest probed size, while staying far inside every
        # supported language's safe integer range.
        values = random.sample(range(-10**12, 10**12), size)
        args[scaling_index] = [v / 1000.0 for v in values] if is_float else values
    elif kind == "string":
        # All-unique characters, not independently random ones -- confirmed
        # by testing to matter exactly like the int case above: an algorithm
        # like "longest substring without repeating characters" that breaks
        # its inner loop on the first repeat will, on a small alphabet, hit a
        # repeat almost immediately (the birthday paradox: even a ~55,000-size
        # alphabet only takes a run of a few hundred characters before a
        # collision is likely), so a brute-force O(n^2) solution's inner loop
        # kept exiting early and measured as flat "O(1)" just like the
        # two-sum case did. Sampling unique code points (never repeating any
        # character across the whole string) removes any repeat for the
        # algorithm to find, forcing the real worst-case traversal.
        codepoints = random.sample(range(0x21, 0xD7FF), size)  # avoids the UTF-16 surrogate range
        args[scaling_index] = "".join(chr(c) for c in codepoints)
    elif kind == "scalar_int":
        args[scaling_index] = size
    return args


def measure_empirical_complexity(
    code: str, function_name: str, language: str,
    test_case_args: list[list], param_tags: list[TypeTag], io_transform: dict | None,
    expected_complexity: str,
) -> ComplexityReport:
    if language not in SUPPORTED_LANGUAGES:
        return ComplexityReport(supported=False, reason=f"Empirical complexity checking isn't available for {language} yet -- see this module's docstring for why.")
    if not test_case_args:
        return ComplexityReport(supported=False, reason="No test cases to base a synthetic scaling shape on.")

    found = _find_scaling_arg(param_tags, io_transform)
    if found is None:
        return ComplexityReport(
            supported=False,
            reason="This problem's inputs aren't a shape this checker knows how to scale synthetically "
                   "(e.g. a tree, a grid, or several independently-sized arguments) -- rather than guess, it's skipped.",
        )
    scaling_index, kind = found
    is_float = kind == "int_list" and param_tags[scaling_index].element.kind == "double"

    base_args = max(test_case_args, key=lambda a: len(a[scaling_index]) if isinstance(a[scaling_index], (list, str)) else abs(a[scaling_index]))

    # A near-trivial run first, to measure this machine's real fixed
    # subprocess-launch overhead -- at the smallest probe sizes, that fixed
    # cost otherwise dwarfs the actual algorithmic work being measured and
    # flattens the growth curve toward "looks like O(1)" regardless of the
    # true complexity. This is a real, measured baseline, not an assumed
    # constant, and it's disclosed in the explanation rather than silently
    # hidden.
    baseline_args = _build_args_at_size(base_args, scaling_index, kind, BASELINE_SIZE, is_float)
    baseline_result = run_submission(code, function_name, [baseline_args], io_transform, language=language)
    baseline_ms = baseline_result.runtime_ms if baseline_result.status == "EXECUTED" else 0.0

    sizes = SCALAR_PROBE_SIZES if kind == "scalar_int" else PROBE_SIZES
    samples: list[ComplexitySample] = []
    for size in sizes:
        args = _build_args_at_size(base_args, scaling_index, kind, size, is_float)
        result = run_submission(code, function_name, [args], io_transform, language=language)
        if result.status != "EXECUTED":
            samples.append(ComplexitySample(size=size, status=result.status))
            break  # a timeout/error at this size means larger sizes will only be worse -- stop probing
        samples.append(ComplexitySample(size=size, status="EXECUTED", runtime_ms=result.runtime_ms))

    return _fit_report(samples, expected_complexity, baseline_ms)


def _fit_report(samples: list[ComplexitySample], expected_complexity: str, baseline_ms: float) -> ComplexityReport:
    executed = [s for s in samples if s.status == "EXECUTED"]
    saw_failure = len(executed) < len(samples)

    if len(executed) < 2:
        return ComplexityReport(
            supported=True, samples=samples,
            explanation="Not enough completed runs to estimate a growth rate -- "
                         + ("the very first, smallest input already timed out or errored, which on its own suggests something is badly wrong well before this problem's real scale." if not executed else "only one input size finished before a timeout/error."),
        )

    import math
    # Subtract the measured fixed overhead before computing ratios (floored
    # so a size that happened to measure at or below the baseline doesn't
    # produce a zero/negative time and break the log) -- see baseline_ms's
    # computation above for why this matters.
    net_times = [max(s.runtime_ms - baseline_ms, 0.05) for s in executed]
    exponents = []
    for (a, t_a), (b, t_b) in zip(zip(executed, net_times), zip(executed[1:], net_times[1:])):
        size_ratio = b.size / a.size
        time_ratio = t_b / t_a
        exponents.append(math.log(time_ratio) / math.log(size_ratio))
    exponent = sum(exponents) / len(exponents) if exponents else None
    # Polynomial growth gives a roughly constant exponent between consecutive
    # pairs; growth that's accelerating (each pair's exponent bigger than the
    # last) is the actual signature of exponential-or-worse blowup -- a
    # timeout alone doesn't distinguish "genuinely exponential" from
    # "polynomial but with a size where it's just slow", so both signals are
    # used together rather than treating any timeout as automatically
    # exponential.
    accelerating = len(exponents) >= 2 and exponents[-1] - exponents[0] > 1.0

    label = _bucket_label(exponent, saw_failure, accelerating)
    matches = _matches_expected(exponent, saw_failure, accelerating, expected_complexity)

    explanation = (
        f"Measured real runtime at sizes {', '.join(str(s.size) for s in samples)} "
        f"({', '.join(f'{s.runtime_ms:.1f}ms' if s.runtime_ms is not None else s.status for s in samples)}), "
        f"with a measured baseline (subprocess-launch) overhead of {baseline_ms:.1f}ms subtracted out before "
        f"fitting the growth rate. "
    )
    if exponent is not None:
        explanation += f"Estimated growth rate: roughly n^{exponent:.2f} -- closest to {label}. "
    else:
        explanation += f"Growth pattern: {label}. "
    if saw_failure:
        explanation += "A run timed out or errored before completing at a larger size, which is itself evidence of poor scaling regardless of the exact label. "
    explanation += (
        "This is a real measurement, not a formal proof -- timing has noise, and O(n) vs O(n log n) in "
        "particular can't be reliably told apart at these practical sizes, so treat the label as an "
        "approximate bucket, not a certificate."
    )

    return ComplexityReport(
        supported=True, samples=samples, estimated_exponent=exponent, estimated_label=label,
        likely_matches_expected=matches, explanation=explanation,
    )


def _bucket_label(exponent: float | None, saw_failure: bool, accelerating: bool) -> str:
    if exponent is None and saw_failure:
        return "very poor scaling (timed out before even two sizes could be compared)"
    if exponent is None:
        return "inconclusive"
    if saw_failure and accelerating:
        return "exponential-or-worse (growth kept accelerating, then a run timed out)"
    suffix = " -- and got too slow to finish at an even larger size, consistent with this same rate" if saw_failure else ""
    if exponent < 0.4:
        return "O(1) / O(log n) (near-constant growth)" + suffix
    if exponent < 0.75:
        return "O(log n) (sub-linear growth)" + suffix
    if exponent < 1.35:
        return "O(n) or O(n log n) (roughly linear growth)" + suffix
    if exponent < 1.75:
        return "between O(n log n) and O(n^2) (super-linear growth)" + suffix
    if exponent < 2.5:
        return "O(n^2) (quadratic-ish growth)" + suffix
    if exponent < 3.5:
        return "O(n^3) (cubic-ish growth)" + suffix
    return "a high-degree polynomial, or worse" + suffix


def _matches_expected(exponent: float | None, saw_failure: bool, accelerating: bool, expected_complexity: str) -> bool | None:
    if expected_complexity in EXPONENTIAL_LABELS:
        return None  # blowing up here is expected, not a red flag -- nothing useful to compare
    expected_exponent = COMPLEXITY_EXPONENT.get(expected_complexity)
    if expected_exponent is None:
        return None
    if saw_failure:
        # A timeout at these deliberately-conservative sizes (max array length
        # 6400, max recursion input 37 -- both individually verified to finish
        # a true O(n^2) or exponential run within a few seconds) is on its own
        # sufficient evidence against any "fast" expected complexity. This is
        # intentionally NOT gated on the (noisy, only 2-3 points) accelerating
        # trend -- that trend is used only to pick which label text to show,
        # not whether a timeout counts as a mismatch, since a stray negative
        # exponent from measurement noise between two small, fast runs could
        # otherwise mask a real timeout as "probably fine".
        return False
    if exponent is None:
        return None
    # Generous margin -- this is a noisy empirical estimate, so only flag a
    # clear, unambiguous overshoot rather than anything close to the line.
    return exponent <= expected_exponent + 0.6
