"""
Run with: python -m app.seed.seed_all

Idempotent: safe to re-run, skips rows that already exist by their unique key.
Test-case expected outputs are computed by actually executing each problem's
reference solution against its test args -- never hand-typed -- so seed data
can't silently drift from the reference implementation.
"""
from __future__ import annotations

import copy

from app.database import Base, SessionLocal, engine
from app.models.contest import Contest
from app.models.problem import Hint, Problem, ProblemTestCase
from app.models.network import NetworkLesson, NetworkQuizQuestion
from app.models.quiz import QuizQuestion
from app.models.skill import Skill, SkillPrerequisite
from app.models.system_design import LLDCase, SystemDesignCase, SystemDesignLesson
from app.seed.contest_seed import build_contests
from app.seed.network_quiz_seed import NETWORK_QUIZZES
from app.seed.network_seed import NETWORK_LESSONS
from app.seed.problems_seed import PROBLEMS as PROBLEMS_BATCH1
from app.seed.problems_seed_batch2 import PROBLEMS_BATCH2
from app.seed.problems_seed_batch3 import PROBLEMS_BATCH3
from app.seed.problems_seed_batch4 import PROBLEMS_BATCH4
from app.seed.quiz_seed import QUIZZES

PROBLEMS = PROBLEMS_BATCH1 + PROBLEMS_BATCH2 + PROBLEMS_BATCH3 + PROBLEMS_BATCH4
from app.seed.skills_seed import PREREQUISITES, SKILLS
from app.seed.system_design_seed import CASES, LESSONS, LLD_CASES
from app.services.execution.io_transforms import (
    ListNode, TreeNode, apply_arg_transforms, apply_result_transform,
)


def _run_reference(source: str, function_name: str, args: list, io_transform: dict | None = None):
    """Mirrors exactly what the sandbox does at submission time (see
    sandbox.py's RUNNER_TEMPLATE): make ListNode/TreeNode available, apply arg
    transforms, call the function, apply the result transform -- so the stored
    expected_output is directly comparable to what a correct submission's
    sandboxed output will be."""
    namespace: dict = {"ListNode": ListNode, "TreeNode": TreeNode}
    exec(compile(source, "<reference>", "exec"), namespace)
    fn = namespace[function_name]
    call_args = apply_arg_transforms(copy.deepcopy(args), (io_transform or {}).get("args"))
    result = fn(*call_args)
    return apply_result_transform(result, (io_transform or {}).get("result"))


def seed_skills(db):
    key_to_id = {}
    for s in SKILLS:
        existing = db.query(Skill).filter(Skill.key == s["key"]).first()
        if existing:
            # Refresh content fields on re-seed so editing skills_seed.py and re-running
            # takes effect without needing a full DB reset -- structural identity (key,
            # id) never changes, only the descriptive/lesson content.
            existing.name = s["name"]
            existing.chapter = s["chapter"]
            existing.level = s["level"]
            existing.description = s["description"]
            existing.concept_markdown = s["concept_markdown"]
            existing.mnemonic = s.get("mnemonic", "")
            existing.comic_script = s.get("comic_script", [])
            key_to_id[s["key"]] = existing.id
            continue
        skill = Skill(
            key=s["key"], name=s["name"], chapter=s["chapter"], level=s["level"],
            description=s["description"], concept_markdown=s["concept_markdown"],
            mnemonic=s.get("mnemonic", ""), comic_script=s.get("comic_script", []),
        )
        db.add(skill)
        db.flush()
        key_to_id[s["key"]] = skill.id
    db.commit()

    for skill_key, prereq_key in PREREQUISITES:
        skill_id = key_to_id[skill_key]
        prereq_id = key_to_id[prereq_key]
        existing = db.query(SkillPrerequisite).filter(
            SkillPrerequisite.skill_id == skill_id, SkillPrerequisite.prerequisite_skill_id == prereq_id
        ).first()
        if not existing:
            db.add(SkillPrerequisite(skill_id=skill_id, prerequisite_skill_id=prereq_id))
    db.commit()
    return key_to_id


