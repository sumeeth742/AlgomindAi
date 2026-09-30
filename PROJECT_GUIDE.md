# ALGOMIND AI — Run Guide & Feature Implementation Reference

A single downloadable document covering how to run the project locally, and exactly how every real feature is implemented. This file lives at the project root (`PROJECT_GUIDE.md`) — open it in any Markdown viewer (VS Code, GitHub, Obsidian, or a browser Markdown extension), or print it to PDF from there.

---

## Part 1 — How to run it

### Prerequisites
- Python 3.12
- Node.js (for the frontend — Next.js 16 / React 19)
- Windows note: this project has been run and verified on Windows with Git Bash / PowerShell.

### Backend

```bash
cd backend
py -3.12 -m venv venv

# llama-cpp-python needs a prebuilt wheel on Windows (building from source hits a
# Windows MAX_PATH limit on llama.cpp's vendored source tree) -- use this index:
./venv/Scripts/pip install -r requirements.txt --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu

./venv/Scripts/python -m app.seed.seed_all               # idempotent -- seeds skills/problems/system-design/networks content
./venv/Scripts/python -m app.services.llm.download_model # one-time ~1.1GB download, enables the local AI lesson chat
./venv/Scripts/python -m uvicorn app.main:app --port 8000 --reload
```

- API docs (interactive): `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/health`
- If you skip the model download, everything works except the three LLM-backed endpoints (lesson `/ask`, submission `/explain`, interview answer "commentary"), which return a clear `503` instead of pretending to work.
- **Windows note**: uvicorn's `--reload` doesn't always pick up a change to `app/main.py` specifically (middleware changes) — if things seem stale after editing that file, stop and restart uvicorn manually.
- The database is a single SQLite file at `backend/algomind.db`, created automatically on first run. To reset all data, stop the server and delete that file, then re-run the seed command.

### Frontend

```bash
cd frontend
npm install
# optional: create .env.local with NEXT_PUBLIC_API_URL if your backend isn't on http://127.0.0.1:8000
npm run dev -- --port 3002
```

Visit `http://localhost:3002`, register an account, and go. (Any port works — the backend's CORS policy allows any `localhost`/`127.0.0.1` port, since Next picks the next free one automatically if you don't pin one.)

### Quick sanity check that everything's wired up
1. Backend: `curl http://127.0.0.1:8000/health` → `{"status":"ok"}`
2. Frontend: open `http://localhost:3002` → you should see the landing page (logged out) or dashboard (logged in)
3. Register a real account, solve a problem on `/problems`, and check `/dashboard` updates

---

## Part 2 — How every feature is implemented

### Access
**Register / Login** — Two real Pydantic `field_validator`s run before an account is created: the name must be 2+ letters with no digits; the password must be 8+ characters with at least one letter and one digit. Passwords are bcrypt-hashed (never stored plain). Login issues a signed JWT (HS256, 24h expiry) — there is no server-side session store; every request re-verifies the token and re-loads the real user row from the database.

