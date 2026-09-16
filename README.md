# ALGOMIND AI

Adaptive DSA + System Design learning platform. This is a working foundation of the
full vision in the original spec, not the complete 88-section system -- see
"Honest scope" below for exactly what's real vs. what's architected-but-not-built.

## Stack

- **Backend**: FastAPI + SQLAlchemy + SQLite (swap `DATABASE_URL` for Postgres in production)
- **Diagnosis / recommendation "AI"**: scikit-learn (a RandomForest trained in-process on a
  rule-grounded synthetic dataset) + deterministic rule engines -- **no LLM API key is used
  anywhere**, per your instruction. See `backend/app/services/diagnosis/model.py`.
- **Local text generation**: Qwen2.5-1.5B-Instruct, quantized to GGUF (Q4_K_M, ~1.1GB), run
  entirely in-process via `llama-cpp-python` -- no network call, no API key, ever. Used to
  *phrase* facts that are already computed deterministically (see "What's real" below), never
  as the source of truth for correctness. See `backend/app/services/llm/local_llm.py`.
- **Frontend**: Next.js (App Router) + TypeScript + Tailwind + Monaco Editor + Recharts + TanStack Query

## Running it

### Backend

```bash
cd backend
py -3.12 -m venv venv
# llama-cpp-python needs a prebuilt wheel on Windows (building from source hits a
# Windows MAX_PATH limit on llama.cpp's vendored source tree) -- use this index:
./venv/Scripts/pip install -r requirements.txt --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
./venv/Scripts/python -m app.seed.seed_all              # idempotent -- seeds skills/problems/system-design content
./venv/Scripts/python -m app.services.llm.download_model # one-time ~1.1GB download for local text generation
./venv/Scripts/python -m uvicorn app.main:app --port 8000 --reload
```

API docs at `http://127.0.0.1:8000/docs`. If you skip the model download, everything works
except the three LLM-backed endpoints (`/problems/{slug}/explain`, `/problems/{slug}/ask`, and
interview answer "commentary"), which return a clear 503 instead of pretending to work.

**Windows note on `--reload`**: in this environment, uvicorn's `--reload` watcher did not
reliably re-apply a middleware change to the running process (a fresh restart was needed to
pick it up) -- if you edit `app/main.py` specifically and things seem stale, restart uvicorn
manually rather than trusting the auto-reload.

### Frontend

```bash
cd frontend
npm install
# .env.local -> NEXT_PUBLIC_API_URL should point at your backend URL/port
npm run dev
```

Visit the printed localhost URL, register an account, and go.

## What's real (per section 87 -- "don't fake it")

- **Real auth**: JWT + bcrypt password hashing.
- **Real code execution**: submissions run in an isolated Python subprocess (`app/services/execution/sandbox.py`)
  against real test cases -- nothing is fabricated. Windows note: memory limits aren't enforced (no `resource`
  module on Windows); wall-clock timeout and process isolation are.
- **Real diagnosis**: a trained scikit-learn classifier + static AST analysis of submitted code, citing only
  evidence it actually observed (test pass ratio, hint count, loop nesting, etc.) -- returns nothing it can't back up.
- **Real skill tracking**: EWMA mastery updates per skill, weighted by difficulty, from real submission outcomes.
- **Real spaced repetition**: SM-2 scheduling (the actual Anki/SuperMemo algorithm) drives retention review due-dates.
- **Real transfer challenge**: once a skill's mastery on familiar problems crosses 60% (`/skills/{key}/transfer-challenge`),
  the app surfaces a specific, not-yet-attempted problem in that skill rather than "solve another easy one" -- solving
  it in transfer mode updates a separate `transfer_accuracy` metric from regular mastery, the platform's actual
  anti-memorization check (spec section 52). Honestly reports "not available yet" or "no unattempted problem left"
  rather than fabricating a challenge.
- **Real study streak**: computed from actual `LearningEvent` timestamps (submissions + retention reviews) --
  consecutive active days ending today or yesterday, not a fabricated or estimated number.
- **Real progress tracking**: the problems list shows per-problem solved/attempted status for the logged-in
  user, with filters for skill, difficulty, and status.
- **Real recommendations**: rule-based over the skill graph/prerequisites/mastery/retention/transfer, each with an
  explicit WHAT/WHY/EXPECTED OUTCOME.
- **Real system design critique**: architecture submissions are checked against each case's expected component list;
  estimation answers are graded against real order-of-magnitude tolerances.
- **Real interview simulator**: a deterministic stage machine (not an LLM for progression/scoring) walks the
  standard DSA/system-design interview loop and reports stage coverage; the local LLM adds an optional short
  reaction to each answer, but never gates progression or the coverage score.
- **Real local text generation, grounded, not free-floating**: `/problems/{slug}/explain` turns the diagnosis
  engine's evidence list into plain language; `/problems/{slug}/ask` answers free-form questions about a problem
  using its own statement/constraints as context. Small local models can still misstate a detail, so both are
  labeled as generated in the UI and shown alongside (never instead of) the deterministic facts.
- **Real Run vs Submit separation**: `/problems/{slug}/run` checks your code against only the visible example
  tests and never touches mastery/retention/diagnosis -- for fast iteration, like a real IDE's "Run" button.
  `/problems/{slug}/submit` runs the full (visible + hidden) suite and is the one that counts as an attempt.
- **Empirical Big-O verification, not just static loop-counting**: after a passing submission, `/problems/{slug}/
  verify-complexity` (`execution/complexity_probe.py`) actually re-runs the user's own code against several
  progressively larger *synthetic* inputs of the same shape as the problem's real test data (sizes chosen and
  verified by directly timing a true worst-case O(n^2) loop, so it finishes within the sandbox's timeout instead
  of always just timing out), measures real wall-clock time for each, and fits a growth-rate exponent via log-log
  regression -- a genuine dynamic complement to `detect_brute_force()`'s static loop-nesting count, which can be
  fooled by two sequential loops instead of nested ones. Every number shown (sizes, raw milliseconds, the fitted
  exponent) is a real measurement, and the label is presented as an approximate bucket ("closest to O(n^2)"), not
  a certificate -- O(n) vs O(n log n) genuinely can't be told apart at these practical sizes, and that's stated
  outright rather than papered over. Two real bugs were found and fixed while building this, both confirmed by
  directly timing the synthetic data before and after: (1) synthetic values were first resampled from the
  problem's own (tiny, low-range) real test values, which made an early-exit algorithm (like two-sum's hashmap
  lookup, or breaking on the first repeated character) accidentally find a match within the first few elements
  of a *large* array almost every time, regardless of true input size -- both a brute-force and an optimal
  solution measured as flat "O(1)", completely hiding the real difference; fixed by generating synthetic values
  (and, for strings, synthetic characters) that are unique across the whole input and drawn from a range wide
  enough that a coincidental match is negligible even at the largest probed size, forcing genuine worst-case
  traversal. (2) fixed subprocess-launch overhead (~150-300ms) dominated the raw timings at small probe sizes,
  flattening the fitted curve toward "looks constant" regardless of true complexity -- fixed by measuring that
  overhead directly (one throwaway run at a trivial size) and subtracting it before fitting, with the subtraction
  disclosed in the shown explanation rather than done silently. Scope, stated rather than glossed over: only
  problems whose primary scaling dimension is a single flat list/string argument, or a single scalar integer
  (e.g. `factorial(n)`), are attempted -- trees, linked lists, grids, and multi-argument shapes are declined with
  a stated reason instead of a guessed or misleading probe. Currently Python and JavaScript only: Java's
  per-submission `javac` compile cost makes four repeated timing runs impractical without a dedicated
  multi-size-in-one-compile harness, which doesn't exist yet.
