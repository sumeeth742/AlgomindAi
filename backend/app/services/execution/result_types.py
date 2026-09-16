"""Execution result types shared by every language's sandbox runner, so the
router and comparison logic can treat Python/JavaScript/Java results
identically regardless of which subprocess actually produced them."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TestOutcome:
    kind: str  # "ok" | "runtime_error"
    value: object = None
    message: str | None = None


@dataclass
class ExecutionResult:
    status: str  # EXECUTED | TIMEOUT | RUNTIME_ERROR | COMPILE_ERROR
    runtime_ms: float
    outcomes: list[TestOutcome] = field(default_factory=list)
    error_message: str | None = None
