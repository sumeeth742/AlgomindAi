from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app import models  # noqa: F401 -- ensures all model classes are registered on Base before create_all
from app.routers import (
    analytics, auth, cheat_sheet, concept_bridges, contests, interviews, lld, networks, problems, recommendations,
    retention, skills, system_design, tracks,
)

app = FastAPI(title="ALGOMIND AI", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    # Next.js dev picks the next free port when 3000 is taken (3001, 3002, ...), so a
    # fixed single-origin allowlist breaks the moment that happens. Regex covers any
    # localhost/127.0.0.1 dev port instead of hardcoding one.
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1):\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


app.include_router(auth.router)
app.include_router(skills.router)
app.include_router(problems.router)
app.include_router(recommendations.router)
app.include_router(retention.router)
app.include_router(system_design.router)
app.include_router(interviews.router)
app.include_router(analytics.router)
app.include_router(tracks.router)
app.include_router(contests.router)
app.include_router(lld.router)
app.include_router(networks.router)
app.include_router(concept_bridges.router)
app.include_router(cheat_sheet.router)


@app.get("/health")
def health():
    return {"status": "ok"}
