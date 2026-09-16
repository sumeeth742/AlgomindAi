"""
Ask-anything doubt-clearing chat for lesson content -- the same local LLM
already used for problem explanations/Q&A (services/llm/local_llm.py),
grounded strictly in the specific lesson's own content so a student stuck on
something in a DSA skill, System Design lesson, or Networks lesson can ask a
plain-English question and get a plain-English answer, without leaving the
page. Shared across all three lesson types since they all reduce to the same
shape: a title, a markdown body, and a student's question.
"""
from __future__ import annotations

from app.services.llm.local_llm import LocalLLMUnavailable, generate as llm_generate  # noqa: F401 -- re-exported for callers


def ask_about_lesson(title: str, content_markdown: str, question: str) -> str:
    return llm_generate(
        system_prompt=(
            "You are a patient tutor helping a student who just read a lesson and got stuck on something. "
            "Answer ONLY using the lesson content given below -- do not introduce facts, numbers, or claims "
            "that aren't supported by it. If the question genuinely can't be answered from this lesson, say so "
            "plainly instead of guessing. Keep the answer to 2-4 short, plain-language sentences, and avoid "
            "unexplained jargon -- assume the student is still learning this topic."
        ),
        user_prompt=f"Lesson: {title}\n\n{content_markdown}\n\nStudent's question: {question}",
        max_tokens=260,
    )
