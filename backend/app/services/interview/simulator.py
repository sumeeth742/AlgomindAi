"""
Interview simulator: a deterministic stage machine, not an LLM.

Without an API key, an "AI interviewer" can't freely generate follow-ups, so
this asks the fixed sequence of questions a real interviewer structurally
asks (spec section 47 for system design, and the standard DSA interview
loop), and reacts to what the candidate answers using simple keyword/number
checks rather than pretending to understand free text.
"""
from __future__ import annotations

SYSTEM_DESIGN_STAGES = [
    ("clarify", "Before designing anything: what does this system need to do, and for whom? Ask me anything you'd ask a real interviewer."),
    ("functional_requirements", "List the functional requirements you'll design for."),
    ("non_functional_requirements", "What non-functional requirements matter most here (latency, availability, consistency, durability)?"),
    ("scale_estimation", "Estimate scale: how many users, requests/sec, and storage growth per day?"),
    ("api_design", "Sketch the core API endpoints you'd expose."),
    ("data_model", "What does your data model look like? Which store(s) hold what?"),
    ("high_level_architecture", "Walk me through the high-level architecture, box by box."),
    ("database_choice", "Why this database? What would break your choice at 100x the data?"),
    ("caching", "Where, if anywhere, does caching help, and what's your invalidation strategy?"),
    ("scaling", "What's your first bottleneck as traffic grows, and how do you scale past it?"),
    ("failure_handling", "What happens when one of your servers/databases goes down mid-request?"),
    ("security", "What are the main security/abuse concerns for this system?"),
    ("monitoring", "What would you monitor to know this system is healthy?"),
    ("tradeoffs", "What's the biggest trade-off in your design, and why did you choose that side?"),
    ("bottlenecks", "If I told you traffic just increased 100x, what's the first thing that breaks?"),
    ("done", "That's a wrap. Let's review your answers."),
]

DSA_STAGES = [
    ("clarify", "Before coding: restate the problem in your own words and ask any clarifying questions."),
    ("approach", "What approach are you considering, and what's its time/space complexity?"),
    ("complexity", "Can you do better than that? What's the theoretical lower bound here?"),
    ("code", "Go ahead and implement it."),
    ("test", "Walk me through your code on the example inputs, including an edge case."),
    ("optimize", "Is there anything you'd optimize if this were a real production function?"),
    ("done", "That's a wrap. Let's review your answers."),
]


def stages_for(interview_type: str):
    return SYSTEM_DESIGN_STAGES if interview_type == "system_design" else DSA_STAGES


def first_stage(interview_type: str) -> tuple[str, str]:
    return stages_for(interview_type)[0]


def next_stage(interview_type: str, current_stage: str) -> tuple[str, str] | None:
    stages = stages_for(interview_type)
    keys = [s[0] for s in stages]
    idx = keys.index(current_stage) if current_stage in keys else -1
    if idx + 1 >= len(stages):
        return None
    return stages[idx + 1]
