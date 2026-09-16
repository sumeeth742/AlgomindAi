"""
Demo contests. Timestamps are computed relative to seed-time (not hardcoded
absolutes) so a freshly seeded database always has one contest in each real
state -- live, upcoming, ended -- rather than stale dates that immediately
read as fake. Re-running the seed skips any contest whose title already
exists (same idempotent pattern as every other seed file), so a contest
seeded as "live" naturally becomes "ended" as real time passes -- that's
correct, not a bug, since these are real timestamps checked against the real
clock, not a display value.
"""
from __future__ import annotations

from datetime import datetime, timedelta


def build_contests() -> list[dict]:
    now = datetime.utcnow()
    return [
        {
            "title": "Beginner Sprint",
            "start_at": now - timedelta(minutes=20),
            "end_at": now + timedelta(minutes=100),
            "problem_slugs": ["find-min-max", "two-sum-indices", "two-sum-sorted"],
        },
        {
            "title": "Weekly Mixed Challenge",
            "start_at": now + timedelta(days=3),
            "end_at": now + timedelta(days=3, hours=2),
            "problem_slugs": ["max-subarray-sum", "range-sum-queries", "count-anagram-groups", "edit-distance"],
        },
        {
            "title": "Foundations Cup",
            "start_at": now - timedelta(days=7, hours=2),
            "end_at": now - timedelta(days=7),
            "problem_slugs": ["two-sum-indices", "max-subarray-sum", "sliding-window-maximum"],
        },
    ]
