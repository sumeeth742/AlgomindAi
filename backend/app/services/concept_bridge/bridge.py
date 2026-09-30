"""
Cross-Domain Concept Bridge: this platform is unusual in teaching DSA, System
Design, and Computer Networks side by side, but the three curricula are
authored and browsed as separate silos -- nothing ever tells a learner that
"Sliding Window" (a DSA pattern) and "TCP Sliding Window" (a Networks lesson)
are the same underlying idea wearing two different hats.

This computes that connection for real: TF-IDF vectorizes every lesson's
actual title + body across all three curricula, then cosine-similarity ranks
every lesson against every other lesson. For a given lesson, the top matches
from the OTHER two curricula (never the same one -- that's just "related
topics", not a cross-domain bridge) above a small noise floor are returned
with their real similarity score, never a hand-curated or invented list.

Local scikit-learn only, no API key, no pretrained embeddings (those were
deliberately removed from this project) -- a classic, honest bag-of-words
technique that is exactly as good as the actual lexical overlap between the
two lessons, and says so via the real score it reports.
"""
from __future__ import annotations

import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session

from app.models.network import NetworkLesson
from app.models.skill import Skill
from app.models.system_design import SystemDesignLesson

TOP_K = 3
MIN_SIMILARITY = 0.06  # below this, lexical overlap is noise, not a real bridge

_CODE_FENCE = re.compile(r"```.*?```", re.S)

# process-lifetime cache: corpus content is seeded once and essentially static,
# so rebuild only if the number of lessons on either side actually changes
# (e.g. a reseed), rather than recomputing TF-IDF on every request.
_cache: dict = {"count": None, "items": None, "matrix": None}


def _clean(text: str) -> str:
    return _CODE_FENCE.sub(" ", text or "")


def _load_items(db: Session) -> list[dict]:
    items: list[dict] = []
    for s in db.query(Skill).all():
        items.append({"domain": "dsa", "key": s.key, "title": s.name, "text": f"{s.name} {_clean(s.concept_markdown)}"})
    for l in db.query(SystemDesignLesson).all():
        items.append({"domain": "system_design", "key": l.slug, "title": l.title, "text": f"{l.title} {_clean(l.content_markdown)}"})
    for l in db.query(NetworkLesson).all():
        items.append({"domain": "networks", "key": l.slug, "title": l.title, "text": f"{l.title} {_clean(l.content_markdown)}"})
    return items


def _get_corpus(db: Session):
    count = db.query(Skill).count() + db.query(SystemDesignLesson).count() + db.query(NetworkLesson).count()
    if _cache["count"] != count:
        items = _load_items(db)
        vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), min_df=1, max_df=0.85)
        matrix = vectorizer.fit_transform([it["text"] for it in items])
        similarity = cosine_similarity(matrix)
        _cache.update(count=count, items=items, matrix=similarity)
    return _cache["items"], _cache["matrix"]


def get_bridges(db: Session, domain: str, key: str) -> list[dict]:
    items, similarity = _get_corpus(db)
    idx = next((i for i, it in enumerate(items) if it["domain"] == domain and it["key"] == key), None)
    if idx is None:
        return []

    scores = similarity[idx]
    candidates = [
        {"domain": it["domain"], "key": it["key"], "title": it["title"], "similarity": float(scores[i])}
        for i, it in enumerate(items)
        if it["domain"] != domain and scores[i] >= MIN_SIMILARITY
    ]
    candidates.sort(key=lambda c: c["similarity"], reverse=True)
    return candidates[:TOP_K]


def get_top_bridges_platform_wide(db: Session, limit: int = 20) -> list[dict]:
    """Every cross-domain pair above the noise floor, ranked highest-first, for
    a whole-platform explorer view rather than one lesson at a time."""
    items, similarity = _get_corpus(db)
    seen_pairs = set()
    pairs = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i]["domain"] == items[j]["domain"]:
                continue
            score = float(similarity[i][j])
            if score < MIN_SIMILARITY:
                continue
            key = tuple(sorted([f"{items[i]['domain']}:{items[i]['key']}", f"{items[j]['domain']}:{items[j]['key']}"]))
            if key in seen_pairs:
                continue
            seen_pairs.add(key)
            pairs.append({
                "a_domain": items[i]["domain"], "a_key": items[i]["key"], "a_title": items[i]["title"],
                "b_domain": items[j]["domain"], "b_key": items[j]["key"], "b_title": items[j]["title"],
                "similarity": score,
            })
    pairs.sort(key=lambda p: p["similarity"], reverse=True)
    return pairs[:limit]