def seed_problems(db, skill_key_to_id: dict):
    for p in PROBLEMS:
        if db.query(Problem).filter(Problem.slug == p["slug"]).first():
            continue
        problem = Problem(
            slug=p["slug"], title=p["title"], statement_markdown=p["statement"],
            difficulty=p["difficulty"], concept_difficulty=p["concept_difficulty"],
            implementation_difficulty=p["implementation_difficulty"], reasoning_difficulty=p["reasoning_difficulty"],
            pattern_difficulty=p["pattern_difficulty"], primary_skill_id=skill_key_to_id[p["primary_skill"]],
            pattern_skill_ids=p["pattern_skills"], constraints_markdown=p["constraints"], examples=p["examples"],
            function_name=p["function_name"], starter_code_python=p["starter_code"],
            reference_solution_python=p["reference_solution"], expected_complexity=p["expected_complexity"],
            io_transform=p.get("io_transform", {}), output_comparison=p.get("output_comparison", "exact"),
        )
        db.add(problem)
        db.flush()

        for tc in p["test_cases"]:
            expected = _run_reference(p["reference_solution"], p["function_name"], tc["args"], p.get("io_transform"))
            db.add(ProblemTestCase(
                problem_id=problem.id, args=tc["args"], expected_output=expected,
                is_hidden=tc["hidden"], explanation=tc["explanation"],
            ))

        for i, hint_text in enumerate(p["hints"], start=1):
            db.add(Hint(problem_id=problem.id, level=i, text_markdown=hint_text))

    db.commit()


def seed_system_design(db):
    for lesson in LESSONS:
        existing = db.query(SystemDesignLesson).filter(SystemDesignLesson.slug == lesson["slug"]).first()
        if existing:
            # Refresh content on re-seed, same as seed_skills -- editing lesson
            # text in system_design_seed.py and re-running takes effect without
            # needing a full DB reset; slug/level/category identity never changes.
            existing.title = lesson["title"]
            existing.level = lesson["level"]
            existing.category = lesson["category"]
            existing.content_markdown = lesson["content"]
            existing.dsa_connection = lesson["dsa_connection"]
            existing.comic_script = lesson.get("comic_script", [])
            continue
        db.add(SystemDesignLesson(
            slug=lesson["slug"], title=lesson["title"], level=lesson["level"], category=lesson["category"],
            content_markdown=lesson["content"], dsa_connection=lesson["dsa_connection"],
            comic_script=lesson.get("comic_script", []),
        ))

    for case in CASES:
        if db.query(SystemDesignCase).filter(SystemDesignCase.slug == case["slug"]).first():
            continue
        db.add(SystemDesignCase(
            slug=case["slug"], title=case["title"], difficulty=case["difficulty"],
            base_slug=case.get("base_slug"), scale_tier=case.get("scale_tier"),
            scale_description=case.get("scale_description"),
            description_markdown=case["description"], functional_requirements=case["functional_requirements"],
            non_functional_requirements=case["non_functional_requirements"], estimation_prompt=case["estimation_prompt"],
            estimation_expected=case["estimation_expected"], expected_components=case["expected_components"],
            editorial_markdown=case["editorial"],
        ))

    for lld_case in LLD_CASES:
        existing = db.query(LLDCase).filter(LLDCase.slug == lld_case["slug"]).first()
        if existing:
            existing.title = lld_case["title"]
            existing.difficulty = lld_case["difficulty"]
            existing.description_markdown = lld_case["description"]
            existing.functional_requirements = lld_case["functional_requirements"]
            existing.non_functional_requirements = lld_case["non_functional_requirements"]
            existing.expected_classes = lld_case["expected_classes"]
            existing.abstraction_hint = lld_case["abstraction_hint"]
            existing.editorial_markdown = lld_case["editorial"]
            continue
        db.add(LLDCase(
            slug=lld_case["slug"], title=lld_case["title"], difficulty=lld_case["difficulty"],
            description_markdown=lld_case["description"], functional_requirements=lld_case["functional_requirements"],
            non_functional_requirements=lld_case["non_functional_requirements"],
            expected_classes=lld_case["expected_classes"], abstraction_hint=lld_case["abstraction_hint"],
            editorial_markdown=lld_case["editorial"],
        ))
    db.commit()