### DSA practice core
- **Submission & grading** — code runs in a fresh, isolated OS subprocess (never `eval()`'d in the API process), with a wall-clock timeout, disabled network sockets, and a throwaway temp directory. Real test cases are fed in; linked-list/tree arguments are built from JSON via `io_transforms.py`. Supports Python, JavaScript, and Java (compiled fresh per submission via `javac`).
- **Hints** — 5 leveled hints per problem; every open is logged as a real `HintUsage` row, which feeds the Habit Profiler.
- **Own-Code Trace** — steps through the learner's *own* code at the exact input that broke it, using a genuinely different real mechanism per language: Python's `sys.settrace` (a real CPython debugging hook), JavaScript via AST instrumentation (espree-parsed, trace calls spliced before every statement), Java via JDI (the Java Debug Interface — the same tech real IDE debuggers use).
- **Blind Practice** — a random unsolved problem with zero skill/chapter context shown, forcing genuinely unprompted pattern recognition.
- **Pattern reasoning + Reasoning Gap Diff** — correctness is a set-membership check against the problem's real valid patterns. The quality score and gap diff are pure vocabulary set-arithmetic: `missing_evidence` is real correct-pattern vocabulary never mentioned; `declared_pattern_evidence` is the wrong pattern's own vocabulary that *was* used — concrete proof of what pulled the reasoning off track.
- **Empirical Complexity Probe** — re-runs the passing solution at real increasing input sizes (100/400/1600/6400, or 10/20/30/37 for recursive/scalar problems), measures real wall-clock time, fits a log-log growth exponent after subtracting a measured baseline overhead. Declines rather than guesses for shapes it can't safely scale (trees, grids, multi-arg).
- **Diagnosis engine** — real AST-derived code features (loop nesting, recursion, hash/heap usage — via Python's `ast`, JS's `acorn`, Java's `javalang`) plus real submission history feed a `RandomForestClassifier` (120 trees, depth 8, trained on 4,000 rule-labeled synthetic examples) for a 7-category root cause with a real confidence and real evidence strings. A separate, always-on deterministic check independently flags a passing-but-brute-force solution even when the model says "mastered."
- **Mastery (EWMA)** — `new = (1-α)·old + α·target`, α scaled by problem difficulty. A correct re-solve of an already-passed problem is dampened to 15% of normal weight; a repeat failure is not dampened.

### AI coach models (scikit-learn, local, no API key)
Four small neural nets (`MLPClassifier`, 2 hidden layers of 32/16 units) share one honest pattern: trained once per server process on 4,000 synthetic examples whose *labels* come from an explicit, readable rule function, while the *features* fed in at prediction time are always 100% real:
- **Habit Profiler** — classifies overall problem-solving habits from real `reasoning_usage_rate`, `avg_hints_per_problem`, `avg_submissions_per_problem`, `solve_rate`.
- **Plan-Quality Scorer** — scores pre-code reasoning text via real structural features (word count, `O(...)` notation detected, tradeoff/edge-case keyword presence).
- **System Design Scope Coach** — verdicts (over/under-engineered) from the real missing/unjustified component counts the critique engine already computed.
- **Explain-It-Back (Feynman) Scorer** — compares a learner's own-words explanation against the lesson's real "Key Takeaway" vocabulary.

A fifth model, the pre-existing **Diagnosis RandomForest**, is described above under DSA core.

### System Design
- **HLD Case Critique** — rule-based, not an LLM. `missing` = expected components absent from the submitted diagram; `unjustified` = any present component from a fixed challenge table that wasn't actually expected at this scale; isolated (edge-less) nodes are also flagged. Score = coverage − penalties. Estimation answers are graded within a ±50% tolerance band of the real expected order of magnitude.
- **LLD Critique** — the class-design equivalent: submitted classes matched against expected ones by name *or* alias (so a reasonable synonym isn't penalized), plus god-class detection.

### Cross-curriculum features
- **Cross-Domain Concept Bridge** — unsupervised TF-IDF + cosine similarity over all 86 real lesson documents (DSA + System Design + Networks). No labels, nothing synthetic — real lexical overlap above a noise floor surfaces genuine cross-curriculum links (e.g. "Sliding Window" ↔ "TCP Sliding Window").
- **Ask-Anything Lesson Chat** — the one feature using an actual language model: Qwen2.5-1.5B-Instruct (GGUF, Q4_K_M), run fully in-process via `llama-cpp-python`, no network call. Grounded to answer only from the specific lesson's real content — never a source of truth for grading.
- **Printable Study Cheat Sheet** — groups every skill/lesson by chapter/category with its real mnemonic and real "Key Takeaway" text (shared extractor also used by Explain-It-Back). A print stylesheet hides the app chrome so only the sheet itself prints.
- **Narrated Animated Walkthroughs** — 18 hand-authored real step sequences (10 System Design + 8 Networks) driving an interactive diagram; a narration toggle reads each step aloud via the browser's own built-in speech synthesis (no API key).

### Progress & motivation systems
- **Retention (SM-2)** — the real Anki/SuperMemo spaced-repetition algorithm, per skill. A review result maps to a quality score; the interval grows 1 day → 3 days → previous×ease-factor, with the ease factor floored at 1.3.
- **Recommendation engine** — a 5-tier rule-based priority waterfall (overdue retention first, then weak-but-ready skills, then transfer gaps, then the next unstarted skill, then a targeted practice problem), every recommendation carrying a real what/why/expected-outcome explanation.
- **Track Tier Assessments** (Novice → Practitioner → Expert) — never gated on mastery; starting one always deals a fresh real random draw of items. Each item scores 0–1 from only real, already-existing signals; the assessment passes at a mean ≥ 0.85 across all items, not a perfect-every-item bar.
- **Streak & dashboard** — the streak is a real walk backward through actual `LearningEvent` dates until a gap is found, never an incremented counter that could drift from reality.

### Interview prep
- **Single-Round Mock Interview** — a deterministic stage machine (not an LLM): fixed real question sequences per stage (7 for DSA, 16 for System Design), reacting to answers with keyword/number checks.
- **Full Mock Interview Loop** — chains one DSA problem, one System Design case, and one behavioral question into a single timed session. Deliberately does *not* re-grade DSA/System Design a second time — it links to the real `Submission`/`SystemDesignAttempt` rows created through the app's own already-tested submit endpoints. The behavioral round is the one genuinely new piece: real, structural STAR-format phrase detection (Situation/Task/Action/Result).

### Contests
**Contests & leaderboard** — a contest bundles a fixed list of real problem ids within a time window; each contest submission links to an already-graded real `Submission` row (code is never duplicated), and the leaderboard aggregates real scores per user.

---

*Generated from the real, currently-running codebase — every mechanism above is verifiable in `backend/app` and `frontend/src`. For a browsable, styled version of this same content, see the "Demo Defense Notes" and "Feature Implementation Guide" artifacts shared earlier in this session.*