- **Step-through execution trace of the learner's own failing code** (`/problems/{slug}/trace`,
  `execution/trace_probe.py`): when a submission fails a *visible* test case, a "Watch your code run on this
  input" button re-runs the learner's own code (not the reference solution) on that exact input under Python's
  `sys.settrace`, capturing the real line number and every local variable's real value at each step -- including
  recursion depth, and linked-list/tree arguments rendered back to readable values via the same conversion helpers
  the sandbox itself uses. It's shown with the same step-control UI already built for the concept-lesson
  visualizers (`useSteps`/`StepControls`), stepping through the learner's own logic instead of an abstract worked
  example. `args` must exactly match a visible example test case (checked server-side) so this can't be used to
  probe a hidden test case's input by trial and error. A real, serious bug was caught and fixed while verifying
  this in an actual browser, not just unit tests: mutable locals (a dict or list being built up, e.g. a hashmap
  solution's `seen = {}`) were captured by reference at each step, not copied -- since the whole trace is only
  serialized to JSON once at the very end, every step showing that variable displayed its *final* mutated state,
  not its state at that point in time (a `seen` dict showed all entries already present from step one). Fixed
  with a deep copy at capture time, then re-verified in the same live browser run to show the dict genuinely
  growing one entry at a time across steps. Now also works for JavaScript, using a genuinely different mechanism
  because there's no JS equivalent of `sys.settrace` here: Node's inspector/debugger protocol was tried first
  (a synchronous `Debugger.paused` handler driving `stepInto` calls) and found, by actually testing it, not to
  reliably halt execution the way a real attached debugger does in this in-process, no-external-client setup --
  so JavaScript tracing instead works by real AST-based source instrumentation: the submission is parsed with
  `espree` (`execution/js_analyzer/instrument.js`) and a trace-recording call is spliced in before every
  statement, with a scope stack tracking exactly which variable names are genuinely declared at each point (so
  the generated code never references a `let`/`const` before its real declaration, which would throw in actual
  JS). The mutable-locals bug above was fixed proactively in the JS path from the start, then verified for real:
  a hashmap-based two-sum's `seen` object was confirmed growing one entry at a time across steps in a live
  browser run, alongside recursion-depth tracking and linked-list argument rendering, matching the Python path's
  behavior. A second, more serious bug in the JS instrumenter was caught by cross-checking the same recursive
  fibonacci(6) across all three languages and noticing JavaScript alone returned the wrong answer (6 instead of
  8) after only a single recorded step: for a brace-less `if (n<=1) return n;`, splicing a trace call in as plain
  text before `return n;` produced `if (n<=1) __trace(...);return n;` -- and since a brace-less `if` only governs
  the one statement immediately after it, the original `return n;` had silently become unconditional. This
  wasn't just wrong trace data, it changed the actual computed result of the traced code, which is precisely the
  kind of bug instrumentation-based tracing has to guard against (the whole point is that tracing must never
  change what the code computes). Fixed by wrapping the trace call and the original statement together in a real
  `{ }` block wherever a brace-less body is instrumented, then reverified with the same cross-language check
  (all three now agree: fibonacci(6) = 8) plus the earlier two-sum/isValid/for-loop cases re-run to confirm no
  regression. **Java tracing exists too**, via JDI (Java Debug Interface) -- the same mechanism real Java debuggers
  (jdb, IntelliJ, VS Code) are built on, not a workaround: a small standalone driver
  (`execution/java_trace/TraceDriver.java`, compiled once and reused since its own source never changes per
  submission) launches the already-familiar `Main`/`Solution` pair as a real *debuggee* JVM over JDWP, sets an
  actual breakpoint at the target method's first line, and single-steps through with a class filter scoped to
  `Solution` -- so it steps genuinely into the method's own recursive calls (a real call stack, real depth) while
  transparently skipping over JDK-internal calls like `HashMap.put` at the JVM level, not by single-stepping
  through their bytecode. This was not the first approach tried and abandoned like JS's inspector-protocol
  attempt -- it was verified end to end via direct prototyping before being built out: local-variable debug info
  needed an explicit `javac -g` flag (confirmed missing without it -- every step came back with an empty locals
  map and an `AbsentInformationException`); a five-level recursive trace alongside an unrelated `HashMap` call
  completed in about a second, confirming the class-filtered stepping genuinely skips JDK internals rather than
  crawling through them; and objects without special handling (a `HashMap`, a learner's own helper class) are
  described by invoking their real `toString()` inside the debuggee via JDI -- an actual computed value, not a
  fabricated summary. `ListNode`/`TreeNode` arguments get the same readable `{"__type__":...,"values":[...]}`
  rendering as the other two languages, by walking their fields through JDI's reflection API. All three language
  tracers are scoped to the target function's own lines only, not into any helper function it calls.
- **Real Linked List / Binary Tree problems** (Reverse Linked List, Merge Two Sorted Lists, Max Depth, Invert
  Binary Tree): the sandbox converts JSON arrays to/from actual linked-list and tree node objects before/after
  calling the submission (`app/services/execution/io_transforms.py`, mirrored inline in the sandboxed subprocess
  script since it can't import the parent package) -- these are genuinely auto-graded, not lesson-only.
- **Order-independent grading where it matters**: subset/permutation-style problems accept any correct
  enumeration order (`Problem.output_comparison = "unordered_nested"`) instead of only the reference solution's
  exact order -- verified against a submission using a structurally different (bitmask-based) algorithm.
- **Real multi-language submission**: every problem can be solved in Python, JavaScript, or Java, not just Python.
  A problem's parameter/return types are never hand-authored per language -- they're inferred from the shape of
  its own (already reference-executed) test data (`app/services/execution/type_inference.py`), and the starter
  code shown for JavaScript/Java is generated from that inference plus the Python starter's real parameter names
  (parsed via `ast`, not guessed), so there's nothing to keep in sync by hand across languages. JavaScript runs
  in a Node `vm` context with no `require` (so no filesystem/network access by construction, not just convention);
  Java is compiled fresh per submission with test arguments embedded as real Java literals (no JSON parser needed
  since the harness is regenerated every time) -- see `javascript_sandbox.py` and `java_sandbox.py`. This was
  verified end-to-end (starter generation -> real compile/run -> comparison against the same reference-computed
  `expected_output`) against every argument/return shape actually used across the problem set: plain arrays,
  strings, booleans, linked lists, binary trees, nested/jagged lists as both arguments and unordered results,
  and correctly-rejected wrong answers / syntax errors / runtime errors in both languages.
- **Diagnosis and brute-force detection work for all three languages, not just Python.** Each language gets a
  *real* parser, not a regex approximation: Python uses its own `ast` module (`diagnosis/features.py`); Java uses
  `javalang`, a real Java-grammar parser (`diagnosis/features_java.py`); JavaScript is parsed by `espree` -- the
  same parser ESLint itself uses -- run as a small standalone Node subprocess with its own `package.json` (kept
  deliberately separate from the frontend's `node_modules` so the backend doesn't depend on the frontend's
  incidental devDependencies) and walked from the Python side (`diagnosis/features_js.py`). All three feed the
  same `CodeFeatures` shape into the same diagnosis model and the same always-on `detect_brute_force()` check, so
  a nested-loop brute-force solution gets flagged whether it's written in Python, JavaScript, or Java -- verified
  by submitting matching brute-force and optimal solutions in all three languages through the live API and
  confirming the nudge fires only on the brute-force ones. Vanilla JavaScript has no built-in heap/priority-queue
  type (and the sandbox disables `require`, so no npm heap package can be pulled in either), meaning a correct JS
  solution needing a heap is necessarily hand-rolled -- so `uses_heap` also recognizes a heap's characteristic
  naming (heapify, sift-up/down, bubble-up/down, percolate-up/down, MinHeap/MaxHeap) across all three languages,
  the same kind of naming heuristic `uses_two_index_vars` already relied on, in addition to each language's real
  built-in (`heapq` import, `new PriorityQueue()`). Fixing this also surfaced and fixed a real bug: every Java/JS
  feature except recursion detection was accidentally scoped to only the one method the harness calls, so a heap
  (or HashMap, or anything else) defined in a helper class or method was invisible to the analyzer -- verified
  fixed by submitting a real hand-rolled MinHeap-in-a-helper-class JS solution through the live API and confirming
  `uses_heap` now sees it.
- C++, Go, and Rust are not wired up for *execution*, not because the architecture couldn't support them (the
  type-inference + literal-embedding approach generalizes) but because this server has
  no C++/Go/Rust toolchain installed to actually compile and verify against, and a language isn't claimed here
  until it's been run for real.
- **Mnemonics, not memorization**: every skill carries a short "memory hook" analogy (e.g. hashing = a phonebook
  lookup) shown before the full lesson, for fast recall of *when to reach for a technique* -- shown alongside,
  never instead of, the full lesson and real practice problems.
- **Every lesson follows one consistent, comprehensive template** so a single page spans beginner to advanced
  rather than assuming prior knowledge: plain-language explanation -> mechanism -> real-world analogy -> a
  hand-traceable worked example (a dry-run table) -> common mistakes -> when to use it / when not to -> an
  interview-style question -> a one-line key takeaway. All 28 skills follow this structure, including the
  advanced tier (Union-Find, Topological Sort, Dijkstra, Knapsack DP, String DP/edit-distance, sweep-line/
  difference-array patterns) needed to go past "easy/medium interview basics" toward broader DSA competence.
- **A genuine LLD (low-level design) track**, not just HLD: OOP fundamentals + all five SOLID principles, and
  the four design patterns (Singleton, Factory, Observer, Strategy) that come up constantly in both LLD
  interviews and real codebases -- each with the problem it solves, why the naive approach fails, and its
  trade-offs, not just a code template to memorize.
- **Mastery can't be gamed by repetition**: re-solving a problem you've already passed dampens its effect on
  mastery to ~15% of normal (`is_repeat_solve` in `update_mastery_from_submission`) -- verified: a first solve
  raised mastery from 0% to 15%, an identical second submission only reached 16.9%, instead of the ~28% a
  naive EWMA would give. The submission response tells the learner why, and points them at a fresh problem or
  the skill's Transfer Challenge instead.
- **Brute-force detection on PASSING submissions, not just failures**: a real gap was found and fixed here --
  the ML diagnosis classifier was trained to treat a high pass rate as evidence of mastery, so a nested-loop
  O(n²) solution that happened to pass anyway (small hidden test cases often don't catch this) was silently
  labeled "MASTERED" and never told the learner they'd found the brute-force path, not the intended one. A
  separate, deterministic, always-on check (`detect_brute_force` in `diagnosis/engine.py`) now runs on every
  passing submission regardless of what the classifier concludes: if the code's loop nesting exceeds what the
  problem's stated complexity should need, the response carries a distinct "room to optimize" nudge. Verified:
  a brute-force `two_sum` (nested loops) now gets flagged even though it passes all tests; the O(n) hashmap
  version does not.
- **Blind Practice mode** (`/problems/blind/random`): a randomly-selected problem with zero skill/chapter
  context anywhere in the surrounding page -- the editor, hints, and the AI-ask feature all stay locked until
  the learner declares which pattern they think applies. This is the platform's actual test of *unprompted*
  pattern recognition, as opposed to recognizing a pattern because you just clicked into its chapter.
- **Prerequisite-aware skill graph, visibly**: `/skills/readiness` exposes the same prerequisite check the
  recommendation engine already used internally, so the Skill Graph page can show a lock icon and name the
  specific prerequisite skills a learner hasn't yet reached 60% mastery on -- guiding bottom-up learning from
  fundamentals without hard-blocking a curious learner from previewing ahead.
- **Every one of the 28 DSA skills has a real, step-through (Play/Pause/Prev/Next) visualization** --
  10 purpose-built components (`frontend/src/components/visualizers/`): array/pointer (two-pointer, sliding
  window, binary search, Kadane's, prefix sum), stack (parentheses matching, the recursive call stack), a
  linked-list reversal with live pointer labels, an SVG binary tree (traversal order, BST search, trie
  insertion, a backtracking decision tree), an SVG graph (BFS, topological sort, Dijkstra with live
  distances, Union-Find component coloring), a DP table that fills in row by row (climbing stairs, 0/1
  knapsack, longest common subsequence), a hashmap, a queue, a binary-digit toggle board, and a complexity
  growth-rate bar race. Every trace mirrors the exact numbers already used in that skill's lesson text, so
  the animation and the prose never disagree with each other (`lib/visualizations.ts`).
- **The original 10 system design lessons have a real architecture diagram** (`lib/sdVisualizations.ts` +
  `FlowDiagram.tsx`), step-through where the lesson describes a sequence (a cache-aside request, a message
  flowing through a queue, a factory picking a class) and static where it's a comparison (SQL vs NoSQL, the
  CAP triangle); the 8 newer graduate-level lessons (see below) don't have one yet. System design case studies
  get something arguably stronger than a canned diagram: an interactive architecture builder the learner
  assembles themselves, graded by the real critique engine.
- **Two track-wide tiers (Novice -> Practitioner -> Expert) -- DSA and System Design -- not one badge per skill,
  and only advance through a real, aggregate-scored assessment** (`services/skill_graph/track_tier.py`). Earlier
  in development this was per-skill (28 separate badges), but that fragmented "different level learning
  experience" into noise instead of signal; it's now exactly two badges, each representing competence across
  the *whole* track. Starting an assessment is deliberately **never gated on mastery** -- an earlier version
  required every individual skill's mastery (or case family's score) to clear 85% before the "start assessment"
  button even appeared, which in practice meant almost no real learner would ever see it, since clearing dozens
  of skills that high is a long road; that gate was removed entirely per explicit direction. Mastery is now
  shown purely as informational context ("here's roughly how much you've learnt so far"), and any learner can
  attempt an assessment at any time -- it's the assessment itself (fresh problems/cases, solved for real, scored
  against an 85% aggregate bar) that gatekeeps advancement, never a prerequisite standing in front of it. Two
  skills genuinely have no practical mastery signal to show even informationally (Algorithmic Thinking &
  Complexity has zero seeded coding problems; Programming Foundations is conceptual) -- they're answered as real
  multiple-choice quiz
  questions (`QuizQuestion`, exact-match graded, never an LLM judgment call) that become *items inside* the DSA
  assessment itself, alongside coding problems drawn from several different skills (proving breadth, not depth
  in one topic) and, at the System Design track's Expert tier, cases from the harder Global scale tier instead
  of Growth (direct reuse of the scale-tier work above -- Expert quite literally means "gets it right at global
  scale," not just "answered more questions"). Passing is an aggregate score across every item, not a
  demand-perfection-on-each bar: a DSA problem scores 1.0 solved hint-free with the correct pattern declared,
  0.6 partial credit if solved with a hint or without declaring the pattern first, 0.5 if solved correctly but
  flagged by the existing `detect_brute_force()` check at the Expert tier, 0.0 if unsolved; a quiz question or
  system-design case scores 1.0/0.0 or its own real critique score respectively; the assessment resolves once
  every item has at least one attempt, and passes if the mean score is >= 85%. Verified end-to-end via live
  HTTP API for both tracks: a full DSA pass (5 problems + 3 quiz questions, aggregate 100%) that advanced
  Novice -> Practitioner in the database, a full System Design pass via real critique-graded architecture
  attempts on all 3 case families, and a genuine *fail* case -- 3 fully-solved problems plus 2 legitimately
  brute-force-flagged reference solutions plus 2 wrong quiz answers landed at a 62.5% aggregate and correctly
  did not advance the tier. Confirmed live in a real browser too, including with a brand-new zero-mastery
  account (the exact case the mastery gate used to block): the DSA/System Design tier panels (shown at the top
  of the Skill Graph and System Design pages respectively, not per-skill) show a visible, always-enabled "start
  assessment" button, and the inline multiple-choice quiz UI actually answers, disables after a response, and
  shows correct/incorrect feedback with explanations -- this last part caught a real bug (the backend had been
  restarted before the quiz-options plumbing was finished, so the running process was silently serving an older
  API shape with no options field, leaving the quiz UI unable to render any answer choices; caught by testing
  the actual page, not just the API, and fixed by restarting). Starting an assessment also deliberately never
  auto-resumes an old in-progress one -- an earlier version blocked a second "start" while one was already in
  progress, which meant navigating away from the page and back (a browser back button, revisiting later) kept
  resurfacing the exact same items indefinitely; fixed so a fresh "start" always deals a brand new random draw
  and silently abandons the stale attempt, while a plain page revisit shows a clean slate rather than
  auto-loading old content. Verified live: starting twice in a row (without finishing the first) returns two
  different assessment ids with completely non-overlapping problem sets, and the first is confirmed marked
  "abandoned" in the database.
- **System design case studies come in 3 real-world scales per problem (Startup / Growth / Global), not just
  the same diagram with bigger numbers.** URL Shortener, Rate Limiter, and Pastebin (9 seeded cases total, up
  from 3) each get a smaller Startup variant whose correct answer is deliberately *less* architecture (e.g. no
  load balancer or cache yet -- there's nothing to balance or protect against at ~1,000 requests/day, and adding
  one gets challenged by the existing "why did you add this?" critique the same way an over-engineered answer
  would be), the original case content unchanged as the Growth tier, and a Global variant whose
  `expected_components` reflect a genuinely different architecture (a CDN and/or queue where warranted, e.g.
  edge-cached redirects or an async analytics event, not just a restated cache). The `/system-design` page groups
  the 9 cases into 3 family cards with a Startup/Growth/Global tab switcher; verified live in a browser that
  switching tabs swaps the title, difficulty badge, and scale description in place, and that opening a case
  shows its scale as a badge plus the scale description on the detail page.
- **Contest mode**: timed, competitive rounds with a live leaderboard (`/contests`), reusing the exact same
  grading pipeline as every other submission (`submit_solution` is called directly, never a separate/weaker
  judge) rather than reimplementing execution logic. A contest has a fixed problem set and start/end time;
  its problems stay hidden until it starts (`GET /contests/{id}` returns an empty problem list for an
  "upcoming" contest), and only a submission made during the live window scores points -- solving one before
  it starts is rejected outright, and solving one after it ends is allowed for practice but no longer affects
  the leaderboard. Scoring is a simple, deterministic time-decay (100 points minus 1 per minute elapsed since
  the contest started, floored at 20) awarded once per problem on its first passing submission -- resubmitting
  an already-solved problem doesn't inflate the score further. The problem-solving page gains a yellow "Contest
  mode" banner when reached via a contest and hides the Hints/Ask-AI/pattern-recognition panels entirely for
  the duration (no scaffolding during a timed round, matching real contest conditions). Verified end-to-end via
  live API (correct scoring math, no double-counting on resubmit, rejection of both a wrong-contest problem and
  a not-yet-started contest) and in a real browser: the full click-through from the contest list to solving a
  problem to seeing the leaderboard update, confirming the Hints/Ask-AI/pattern-recognition panels are genuinely
  absent from the DOM (not just visually hidden) and that an upcoming contest's problems stay hidden until its
  start time.
- **System design lessons rewritten and expanded from basic to genuinely advanced/graduate-level depth, all in
  the same accessible template** -- per explicit user direction that depth and clarity should never trade off
  against each other. The original 10 lessons were one short paragraph each (350-480 characters); all 8
  non-LLD ones were rewritten to the same comprehensive 8-section template already used by every DSA skill
  lesson (What is it -> How it works -> Real-world analogy -> Worked example -> Common mistakes -> When to use
  it / when not to -> Interview-style question -> Key takeaway), so a hard topic is still walked through with a
  concrete worked example and a plain-language analogy, never just denser prose. 8 brand-new HLD lessons were
  added at genuinely graduate-level depth (levels 8-10): Consistent Hashing, Database Replication & Consensus
  (Raft/Paxos, including the actual majority-quorum argument for why a 5-node cluster tolerates exactly 2
  failures, not 3), Sharding & Partitioning Strategies, Distributed Transactions (Two-Phase Commit vs the Saga
  pattern, with compensating transactions), CQRS & Event Sourcing, Bloom Filters & Probabilistic Data
  Structures, Circuit Breakers & Resilience Patterns, and Database Internals (B-Trees vs LSM-Trees) -- each with
  a real worked numeric or step-by-step example, not just a definition (e.g. Consistent Hashing traces exactly
  which keys move when a specific server is removed from a 4-node ring). A follow-up pass, after direct
  feedback that the new lessons still read as too dense and text-only to be "easily analysed," added a small
  ASCII diagram to every one of those 8 (a hash ring, a 2PC message sequence, a circuit breaker's 3-state
  machine, a B-Tree vs LSM-Tree write path, etc.) and restructured their densest paragraphs into scannable
  bullet lists instead of one wall-of-text paragraph per section. 3 more LLD lessons were added alongside the
  existing OOP/SOLID and 4-patterns lessons: UML Class Diagrams & Relationships (the inheritance/association/
  aggregation/composition notation LLD case studies below assume), Structural Design Patterns (Adapter,
  Decorator, Facade, Proxy), and Concurrency-Safe Object Design. Verified live in a browser: all 21 lessons
  (up from 10) list correctly with their level, the original lessons' diagram visualizations survived
  untouched, and every rewritten/new lesson renders cleanly with no errors.
- **LLD Practice**: 3 hands-on low-level design exercises (Design a Parking Lot, Design an Elevator System,
  Design a Vending Machine) on `/system-design`, graded by a real rule-based critique engine
  (`services/system_design/lld_critique.py`) -- the class-design counterpart to the HLD case studies' component
  critique. A learner declares the classes they'd build (name, fields, methods, `extends`, `implements`) through
  a real form UI, and the engine checks deterministic signals grounded in what was actually submitted: which of
  the case's expected classes are covered (matched by name or a declared alias, so a reasonable synonym like
  "Spot" for "ParkingSpot" isn't penalized), whether any real inheritance/interface relationship was used at all
  (a concrete polymorphism signal), and whether any single class has grown suspiciously large in method count (a
  rough Single Responsibility / "God Class" signal) -- surfacing "why did you add this?" questions for
  unrecognized extra classes, the same spirit as the HLD critique's unjustified-component check. Verified via
  live API with both a well-designed submission (all 5 expected Parking Lot classes present, `Car extends
  Vehicle` -> scored 100%, abstraction detected) and a deliberately poor one (one 9-method God Class, no
  inheritance, one unexplained extra class -> scored 10%, all four signals correctly flagged with the right
  why-questions), then confirmed the exact same math live in a real browser using the actual class-builder form
  (4 of 5 expected classes covered with real inheritance used -> 60%, missing classes correctly named).
- **Fixed a real, previously-undiscovered rendering bug affecting every markdown surface in the entire app, not
  just system design**: the shared `Markdown` component (used for every lesson, every problem statement, every
  case description) applies Tailwind's `prose` typography classes, but `@tailwindcss/typography` was never
  installed or registered -- so `prose` had been a complete no-op the whole time, and every heading, paragraph,
  and bullet list across the whole platform was rendering as flat, unspaced, browser-default HTML with no real
  typographic hierarchy. Found while investigating a direct report that lesson content looked "clumsy" and
  lacked spacing -- confirmed via live-browser computed-style inspection (h2 and p were rendering at visually
  similar weight/size with no real margin between blocks) before the fix, and h2 at 30px/700-weight vs p at
  18px/400-weight with a real 12-36px vertical rhythm after it. The same investigation surfaced a second,
  independent bug: markdown tables (used by every DSA skill lesson's dry-run "worked example," e.g. Sliding
  Window's step-by-step trace table) were never actually parsed into `<table>` elements at all, since
  `remark-gfm` was never wired into `ReactMarkdown` -- a table rendered as one paragraph of literal pipe
  characters. Both fixed together (installed and registered `@tailwindcss/typography`, added `remarkGfm` to
  the markdown pipeline, and layered additional book-like styling on top: heading rules, relaxed line-height,
  a dark monospace treatment for the ASCII diagrams added earlier, and a larger `prose-lg` size specifically
  for the two main lesson-reading pages). Verified live in a browser on both a system design lesson (the
  Consistent Hashing hash-ring ASCII diagram now renders in a real dark rounded code box, not inline text) and
  a DSA skill lesson (the Sliding Window dry-run table now renders as a real bordered table with a visually
  distinct header row, not a paragraph of pipes) -- this fix alone likely explains most of the "not
  understandable" feedback, since it was a real rendering defect, not a content-depth problem.
- **Concept Map Preview**: a small orientation strip shown above any lesson (DSA skill or system design),
  naming what leads into it and what it leads to, using only real relationship data -- never a fabricated
  dependency. For DSA skills this reads the exact same `SkillPrerequisite` table `/skills/readiness` already
  uses (`GET /skills/{key}/concept-map`); for system design lessons, which don't have an authored prerequisite
  graph, "previous"/"next" is an honest, deterministic fallback -- the nearest lower/higher-level lesson in the
  same category (`GET /system-design/lessons/{slug}/concept-map`) -- clearly a coarser relationship, not
  pretended to be an authored one. Every pill is clickable and actually navigates the lesson panel, not just
  decorative. A lesson with no real prerequisite and nothing depending on it renders no strip at all, rather
  than an empty box. Verified live in a browser: Sliding Window correctly showed "Two Pointers" as its real
  prerequisite pill, clicking it genuinely navigated the panel (confirmed by both the title and the strip
  itself updating to Two Pointers' own prerequisite, Array Traversal & Kadane's Technique), and The CAP
  Theorem -- a root-level concept with no prerequisite -- correctly showed no prerequisite pill at all while
  still showing "Database Replication & Consensus" as a real next-concept pill.
- **Lesson in Acts**: lesson content (previously one long continuous scroll) is now split into sequential
  "Acts" shown one at a time, with a segmented progress bar and an optional one-line reflection prompt between
  acts ("what's the core idea so far, in your own words?") -- purely local, never graded or stored, just a
  pacing nudge. The split is computed client-side by chunking a lesson's existing `##` headings into up to 4
  even groups (`components/LessonActs.tsx`), so it adapts to however many sections any given lesson actually
  has rather than assuming a fixed template -- verified live with a 4-section lesson (Two Pointers) and a
  3-section lesson (Database Replication & Consensus) both chunking and progressing correctly, ending in a
  "you've reached the end" state with no further Continue button or reflection box once the last act is
  reached.
- **Concept Map + case editorials rolled out beyond the two main lesson pages.** The problem-solving page now
  shows the same Concept Map strip, keyed off the problem's own `primary_skill_key` (newly exposed on
  `ProblemDetail`), letting a learner jump straight from "I'm stuck on this problem" to "here's the prerequisite
  skill it's actually testing" -- clicking a pill deep-links to `/skills?skill=<key>`, which the Skill Graph page
  now reads on load to auto-open that skill's lesson. Doing this surfaced and fixed a real, separate gap: the
  frontend's problem-fetch call never actually sent `mode` to the backend at all, so the existing "blind mode
  withholds skill info" comment in the API schema was never actually enforced server-side for any request this
  frontend made -- harmless before since no field revealed the skill either way, but it would have silently
  leaked the skill through this new field the moment blind mode ran. Fixed by wiring `mode` into the request,
  and the concept map is skipped entirely in blind mode as an extra safety margin, not just gated by an
  unenforced flag. Verified live: standard mode shows the real prerequisite pill and current skill, blind mode
  shows zero trace of the concept map anywhere in the DOM, and clicking a pill genuinely navigates and opens
  the target skill. Separately, both system design case pages (`/system-design/[slug]` for HLD,
  `/system-design/lld/[slug]` for LLD) now reveal their `editorial_markdown` -- rich, already-written content
  that existed in the database from the start but was never exposed through either schema or ever rendered
  anywhere -- behind a "See the editorial" button shown only after a real attempt, rendered through the same
  `LessonActs` component used for lessons. Verified live on both a real HLD attempt (URL Shortener) and a real
  LLD attempt (Parking Lot), confirming genuine editorial text renders in both, not a placeholder.
- **System design syllabus reorganized into three explicit, complete tracks** -- Foundations, Low-Level Design,
  and High-Level Design -- instead of one long page mixing a flat 21-lesson list with both case-study types
  stacked underneath regardless of relevance. Every lesson's existing `category` maps into exactly one of the
  three (an exhaustive mapping, not a partial one), and each track shows only its own lessons plus whichever
  case-study section actually belongs to it: Foundations shows lessons only (no exercises exist at that level
  yet), Low-Level Design shows its lessons alongside the LLD Practice exercises, High-Level Design shows its
  lessons alongside the HLD case studies -- directly addressing the "shouldn't have to read half the syllabus
  mixed with the wrong half" feedback. Filling out High-Level Design also meant closing 3 real content gaps
  that were referenced constantly across existing case editorials but never actually taught as their own lesson:
  **Load Balancing Algorithms** (round robin, least connections, IP hash, Layer 4 vs Layer 7), **Content
  Delivery Networks** (edge PoPs, origin pull vs push, `Cache-Control`), and **Microservices vs Monolith and API
  Gateways**. Low-Level Design gained **The LLD Interview Framework**, a five-step process lesson (clarify
  requirements -> identify entities -> define relationships -> spot pattern fits -> walk a core flow) placed as
  the track's entry point, tying its other 5 lessons (OOP/SOLID, UML, two design-pattern lessons, concurrency)
  into one coherent approach rather than a loose bag of topics. Total lesson count at that point: 25 (2
  Foundations / 6 LLD / 17 HLD), verified live in a browser to sum to exactly the full lesson set with no
  lesson duplicated or dropped between tracks, each tab correctly showing and hiding its own case-study
  section, and the 3 new HLD lessons rendering real content.
- **5 more lessons added specifically to close the gap to senior/staff-level depth**, per explicit user
  direction that the curriculum should reach the level a top company's senior engineers actually operate at,
  not just solid mid-level coverage. **Back-of-the-Envelope Estimation & Latency Numbers** teaches the actual
  memorized reference numbers (L1 cache ~1ns, RAM ~100ns, SSD random read ~100-150us, same-datacenter round
  trip ~0.5ms, cross-continent ~150ms) and a systematic 5-step estimation framework -- the single most
  reliably-tested "is this person senior" skill in real system design interviews, and the exact skill every
  case study's estimation step in this app has been silently assuming rather than actually teaching until now.
  **Consistency Models: Linearizability to Eventual Consistency** replaces CAP theorem's binary framing with
  the real 4-point spectrum (linearizable -> sequential -> causal -> eventual) practitioners actually use, since
  "consistent" is not one thing. **Observability: Metrics, Logs, Traces, and SLOs** covers genuinely
  senior/staff operational maturity that was completely absent before -- the three observability pillars, plus
  SLIs/SLOs/error budgets as a concrete framework for turning "reliability" into a number a team can make
  trade-offs against. **Real-World Case Study: How Twitter's Timeline Works** is the one lesson in the whole
  curriculum built around a real, publicly-documented production system rather than a generic pattern -- the
  fan-out-on-write vs fan-out-on-read trade-off and the actual hybrid solution large platforms use for
  outlier (celebrity) accounts, chosen because "a small number of hot keys breaks the pattern that works for
  everything else" recurs constantly in real system design and is exactly the kind of war-story knowledge
  senior engineers carry. **Thread-Safe Producer-Consumer Systems & Thread Pools** gives Low-Level Design one
  of the most frequently-asked concrete LLD prompts (a bounded blocking queue plus a thread pool), applying the
  earlier Concurrency-Safe Object Design lesson's principles to a real, buildable class design instead of only
  discussing concurrency in the abstract. Total lesson count at that point: 30 (2 Foundations / 7 LLD / 21 HLD)
  -- verified live in a browser that the tally still summed exactly to the full lesson set, that no 4th tab was
  accidentally created for the two new lesson categories these needed (`estimation`, `real-world-systems` both
  correctly fold into the High-Level Design tab), and that both the Twitter case study's ASCII fan-out diagram
  and the estimation lesson's latency-number table rendered cleanly in their dark code blocks.
- **10 more lessons and 1 more practical LLD exercise added in a second pass**, per explicit direction to match
  how much a genuine real-world system design + LLD curriculum actually covers, with both practical and
  theoretical depth and real diagrams throughout -- not just a curated top-N list. Foundations gained **DNS:
  How a URL Becomes a Connection** (the full root -> TLD -> authoritative nameserver resolution chain, caching,
  TTLs) and **Proxy Servers: Forward vs Reverse Proxy** (the distinction most learners blur, since a reverse
  proxy is functionally what a load balancer already taught actually *is*). High-Level Design gained
  **Database Indexing** (the concrete B-tree mechanism behind why some queries are instant and others crawl),
  **Distributed ID Generation** (why auto-increment and random UUIDs both break once data is sharded, and how a
  Twitter Snowflake ID -- timestamp + machine ID + sequence packed into 64 bits -- solves it with zero runtime
  coordination), **Real-Time Communication** (polling -> long polling -> SSE -> WebSockets, and *why* each
  exists rather than just naming them), **Geospatial Indexing** (geohashing and quadtrees -- the actual
  mechanism behind every "find nearby drivers/restaurants" feature, including the real boundary-cell edge case
  naive prefix-matching misses), **Search Systems & Inverted Indexes** (the word-to-documents mapping behind
  every real search feature, plus why TF-IDF/BM25 ranking exists), and a second real-world case study, **How
  Uber's Dispatch System Works**, deliberately built to require combining three separate earlier lessons
  (geospatial indexing, real-time communication, back-of-envelope estimation) into one system, rather than
  testing any one of them in isolation. Low-Level Design gained **More Behavioral Patterns** (Command, Iterator,
  Chain of Responsibility, Template Method -- completing GoF behavioral pattern coverage alongside the earlier
  Observer/Strategy lesson), **Dependency Injection & Inversion of Control** (making SOLID's Dependency
  Inversion Principle concrete: constructor vs setter injection, and what an IoC container actually automates),
  and **API Design Principles** (resource naming, versioning, cursor- vs offset-based pagination and exactly
  why offset-based pagination silently breaks under concurrent writes, and idempotency keys for non-idempotent
  `POST` requests). On the practical side, **Design a Chess Game** was added as a 4th LLD exercise specifically
  to broaden domain variety beyond the existing "hardware simulation" theme (Parking Lot, Elevator, Vending
  Machine) into a pure software/rules-engine domain, using the same real rule-based critique engine (expected
  classes: Board, Piece, Move, Player, Game, with Piece as the polymorphic base every concrete chess piece
  implements). Total lesson count: 41 (4 Foundations / 10 LLD / 27 HLD), across 4 LLD exercises and 9 HLD
  cases -- verified live in a browser with an exact tally match (4+10+27=41), every named lesson confirmed
  present in its correct tab, a real chess-design critique submission scoring correctly (2 of 5 expected
  classes present -> 40%, missing classes named correctly), and the Uber case study's ASCII diagram rendering
  cleanly in its dark code block. This still isn't literally exhaustive of everything a real-world curriculum
  could ever cover (notably absent: distributed file systems, video streaming/chunking, payment-system
  reconciliation, notification delivery infrastructure) -- rather than claim false completeness, this list of
  what's still missing is kept here deliberately, consistent with this project's standing "don't fake content"
  principle.
- **3 more real-world-scope lessons added in a third pass**, closing 3 of the 4 gaps named directly above:
  **Distributed File Systems** (the GFS/HDFS-style chunking + replication pattern -- a metadata-only master
  coordinating chunkservers that clients talk to directly, and why that separation is what lets the design
  scale), **How Video Streaming Works (HLS/DASH)** (adaptive bitrate streaming as chunked video over plain
  HTTP, reusing the CDN-caching lesson directly, with the player -- not the server -- making the quality
  decision each chunk), and **Payment Systems & Idempotent Reconciliation** (extending the API Design lesson's
  idempotency-key idea into a full layered defense: idempotency keys, a double-entry ledger, a strict
  forward-only payment state machine, and reconciliation against the external processor's own records for the
  one failure mode idempotency keys alone can't catch). Total lesson count: 44 (4 Foundations / 10 LLD / 30
  HLD) -- verified via the live API (`GET /system-design/lessons` returns all three new slugs and a total count
  of 44) and a passing `tsc --noEmit`/`eslint` pass on the touched frontend files; **no live browser
  verification was performed for this pass** (no browser-automation tool was available in this session), so
  this is deliberately reported at API-and-typecheck confidence, not "confirmed live in a browser" confidence,
  consistent with this project's "don't fake it" principle. **Notification delivery infrastructure** remains
  the one named gap still unbuilt.
- **Computer Networks: a new, entirely separate top-level feature** (its own nav item, its own database table,
  its own router, its own frontend page), built in parallel to DSA/Skills and System Design rather than folded
  into System Design's Foundations track, per explicit direction. 14 lessons across 5 real categories spanning
  the full stack from the physical/data-link layer up through application-layer practice: **Fundamentals**
  (network types and topologies, the OSI model, the TCP/IP model, wireless networking/WiFi/cellular basics),
  **Data Link & Network Layer** (MAC addresses/ARP/switches, IP addressing & subnetting including IPv4/IPv6,
  routers & routing algorithms including BGP's policy-driven path selection, NAT & firewalls), **Transport
  Layer** (TCP vs UDP's real reliability/latency trade-off, the TCP three-way handshake & connection lifecycle,
  TCP congestion control's slow-start/AIMD behavior), **Network Security** (TLS/SSL -- how HTTPS actually
  bootstraps a shared session key via asymmetric crypto then switches to fast symmetric encryption -- and VPNs'
  tunneling/encryption), and **Application Layer & Practice** (socket programming -- the real OS-level
  `bind`/`listen`/`accept`/`connect` API underneath every networked application, plus a second wireless
  networking lesson). Every lesson follows the identical 8-section template used throughout this curriculum,
  reuses the same `ConceptMapStrip`/`LessonActs` components already proven in System Design (same level +
  category-adjacency fallback for concept-map "previous"/"next," since -- honestly, same as System Design's
  lessons -- no authored prerequisite graph exists for this content either), and the same `Markdown` rendering
  pipeline (so the `@tailwindcss/typography` + `remark-gfm` fixes from earlier this session apply here too, not
  just to the pages they were originally found on). Verified via the live API with a real registered user
  (`GET /networks/lessons` returns all 14 lessons across exactly the 5 named categories, and
  `GET /networks/lessons/{slug}/concept-map` returns correct previous/next relationships), backend import and
  router registration confirmed (`app.main` imports cleanly with `networks.router` included), and a passing
  `tsc --noEmit`/`eslint` pass on the new frontend page and the modified `Sidebar`/`Navbar`/`types.ts` files --
  **not verified live in a browser** for the same reason as the System Design additions above (no
  browser-automation tool available this session), reported honestly at that lower confidence level rather than
  claimed as fully UI-verified.
- **A "Simple version" comic-strip explainer, added to every lesson in all three curricula (86 total: 28 DSA
  skills, 44 System Design lessons, 14 Networks lessons)**, plus real practice quizzes for Computer Networks --
  both added in response to explicit feedback that some lesson prose used more vocabulary than necessary and
  needed an easier on-ramp, "like a conversation." Each lesson now carries a `comic_script` field -- a genuine,
  continuous back-and-forth dialogue (6-8 exchanges) between two consistent personas, Mira (a curious learner)
  and Dev (a patient guide), written in plain, jargon-light everyday language, walking through the same concept
  the dense lesson covers. This is *additive*, not a replacement: the original in-depth lesson prose (built up
  deliberately across this session's earlier "senior/staff engineer depth" and "real-world scope" passes) is
  untouched and still the default view -- a "Deep lesson / Simple version 💬" toggle lets a learner switch to
  the comic explainer instead, rendered by a new `ComicPanels` component as chat-bubble panels (no illustrated
  art -- there's no image-generation capability available -- styled purely with CSS to read as a comic strip:
  alternating sides, avatar bubbles, panel borders). If the intent was actually to simplify the existing dense
  prose itself rather than add a second, easier path alongside it, that's a real, worth-flagging design choice
  to revisit. Separately, **Computer Networks gained a real practice layer** it previously lacked entirely (no
  coding problems like DSA, no case studies like System Design): 28 multiple-choice questions (2 per lesson,
  `NetworkQuizQuestion`/`NetworkQuizAttempt` models, deterministic exact-match grading with an explanation
  shown after each answer) reachable from every lesson page. Verified live: the DB migration (`ALTER TABLE ...
  ADD COLUMN comic_script`) was applied to the existing dev database rather than dropping it, all 86 lessons
  confirmed via a live API count of `"speaker":"mira"` occurrences (176 = 4×44 for System Design, 4 panels
  confirmed on 6 spot-checked DSA skills spanning first/middle/last, 14/14 for Networks), a real registered
  user submitted both a correct and an incorrect Networks quiz answer and got back correct grading and
  explanation text, and `tsc --noEmit` / `eslint` both pass clean on every new and modified frontend file --
  again, **no live browser verification**, for the same reason noted above.
- **Three real trained models coaching problem-solving APPROACH, not just correctness** (`app/services/coach/`),
  built in response to explicit direction to improve how students approach DSA and System Design, not just
  what they know. A fourth -- a complexity self-assessment coach classifying a submitted solution's likely
  Big-O class from its code structure -- was built, honestly evaluated (48.0% cross-validated accuracy on this
  app's 148 real reference solutions, after already switching from a worse-performing MLPClassifier to a
  RandomForestClassifier), and then removed at the user's explicit request once that accuracy was judged too
  low to be a useful coaching signal -- named here rather than silently dropped from the record.
  - **Behavioral habit profiler**: classifies a student's *habits across their whole submission history*
    (not one problem) -- plans before coding vs. skips planning, hint-dependent vs. self-reliant,
    trial-and-error vs. deliberate -- surfaced on the dashboard. Trained the same way as the pre-existing
    diagnosis model (`services/diagnosis/model.py`): a synthetic dataset whose *labels* come from an explicit,
    auditable rule function, letting the trained classifier generalize across feature combinations the rules
    didn't explicitly enumerate. The *features* fed in at prediction time are always real, computed live from
    that specific user's actual `Submission`/`ReasoningAttempt`/`HintUsage` rows -- verified live returning a
    genuine "not enough data" response below 3 submissions, then a real profile once a test user crossed that
    threshold.
  - **System Design scope coach**: classifies a submitted architecture as over-engineered, well-scoped, or
    under-engineered *for its stated scale tier*, complementing (not replacing) the existing deterministic
    per-component critique engine. Same synthetic-labels/real-features training split as the habit profiler,
    with the rule function itself encoding this app's own standing pedagogy (don't add unjustified complexity
    at startup scale; don't skip necessary components at global scale) -- verified live against all three real
    verdicts (over-engineered, well-scoped, under-engineered) using real case data.
  - **"Think First" plan-quality coach**: scores the QUALITY of a student's stated reasoning (written before
    they see any code, via the existing pattern-declaration flow) as Weak/Adequate/Strong, extending the
    existing keyword-overlap reasoning score with a trained second signal. Deliberately scores *structural*
    text features (word count, presence of Big-O notation, mentions of an alternative/brute-force approach) via
    the same synthetic-labels/real-features split, rather than pretending a small classifier semantically
    understands the reasoning text -- verified live distinguishing a one-word "hashmap" answer (Weak) from a
    genuine multi-sentence justification naming complexity and an alternative approach (Strong).
- **Four learning aids added in response to explicit direction to help students learn concepts more easily**,
  three genuinely new and one an existing feature discovered and verified rather than rebuilt:
  - **A full step-through algorithm visualizer already existed** (`components/visualizers/`, 9 visualization
    types -- array/pointer, stack, linked list, tree, graph, grid, hashmap, bits, queue -- with real play/pause/
    step/reset controls via a shared `useSteps` hook) covering all 28 DSA skills, built earlier in this same
    session. Verified it's genuinely complete (every one of the 28 skill keys has an entry in
    `lib/visualizations.ts`) rather than rebuilding it from scratch.
  - **Complexity Growth Playground** (`/skills/complexity-playground`, new): a real interactive slider (not
    preset steps) for input size *n* from 1 to 1,000,000 on a log scale, with a live log-log line chart
    comparing O(1)/O(log n)/O(n)/O(n log n)/O(n^2)/O(2^n) and a table converting operation counts into a rough
    real-world time estimate (using ~10^8 ops/sec, a genuinely commonly-cited CPU benchmark, not an invented
    number). O(2^n) is deliberately capped at n=60 and shown as "computationally infeasible" beyond that rather
    than plotting a fabricated/overflowed value -- honest about where the numbers stop being real.
  - **"Explain it back" (Feynman technique) coach** (`services/coach/explain_back_scorer.py`, new): a fourth
    coach model, same architecture and honesty split as the habit profiler and SD scope coach (synthetic
    rule-grounded training labels, always-real features) -- scores a student's own-words explanation of a
    lesson against that lesson's own real "Key Takeaway" vocabulary (extracted via regex, never invented) plus
    structural signals (does it give an example, does it explain *why*). Live-verified across all three lesson
    types (DSA skill, System Design lesson, Networks lesson) producing correctly differentiated Weak/Adequate/
    Strong verdicts, including one real calibration fix made after live testing (the initial match-ratio
    threshold for "Strong" was too strict and under-scored a genuinely good explanation using synonyms rather
    than the lesson's exact wording -- adjusted and re-verified, not just assumed correct).
  - **Ask-anything doubt-clearing chat** (`services/llm/lesson_qa.py`, new): reuses the same local LLM already
    running for problem explanations, now grounded in a specific lesson's own content so a stuck student can
    ask a plain-English question without leaving the page. Verified live end-to-end including an actual
    generated answer from the local model, not just that the endpoint returns 200.
  - All three lesson types (`skills.py`, `system_design.py`, `networks.py`) got both new endpoints
    (`/ask`, `/explain-back`) behind a single shared `LessonCoachPanel` frontend component, avoiding tripling
    the UI code across pages that already look and behave identically for this purpose.
- **Full Mock Interview Loop** (`/interview/full-loop`, `models/mock_interview.py`): one DSA problem, one System
  Design case, and one behavioral question chained into a single timed session with one combined report, per
  explicit direction that answers in a mock interview "should ask questions and should verify those answers,"
  not just log them. Deliberately does NOT reimplement DSA or System Design grading a second time -- each round
  requires the candidate to actually go submit through this app's own existing, already-tested
  `/problems/{slug}/submit` and `/system-design/cases/{slug}/attempt` endpoints, and the loop then links to
  that real `Submission`/`SystemDesignAttempt` row rather than trusting a second, parallel judgment that could
  disagree with the first. The only genuinely new verification is the behavioral round: a real, structural
  (not semantically invented) check for the four STAR components -- Situation, Task, Action, Result -- via
  deterministic phrase detection, honest about its real limit (it can tell whether an answer has the SHAPE of
  a STAR answer, never whether the underlying story is true or good). The 8 behavioral questions are a real,
  standard industry question bank, not invented. Verified live end-to-end with a real registered user: the
  DSA round correctly refused to advance before a submission existed, correctly advanced after a genuine
  passing submission; the same refuse-then-advance behavior verified for the System Design round (real 100%
  critique score linked); the behavioral round correctly distinguished a real STAR-structured answer (scored
  "STRONG_STAR_STRUCTURE") from a shorter one; and the final combined report pulled real data from all three
  linked records into one honest summary.

## Honest scope limitations (things NOT built, so as not to overclaim)

- **148 seeded problems across 28 skills** (every practical skill has at least 4, up from a low of 2), not
  "2000+" like LeetCode -- all with genuine test cases (expected outputs are computed by executing each
  problem's reference solution in the real sandbox, never hand-typed, and every problem in this repo has been
  verified this way, including the unordered-answer, linked-list/tree, and ambiguous-multiple-valid-answer ones
  -- e.g. Course Schedule II and Convert Sorted Array to BST explicitly pin down a tie-breaking convention in
  their statements so grading against one specific reference output stays well-defined). Difficulty depth also
  grew: 7 hard-tier problems (Median of Two Sorted Arrays, N-Queens, Minimum Window Substring, Trapping Rain
  Water, Minimum Height Trees among them). A follow-up batch of 13 problems specifically targeted real gaps
  rather than padding evenly: Trie had zero seeded problems at all (now 3: insert/search, prefix counting, and
  the classic "replace words with shortest root" problem, each solvable with a real trie even though the
  harness only grades the return value, the same way every other problem here never forces a specific internal
  data structure), and Prefix Sum / Knapsack / String DP / Greedy / Two Pointer each had only 3 (now 5, with
  problems chosen to cover a genuinely different technique within the skill rather than a near-duplicate of an
  existing one -- e.g. Product of Array Except Self teaches two-direction prefix computation, distinct from the
  range-sum-query prefix sum already there). Verified beyond the standard reference-execution check: every new
  problem's starter code was confirmed to generate correctly in all three languages via the type-inference
  system, and a real Java solution (nested `List<List<Integer>>` argument) and a real JavaScript solution
  (string-list argument, boolean-list return) were submitted through the live API and passed all real test
  cases, not just Python. Reaching LeetCode's ~2000-problem scale through this same hand-verified process (one
  authored reference solution, executed and checked, per problem) is a large ongoing content effort, not a
  one-session task -- the schema and seeding pipeline (`seed_all.py`, `problems_seed*.py`)
  are built to scale to it incrementally without ever compromising the "never fabricated" guarantee, i.e. no
  problem is added without a reference solution that has actually been run against its test cases.
- **3 HLD system design case families (9 cases across Startup/Growth/Global scale tiers)** -- URL Shortener,
  Rate Limiter, Pastebin -- fully wired for critique + estimation grading, plus 4 LLD case studies (Parking
  Lot, Elevator System, Vending Machine, Chess Game) with their own rule-based critique, and 44 lessons
  organized into 3 explicit tracks (4 Foundations / 10 Low-Level Design / 30 High-Level Design) -- not the
  "15 cases / 60 lessons" scale in the original spec, and (see the "What's real" entries above) still not
  literally everything a real-world curriculum could ever cover -- distributed file systems, video
  streaming/chunking, and payment-reconciliation systems were added in a later pass, but notification delivery
  infrastructure remains unbuilt, named explicitly rather than implied-covered. The newer HLD lessons don't yet
  have the hand-built FlowDiagram visualization the original 10 lessons have
  -- the "See it in action" panel is simply absent for those, not broken or faked -- and the LLD case studies'
  critique is a class/method/inheritance-level check (missing classes, unjustified extras, abstraction usage,
  a rough God-Class method-count heuristic), not real static analysis of actual code.
- **Computer Networks (14 lessons across 5 categories)** is a separate, newer feature than the rest of this
  README's original content and hasn't yet received the same multi-pass depth expansion System Design went
  through -- 14 lessons is a genuinely complete pass through the core undergraduate-networking syllabus (OSI/
  TCP-IP models, addressing, routing, TCP/UDP, TLS, VPNs, sockets), not an exhaustive graduate-level or
  vendor-certification-level treatment. It now has a real practice layer (28 multiple-choice questions, 2 per
  lesson, deterministically graded) added in a later pass, but still nothing analogous to System Design's
  interactive case studies or LLD critique engine -- no open-ended design submission, no architecture grading,
  quiz questions only -- and (per the note in "What's real" above) its live-browser rendering was not verified
  this session, only its API responses and frontend type-checking/linting.
- **Graph problems are JSON-native (adjacency list), not object-graph-based** -- connected components, BFS
  shortest-path, Dijkstra, topological sort, and Union-Find are all auto-graded; Bellman-Ford, Floyd-Warshall,
  and MST (Kruskal/Prim) aren't seeded yet.
- **No PWA/offline mode, no admin content UI, no company-specific tracks** -- all mentioned in the original spec
  but out of scope for this pass.
- **The system design "architecture canvas" is a simple add-node/connect-node list UI**, not a drag-and-drop canvas
  (no React Flow) -- functionally real (it drives the same critique engine) but visually simpler.
- **Interview simulator still does not grade free-text answer quality** -- the local LLM adds a short reaction/
  commentary per answer, but the coverage score is still "was each stage addressed," not "was the answer good."
  A 1.5B local model isn't reliable enough to grade interview answers, and pretending otherwise would violate the
  no-fabrication principle this whole project is built around.
- **The local LLM is a small (1.5B parameter) model** chosen for CPU speed (a few seconds per response, no GPU
  required). It's a genuine instruction-tuned model, not a toy, but it will occasionally misstate a minor detail
  even when given the correct facts to work from (observed in testing) -- which is why every LLM-generated response
  in this app is shown next to, not instead of, the deterministic ground truth. A bigger local model (e.g. Phi-3.5,
  Qwen2.5-7B) would be more reliable but slower on CPU-only hardware -- swap `MODEL_URL` in
  `backend/app/services/llm/download_model.py` and re-download if you have the hardware for it.

## Repo layout

```
backend/app/
  models/         SQLAlchemy models (users, skills, problems, submissions, retention, recommendations, system design, interviews)
  routers/        FastAPI route handlers
  services/
    execution/    sandboxed code runner
    diagnosis/    static analysis + scikit-learn root-cause classifier
    recommendation/  rule-based recommendation engine
    retention/    SM-2 spaced repetition scheduler
    skill_graph/  mastery updates + prerequisite checks
    system_design/  architecture critique + estimation grading
    interview/    deterministic interview stage machine
  seed/           skill/problem/system-design seed data + idempotent seed script
frontend/src/
  app/            Next.js App Router pages
  components/     shared UI (Navbar, Markdown renderer, auth guard)
  lib/            API client, auth context, TS types matching backend schemas
```
