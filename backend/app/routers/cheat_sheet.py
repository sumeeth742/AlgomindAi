from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.network import NetworkLesson
from app.models.skill import Skill
from app.models.system_design import SystemDesignLesson
from app.schemas.cheat_sheet import CheatSheetGroup, CheatSheetItem
from app.services.content.key_takeaway import extract_key_takeaway

router = APIRouter(prefix="/cheat-sheet", tags=["cheat-sheet"])


def _group(items: list[tuple[str, CheatSheetItem]]) -> list[CheatSheetGroup]:
    """Groups items by their group label, preserving first-seen order -- since
    callers already query sorted by curriculum level, groups naturally come
    out in the same order the curriculum introduces them, without needing a
    second hand-maintained ordering list."""
    order: list[str] = []
    buckets: dict[str, list[CheatSheetItem]] = {}
    for group_label, item in items:
        if group_label not in buckets:
            buckets[group_label] = []
            order.append(group_label)
        buckets[group_label].append(item)
    return [CheatSheetGroup(group=g, items=buckets[g]) for g in order]


@router.get("/dsa", response_model=list[CheatSheetGroup])
def dsa_cheat_sheet(db: Session = Depends(get_db)):
    """One real card per DSA skill: its own mnemonic plus its own real
    'Key Takeaway' section -- nothing generated for this page specifically,
    just the same content already shown on the lesson page, condensed."""
    skills = db.query(Skill).order_by(Skill.level.asc(), Skill.chapter.asc()).all()
    items = [
        (s.chapter, CheatSheetItem(
            key=s.key, title=s.name, mnemonic=s.mnemonic or None,
            key_takeaway=extract_key_takeaway(s.concept_markdown),
        ))
        for s in skills
    ]
    return _group(items)


@router.get("/system-design", response_model=list[CheatSheetGroup])
def system_design_cheat_sheet(db: Session = Depends(get_db)):
    lessons = db.query(SystemDesignLesson).order_by(SystemDesignLesson.level.asc(), SystemDesignLesson.category.asc()).all()
    items = [
        (l.category or "general", CheatSheetItem(
            key=l.slug, title=l.title, key_takeaway=extract_key_takeaway(l.content_markdown),
        ))
        for l in lessons
    ]
    return _group(items)


@router.get("/networks", response_model=list[CheatSheetGroup])
def networks_cheat_sheet(db: Session = Depends(get_db)):
    lessons = db.query(NetworkLesson).order_by(NetworkLesson.level.asc(), NetworkLesson.category.asc()).all()
    items = [
        (l.category or "general", CheatSheetItem(
            key=l.slug, title=l.title, key_takeaway=extract_key_takeaway(l.content_markdown),
        ))
        for l in lessons
    ]
    return _group(items)
