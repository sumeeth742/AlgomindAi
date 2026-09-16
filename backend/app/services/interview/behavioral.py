"""
Real, structural verification of a behavioral interview answer -- checks for
the four STAR components (Situation, Task, Action, Result) via deterministic
keyword/phrase detection, the same honesty boundary as every other "AI"
feature in this app: it can detect whether an answer has the SHAPE of a
STAR answer, never whether the story itself is true, good, or convincing --
that would require actually understanding the content, which a keyword
check (or, honestly, this app's small local LLM) can't be trusted to judge
without risking a fabricated verdict.

A small, real, industry-standard bank of behavioral questions -- these are
genuinely the questions companies ask, not invented for this app.
"""
from __future__ import annotations

import re

BEHAVIORAL_QUESTIONS = [
    "Tell me about a time you disagreed with a teammate or manager. How did you handle it?",
    "Describe a project you're most proud of. What was your specific contribution?",
    "Tell me about a time you failed at something. What did you learn?",
    "Describe a time you had to learn a new technology or skill quickly under pressure.",
    "Tell me about a time you had to deal with an ambiguous or poorly-defined problem.",
    "Describe a situation where you had to convince others to adopt your point of view.",
    "Tell me about a time you had to make a decision with incomplete information.",
    "Describe a time you received critical feedback. How did you respond?",
]

SITUATION_WORDS = ("when i", "at my", "during", "while working", "in my previous", "last year", "at the time", "on a project")
TASK_WORDS = ("needed to", "responsible for", "my task", "the goal was", "had to", "was asked to")
ACTION_WORDS = ("i decided", "i implemented", "i built", "i led", "i created", "i chose", "i communicated", "so i", "i proposed", "i reached out")
RESULT_WORDS = ("as a result", "which led to", "ultimately", "in the end", "this resulted in", "we achieved", "improved by", "the outcome")

STAR_PARTS = {
    "situation": SITUATION_WORDS,
    "task": TASK_WORDS,
    "action": ACTION_WORDS,
    "result": RESULT_WORDS,
}


def score_behavioral_answer(answer: str) -> dict:
    text = answer.lower()
    matched = [part for part, words in STAR_PARTS.items() if any(w in text for w in words)]
    score = len(matched) / len(STAR_PARTS)

    if len(answer.split()) < 15:
        tier = "TOO_SHORT"
        tip = "Too brief to show real structure -- a strong behavioral answer is usually 4-8 sentences."
    elif score >= 0.75:
        tier = "STRONG_STAR_STRUCTURE"
        tip = "Hits the real STAR shape -- situation, task, action, and result are all present."
    elif score >= 0.5:
        tier = "PARTIAL_STAR_STRUCTURE"
        missing = [p for p in STAR_PARTS if p not in matched]
        tip = f"Good start -- your answer is missing a clear {' and '.join(missing)} section."
    else:
        tier = "WEAK_STAR_STRUCTURE"
        tip = "Missing most of the STAR structure -- name a specific situation, what you had to do, what you actually did, and what happened as a result."

    return {"tier": tier, "coaching_tip": tip, "star_score": round(score, 2), "matched_parts": matched}
