"""
Shared real-content extraction: pulls a lesson's own "## Key Takeaway" section
verbatim out of its markdown (falling back to "## What is it?", then a plain
prefix of the raw text). Used by both the Explain-It-Back scorer (to know what
vocabulary a student's explanation should cover) and the Printable Study
Cheat Sheet (to show the same real takeaway as a compact study line) -- one
implementation, so the two features can never quietly disagree about what a
lesson's key idea is.
"""
from __future__ import annotations

import re


def extract_key_takeaway(markdown: str) -> str:
    match = re.search(r"##\s*key takeaway\s*\n(.+?)(?=\n##|\Z)", markdown, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()
    match = re.search(r"##\s*what is it\??\s*\n(.+?)(?=\n##|\Z)", markdown, re.IGNORECASE | re.DOTALL)
    return match.group(1).strip() if match else markdown[:400]