def seed_networks(db):
    for lesson in NETWORK_LESSONS:
        existing = db.query(NetworkLesson).filter(NetworkLesson.slug == lesson["slug"]).first()
        if existing:
            # Same refresh-on-conflict pattern as seed_system_design -- editing
            # lesson text in network_seed.py and re-running takes effect without
            # needing a full DB reset.
            existing.title = lesson["title"]
            existing.level = lesson["level"]
            existing.category = lesson["category"]
            existing.content_markdown = lesson["content"]
            existing.practical_connection = lesson["practical_connection"]
            existing.comic_script = lesson.get("comic_script", [])
            continue
        db.add(NetworkLesson(
            slug=lesson["slug"], title=lesson["title"], level=lesson["level"], category=lesson["category"],
            content_markdown=lesson["content"], practical_connection=lesson["practical_connection"],
            comic_script=lesson.get("comic_script", []),
        ))
    db.commit()


def seed_network_quizzes(db):
    seeded = 0
    for lesson_slug, questions in NETWORK_QUIZZES.items():
        lesson = db.query(NetworkLesson).filter(NetworkLesson.slug == lesson_slug).first()
        if not lesson:
            continue
        existing = {q.question for q in db.query(NetworkQuizQuestion).filter(NetworkQuizQuestion.lesson_id == lesson.id).all()}
        for q in questions:
            if q["question"] in existing:
                continue
            db.add(NetworkQuizQuestion(
                lesson_id=lesson.id, question=q["question"], options=q["options"],
                correct_index=q["correct_index"], explanation=q.get("explanation", ""),
            ))
            seeded += 1
    db.commit()
    return seeded


def seed_quizzes(db, skill_key_to_id: dict):
    seeded = 0
    for skill_key, questions in QUIZZES.items():
        skill_id = skill_key_to_id.get(skill_key)
        if not skill_id:
            continue
        existing = {q.question for q in db.query(QuizQuestion).filter(QuizQuestion.skill_id == skill_id).all()}
        for q in questions:
            if q["question"] in existing:
                continue
            db.add(QuizQuestion(
                skill_id=skill_id, question=q["question"], options=q["options"],
                correct_index=q["correct_index"], explanation=q.get("explanation", ""),
            ))
            seeded += 1
    db.commit()
    return seeded


def seed_contests(db):
    seeded = 0
    for c in build_contests():
        if db.query(Contest).filter(Contest.title == c["title"]).first():
            continue
        problem_ids = [
            p.id for slug in c["problem_slugs"]
            for p in [db.query(Problem).filter(Problem.slug == slug).first()] if p
        ]
        db.add(Contest(title=c["title"], start_at=c["start_at"], end_at=c["end_at"], problem_ids=problem_ids))
        seeded += 1
    db.commit()
    return seeded


def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        skill_key_to_id = seed_skills(db)
        seed_problems(db, skill_key_to_id)
        seed_system_design(db)
        seed_networks(db)
        n_quiz = seed_quizzes(db, skill_key_to_id)
        n_network_quiz = seed_network_quizzes(db)
        n_contests = seed_contests(db)
        print(
            f"Seeded {len(SKILLS)} skills, {len(PROBLEMS)} problems, {len(LESSONS)} lessons, "
            f"{len(CASES)} case studies, {len(LLD_CASES)} LLD exercises, {len(NETWORK_LESSONS)} network lessons, "
            f"{n_quiz} quiz questions, {n_network_quiz} network quiz questions, {n_contests} contests."
        )
    finally:
        db.close()


if __name__ == "__main__":
    main()
