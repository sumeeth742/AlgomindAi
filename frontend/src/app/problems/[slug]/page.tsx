"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useParams, useRouter, useSearchParams } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import dynamic from "next/dynamic";
import Link from "next/link";
import {
  ActivitySquare, Brain, CheckCircle2, Clock, EyeOff, Gauge, Lightbulb, Lock, Play, RotateCcw,
  Shuffle, Sparkles, Trophy, XCircle, Zap,
} from "lucide-react";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import { ConceptMapStrip } from "@/components/ConceptMapStrip";
import { Markdown } from "@/components/Markdown";
import { AiLabel, Badge, Button, Card, Spinner } from "@/components/ui";
import { api } from "@/lib/api";
import {
  AskResponse, ComplexityCheckResponse, ConceptMapOut, ExplainResponse, ProblemDetail, ReasoningSubmitResponse,
  RunResponse, SubmissionHistoryItem, SubmitResponse, TestResultOut, TraceResponse,
} from "@/lib/types";
import { OwnCodeTrace } from "@/components/visualizers/OwnCodeTrace";

const MonacoEditor = dynamic(() => import("@monaco-editor/react"), { ssr: false });

const DIFFICULTY_TONE: Record<string, "emerald" | "amber" | "red" | "purple"> = {
  easy: "emerald", medium: "amber", hard: "red", expert: "purple",
};

const MONACO_LANGUAGE: Record<string, string> = {
  python: "python", javascript: "javascript", java: "java",
};

const LANGUAGE_LABEL: Record<string, string> = {
  python: "Python", javascript: "JavaScript", java: "Java",
};

// Plain-English versions of the diagnosis engine's internal category names,
// so a learner sees "Too slow for this problem's constraints" instead of the
// raw label "TIME_COMPLEXITY".
const DIAGNOSIS_LABEL: Record<string, string> = {
  MASTERED: "You've got this down",
  CONCEPT_GAP: "Missing concept",
  PATTERN_RECOGNITION: "Didn't spot the right approach",
  IMPLEMENTATION: "Implementation slip",
  TIME_COMPLEXITY: "Too slow for this problem's constraints",
  EDGE_CASE: "Missed an edge case",
  HINT_DEPENDENCY: "Leaned on hints",
};

function relativeTime(iso: string): string {
  const diffMs = Date.now() - new Date(iso + "Z").getTime();
  const mins = Math.floor(diffMs / 60000);
  if (mins < 1) return "just now";
  if (mins < 60) return `${mins}m ago`;
  const hours = Math.floor(mins / 60);
  if (hours < 24) return `${hours}h ago`;
  return `${Math.floor(hours / 24)}d ago`;
}

function CaseTabs({ count, selected, onSelect, results }: {
  count: number; selected: number; onSelect: (i: number) => void; results?: TestResultOut[];
}) {
  return (
    <div className="flex flex-wrap gap-1.5">
      {Array.from({ length: count }, (_, i) => {
        const result = results?.[i];
        const tone = result ? (result.passed ? "emerald" : "red") : null;
        return (
          <button
            key={i}
            onClick={() => onSelect(i)}
            className={`flex items-center gap-1 rounded-lg px-2.5 py-1 text-xs font-medium transition ${
              selected === i
                ? tone === "red" ? "bg-red-100 text-red-700 ring-1 ring-red-300"
                  : tone === "emerald" ? "bg-emerald-100 text-emerald-700 ring-1 ring-emerald-300"
                  : "bg-indigo-100 text-indigo-700 ring-1 ring-indigo-300"
                : "bg-neutral-100 text-neutral-500 hover:bg-neutral-200"
            }`}
          >
            {result && (result.passed ? <CheckCircle2 size={12} /> : <XCircle size={12} />)}
            Case {i + 1}
          </button>
        );
      })}
    </div>
  );
}

function ProblemContent() {
  const params = useParams<{ slug: string }>();
  const slug = params.slug;
  const router = useRouter();
  const searchParams = useSearchParams();
  const rawMode = searchParams.get("mode");
  const mode = rawMode === "transfer" ? "transfer" : rawMode === "blind" ? "blind" : "standard";
  const contestId = searchParams.get("contestId");
  const contestTitle = searchParams.get("contestTitle");
  const queryClient = useQueryClient();

  const [language, setLanguage] = useState("python");

  const problemQ = useQuery({
    queryKey: ["problem", slug, language, mode],
    queryFn: async () => (await api.get<ProblemDetail>(`/problems/${slug}`, { params: { language, mode } })).data,
    // Only carry over the previous response while switching *language* for the
    // same problem (so the editor doesn't flash a full-page loading spinner) --
    // never across a genuine slug change, which would otherwise briefly render
    // the wrong problem's title/statement while the new one is still loading.
    placeholderData: (previousData, previousQuery) =>
      previousQuery?.queryKey[1] === slug ? previousData : undefined,
  });

  const conceptMapQ = useQuery({
    queryKey: ["concept-map", problemQ.data?.primary_skill_key],
    queryFn: async () => (await api.get<ConceptMapOut>(`/skills/${problemQ.data!.primary_skill_key}/concept-map`)).data,
    enabled: mode !== "blind" && !!problemQ.data?.primary_skill_key,
  });

  const [code, setCode] = useState<string>("");
  const [hintsRevealed, setHintsRevealed] = useState<{ level: number; text: string }[]>([]);
  const [declaredPattern, setDeclaredPattern] = useState("");
  const [reasoningText, setReasoningText] = useState("");
  const [reasoningResult, setReasoningResult] = useState<ReasoningSubmitResponse | null>(null);
  const [submitResult, setSubmitResult] = useState<SubmitResponse | null>(null);
  const [runResult, setRunResult] = useState<RunResponse | null>(null);
  const [question, setQuestion] = useState("");
  const [askAnswer, setAskAnswer] = useState<string | null>(null);
  const [leftTab, setLeftTab] = useState<"description" | "submissions">("description");
  const [consoleTab, setConsoleTab] = useState<"testcase" | "result">("testcase");
  const [selectedCase, setSelectedCase] = useState(0);
  const [expandedSubmission, setExpandedSubmission] = useState<string | null>(null);
  const startTimeRef = useRef<number>(0);

  const complexityMutation = useMutation({
    mutationFn: async () =>
      (await api.post<ComplexityCheckResponse>(`/problems/${slug}/verify-complexity`, { code, language })).data,
  });

  const traceMutation = useMutation({
    mutationFn: async (args: unknown[]) =>
      (await api.post<TraceResponse>(`/problems/${slug}/trace`, { code, language, args })).data,
  });

  useEffect(() => {
    // A trace belongs to one specific test case -- clear it whenever the
    // selected case changes so a stale trace from a different input isn't
    // shown under the newly-selected case. traceMutation is intentionally
    // left out of the deps below (see the similar note further down): it's a
    // new object every render, so including it would re-run this on every render.
    traceMutation.reset();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedCase]);

  useEffect(() => {
    // Resets local editor/attempt state and starts the solve timer whenever a
    // (possibly different) problem finishes loading -- an external-system sync,
    // not derived render state, so it belongs in an effect.
    if (problemQ.data) {
      startTimeRef.current = Date.now();
      // eslint-disable-next-line react-hooks/set-state-in-effect
      setCode(problemQ.data.starter_code);
      setHintsRevealed([]);
      setSubmitResult(null);
      setRunResult(null);
      setReasoningResult(null);
      setAskAnswer(null);
      setConsoleTab("testcase");
      setSelectedCase(0);
      complexityMutation.reset();
      traceMutation.reset();
    }
    // complexityMutation/traceMutation are new objects every render
    // (useMutation's return value isn't referentially stable) -- adding them
    // here would re-run this
    // effect on every render instead of only on a real problem/language change.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [problemQ.data]);

  const submissionsQ = useQuery({
    queryKey: ["problem-submissions", slug],
    queryFn: async () => (await api.get<SubmissionHistoryItem[]>(`/problems/${slug}/submissions`)).data,
    enabled: leftTab === "submissions",
  });

  const hintMutation = useMutation({
    mutationFn: async (level: number) =>
      (await api.get<{ level: number; text_markdown: string }>(`/problems/${slug}/hints/${level}`)).data,
    onSuccess: (data) => {
      setHintsRevealed((prev) => [...prev, { level: data.level, text: data.text_markdown }]);
    },
  });

  const reasoningMutation = useMutation({
    mutationFn: async () =>
      (
        await api.post<ReasoningSubmitResponse>(`/problems/${slug}/reasoning`, {
          declared_pattern: declaredPattern,
          reasoning_text: reasoningText,
        })
      ).data,
    onSuccess: setReasoningResult,
  });

  const runMutation = useMutation({
    mutationFn: async () => (await api.post<RunResponse>(`/problems/${slug}/run`, { code, language })).data,
    onSuccess: (data) => {
      setRunResult(data);
      setSubmitResult(null);
      setConsoleTab("result");
      setSelectedCase(0);
      traceMutation.reset();
    },
  });

  const submitMutation = useMutation({
    mutationFn: async () => {
      if (contestId) {
        return (
          await api.post<SubmitResponse>(`/contests/${contestId}/problems/${slug}/submit`, { code, language })
        ).data;
      }
      const timeToSolve = (Date.now() - startTimeRef.current) / 1000;
      return (
        await api.post<SubmitResponse>(`/problems/${slug}/submit`, {
          code,
          mode,
          language,
          time_to_solve_seconds: timeToSolve,
          hint_count_used: hintsRevealed.length,
        })
      ).data;
    },
    onSuccess: (data) => {
      setSubmitResult(data);
      setRunResult(null);
      setSelectedCase(0);
      complexityMutation.reset();
      traceMutation.reset();
      queryClient.invalidateQueries({ queryKey: ["my-skill-graph"] });
      queryClient.invalidateQueries({ queryKey: ["dashboard"] });
      queryClient.invalidateQueries({ queryKey: ["recommendations"] });
      queryClient.invalidateQueries({ queryKey: ["problem-submissions", slug] });
      if (contestId) {
        queryClient.invalidateQueries({ queryKey: ["contest-leaderboard", contestId] });
        queryClient.invalidateQueries({ queryKey: ["contest-detail", contestId] });
      }
    },
  });

  const explainMutation = useMutation({
    mutationFn: async () => (await api.get<ExplainResponse>(`/problems/${slug}/explain`)).data,
  });

  const askMutation = useMutation({
    mutationFn: async () => (await api.post<AskResponse>(`/problems/${slug}/ask`, { question })).data,
    onSuccess: (data) => setAskAnswer(data.answer),
  });

  if (problemQ.isLoading) return <Spinner label="Loading problem..." />;
  if (!problemQ.data) return <p className="text-red-600">Problem not found.</p>;
  const p = problemQ.data;
  const blindLocked = mode === "blind" && !reasoningResult;

  function resetCode() {
    if (problemQ.data) setCode(problemQ.data.starter_code);
  }

  return (
    <div className="grid gap-6 lg:grid-cols-2">
      {/* LEFT PANEL */}
      <div className="flex flex-col overflow-hidden rounded-xl border border-neutral-200 bg-white">
        <div className="flex border-b border-neutral-200 bg-neutral-50">
          {(["description", "submissions"] as const).map((tab) => (
            <button
              key={tab}
              onClick={() => setLeftTab(tab)}
              className={`px-4 py-2.5 text-sm font-semibold capitalize transition ${
                leftTab === tab
                  ? "border-b-2 border-indigo-500 bg-white text-indigo-700"
                  : "text-neutral-500 hover:text-neutral-800"
              }`}
            >
              {tab}
            </button>
          ))}
        </div>

        <div className="flex max-h-[calc(100vh-190px)] flex-col gap-4 overflow-y-auto p-4">
          {leftTab === "description" ? (
            <>
              {contestId && (
                <div className="flex items-center justify-between gap-2 rounded-xl border border-yellow-200 bg-yellow-50 px-3 py-2 text-sm text-yellow-900">
                  <span className="flex items-center gap-2">
                    <Trophy size={16} /> Contest mode{contestTitle ? `: ${contestTitle}` : ""} -- no hints or Ask-AI while it&apos;s live; a correct submission scores points on the leaderboard.
                  </span>
                  <Link href={`/contests/${contestId}`} className="shrink-0 font-semibold text-yellow-700 hover:underline">
                    Back to contest
                  </Link>
                </div>
              )}
              {mode === "transfer" && (
                <div className="flex items-center gap-2 rounded-xl border border-violet-200 bg-violet-50 px-3 py-2 text-sm text-violet-800">
                  <Shuffle size={16} /> New problem challenge -- this checks whether you really understand the idea, not just this one problem. Solving it counts separately from your regular progress.
                </div>
              )}
              {mode === "blind" && (
                <div className="flex items-center gap-2 rounded-xl border border-indigo-200 bg-indigo-50 px-3 py-2 text-sm text-indigo-800">
                  <EyeOff size={16} /> Blind practice -- no skill hint attached. Declare which pattern you think this is (below) to unlock the editor.
                </div>
              )}
              <div>
                <div className="flex flex-wrap items-center gap-2">
                  <h1 className="text-xl font-bold text-neutral-900 sm:text-2xl">{p.title}</h1>
                  <Badge tone={DIFFICULTY_TONE[p.difficulty]}>{p.difficulty}</Badge>
                </div>
                <p className="mt-1 text-sm text-neutral-500">
                  Expected complexity {p.expected_complexity} -- time limit {p.time_limit_ms}ms
                </p>
              </div>
              {conceptMapQ.data && (
                <ConceptMapStrip
                  before={conceptMapQ.data.prerequisites.map((pr) => ({ key: pr.key, label: pr.name }))}
                  currentLabel={conceptMapQ.data.current.name}
                  after={conceptMapQ.data.unlocks.map((u) => ({ key: u.key, label: u.name }))}
                  onNavigate={(key) => router.push(`/skills?skill=${key}`)}
                />
              )}
              <Markdown>{p.statement_markdown}</Markdown>
              <div>
                <h3 className="font-semibold text-neutral-900">Constraints</h3>
                <p className="text-sm text-neutral-600">{p.constraints_markdown}</p>
              </div>
              <div>
                <h3 className="font-semibold text-neutral-900">Examples</h3>
                {p.examples.map((ex, i) => (
                  <div key={i} className="mt-1 rounded-lg bg-neutral-50 p-2 font-mono text-xs">
                    <div>input: {ex.input}</div>
                    <div>output: {ex.output}</div>
                    <div className="text-neutral-500">{ex.explanation}</div>
                  </div>
                ))}
              </div>

              {!contestId && (
                <Card className={blindLocked ? "border-2 border-indigo-300" : ""}>
                  <h3 className="mb-2 flex items-center gap-2 font-semibold text-neutral-900">
                    <Brain size={16} className="text-indigo-500" />
                    {mode === "blind" ? "Declare the pattern to unlock the editor" : "Pattern recognition (optional, before you code)"}
                  </h3>
                  <input
                    value={declaredPattern}
                    onChange={(e) => setDeclaredPattern(e.target.value)}
                    placeholder="e.g. HASHING, TWO_POINTER, SLIDING_WINDOW..."
                    className="w-full rounded-lg border border-neutral-300 px-2 py-1.5 text-sm outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100"
                  />
                  <textarea
                    value={reasoningText}
                    onChange={(e) => setReasoningText(e.target.value)}
                    placeholder="Why do you think this pattern fits? What clues in the problem point there?"
                    className="mt-2 w-full rounded-lg border border-neutral-300 px-2 py-1.5 text-sm outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100"
                    rows={2}
                  />
                  <Button variant="secondary" onClick={() => reasoningMutation.mutate()} disabled={!declaredPattern || reasoningMutation.isPending} className="mt-2">
                    Check my reasoning
                  </Button>
                  {reasoningResult && (
                    <>
                      <p className={`mt-2 text-sm ${reasoningResult.is_correct_pattern ? "text-emerald-700" : "text-amber-700"}`}>
                        {reasoningResult.feedback} (reasoning quality: {Math.round(reasoningResult.reasoning_quality_score * 100)}%)
                      </p>
                      {!reasoningResult.is_correct_pattern && (reasoningResult.missing_evidence.length > 0 || reasoningResult.declared_pattern_evidence.length > 0) && (
                        <div className="mt-2 rounded-lg bg-amber-50 p-2.5 text-xs ring-1 ring-amber-200">
                          <p className="font-bold uppercase tracking-wide text-amber-700">Reasoning gap</p>
                          {reasoningResult.declared_pattern_evidence.length > 0 && (
                            <p className="mt-1 text-amber-900">
                              Your reasoning used real {reasoningResult.declared_pattern_evidence.map((w) => `"${w}"`).join(", ")} vocabulary --
                              that&apos;s what pulled it toward the wrong pattern.
                            </p>
                          )}
                          {reasoningResult.missing_evidence.length > 0 && (
                            <p className="mt-1 text-amber-900">
                              The real signal for {reasoningResult.correct_pattern} that&apos;s missing: {reasoningResult.missing_evidence.map((w) => `"${w}"`).join(", ")}.
                            </p>
                          )}
                        </div>
                      )}
                      {reasoningResult.plan_quality_coach && (
                        <div className="mt-2 rounded-lg bg-violet-50 p-2.5 ring-1 ring-violet-200">
                          <p className="text-xs font-bold uppercase tracking-wide text-violet-700">
                            AI plan-quality coach: {reasoningResult.plan_quality_coach.plan_quality_tier}
                          </p>
                          <p className="mt-0.5 text-xs text-violet-900">{reasoningResult.plan_quality_coach.coaching_tip}</p>
                        </div>
                      )}
                    </>
                  )}
                </Card>
              )}

              {contestId ? (
                <Card className="border-dashed text-center text-sm text-neutral-400">
                  <Trophy size={18} className="mx-auto mb-1" />
                  Hints and Ask-AI are off during a contest -- solve it the way you&apos;d solve it under real conditions.
                </Card>
              ) : blindLocked ? (
                <Card className="border-dashed text-center text-sm text-neutral-400">
                  <Lock size={18} className="mx-auto mb-1" />
                  Hints and Ask-AI unlock once you&apos;ve declared a pattern above -- using them first would defeat the point of blind practice.
                </Card>
              ) : (
                <>
                  <Card>
                    <h3 className="mb-2 flex items-center gap-2 font-semibold text-neutral-900">
                      <Lightbulb size={16} className="text-amber-500" /> Hints ({hintsRevealed.length} used)
                    </h3>
                    <div className="flex flex-col gap-2">
                      {hintsRevealed.map((h) => (
                        <p key={h.level} className="text-sm text-neutral-700">
                          <span className="font-semibold">Hint {h.level}:</span> {h.text}
                        </p>
                      ))}
                    </div>
                    <Button variant="ghost" onClick={() => hintMutation.mutate(hintsRevealed.length + 1)} disabled={hintMutation.isPending} className="mt-2">
                      Reveal next hint
                    </Button>
                  </Card>

                  <Card>
                    <div className="mb-2 flex items-center gap-2">
                      <h3 className="flex items-center gap-2 font-semibold text-neutral-900">
                        <Sparkles size={16} className="text-violet-500" /> Ask about this problem
                      </h3>
                      <AiLabel />
                    </div>
                    <div className="flex gap-2">
                      <input
                        value={question}
                        onChange={(e) => setQuestion(e.target.value)}
                        placeholder="e.g. why does this need O(n) and not O(n^2)?"
                        className="flex-1 rounded-lg border border-neutral-300 px-2 py-1.5 text-sm outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100"
                      />
                      <Button variant="secondary" onClick={() => askMutation.mutate()} disabled={!question.trim() || askMutation.isPending}>
                        Ask
                      </Button>
                    </div>
                    {askMutation.isPending && <div className="mt-2"><Spinner label="Thinking (local model, a few seconds)..." /></div>}
                    {askMutation.isError && <p className="mt-2 text-sm text-red-600">Local model isn&apos;t available -- see README for the one-time download step.</p>}
                    {askAnswer && <p className="mt-2 text-sm text-neutral-700">{askAnswer}</p>}
                  </Card>
                </>
              )}
            </>
          ) : (
            <>
              {submissionsQ.isLoading && <Spinner label="Loading submissions..." />}
              {submissionsQ.data && submissionsQ.data.length === 0 && (
                <p className="text-sm text-neutral-500">No submissions yet -- solve it and hit Submit.</p>
              )}
              {submissionsQ.data?.map((s) => (
                <div key={s.id} className="rounded-lg border border-neutral-200">
                  <button
                    onClick={() => setExpandedSubmission(expandedSubmission === s.id ? null : s.id)}
                    className="flex w-full items-center justify-between gap-2 px-3 py-2 text-left text-sm"
                  >
                    <span className={`flex items-center gap-1.5 font-semibold ${s.status === "PASSED" ? "text-emerald-700" : "text-red-600"}`}>
                      {s.status === "PASSED" ? <CheckCircle2 size={14} /> : <XCircle size={14} />}
                      {s.status === "PASSED" ? "Accepted" : s.status.replace("_", " ")}
                    </span>
                    <span className="text-xs text-neutral-500">{LANGUAGE_LABEL[s.language] ?? s.language}</span>
                    <span className="text-xs text-neutral-500">{s.passed_count}/{s.total_count} tests</span>
                    <span className="text-xs text-neutral-400">{relativeTime(s.created_at)}</span>
                  </button>
                  {expandedSubmission === s.id && (
                    <pre className="overflow-x-auto border-t border-neutral-200 bg-neutral-50 p-3 text-xs">{s.code}</pre>
                  )}
                </div>
              ))}
            </>
          )}
        </div>
      </div>

      {/* RIGHT PANEL */}
      <div className="flex flex-col overflow-hidden rounded-xl border border-neutral-200 bg-white">
        {blindLocked ? (
          <div className="flex h-[320px] flex-col items-center justify-center gap-2 text-center text-neutral-400">
            <Lock size={28} />
            <p className="text-sm">Declare a pattern on the left to unlock the editor.</p>
          </div>
        ) : (
          <>
            <div className="flex items-center justify-between border-b border-neutral-200 bg-neutral-50 px-3 py-1.5">
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className="rounded-lg border border-neutral-300 bg-white px-2 py-1 text-xs font-medium text-neutral-700 outline-none focus:border-emerald-500"
              >
                {(p.supported_languages ?? ["python"]).map((lang) => (
                  <option key={lang} value={lang}>{LANGUAGE_LABEL[lang] ?? lang}</option>
                ))}
              </select>
              <div className="flex items-center gap-2">
                <button
                  onClick={resetCode}
                  title="Reset to starter code"
                  className="rounded-lg p-1.5 text-neutral-500 hover:bg-neutral-200 hover:text-neutral-800"
                >
                  <RotateCcw size={14} />
                </button>
                <Button variant="ghost" onClick={() => runMutation.mutate()} disabled={runMutation.isPending} className="flex items-center gap-1.5 !px-3 !py-1.5 !text-xs">
                  <Play size={13} /> {runMutation.isPending ? "Running..." : "Run"}
                </Button>
                <Button onClick={() => submitMutation.mutate()} disabled={submitMutation.isPending} className="!px-3 !py-1.5 !text-xs">
                  {submitMutation.isPending ? "Submitting..." : "Submit"}
                </Button>
              </div>
            </div>
            <MonacoEditor
              height="320px"
              language={MONACO_LANGUAGE[language] ?? "plaintext"}
              value={code}
              onChange={(v) => setCode(v ?? "")}
              options={{ minimap: { enabled: false }, fontSize: 13 }}
            />

            <div className="flex flex-col border-t border-neutral-200">
              {submitResult ? (
                <div className={`flex flex-col gap-3 p-4 ${submitResult.status === "PASSED" ? "bg-emerald-50/50" : "bg-red-50/40"}`}>
                  <p className={`flex items-center gap-2 text-lg font-bold ${submitResult.status === "PASSED" ? "text-emerald-700" : "text-red-600"}`}>
                    {submitResult.status === "PASSED" ? <CheckCircle2 size={22} /> : <XCircle size={22} />}
                    {submitResult.status === "PASSED"
                      ? (submitResult.repeat_solve_note ? "Accepted (again)" : "Accepted")
                      : submitResult.status === "FAILED" ? "Wrong Answer"
                      : submitResult.status.replace("_", " ")}
                  </p>
                  <div className="flex flex-wrap gap-3 text-xs">
                    <span className="flex items-center gap-1 rounded-lg bg-white px-2.5 py-1.5 ring-1 ring-neutral-200">
                      <Gauge size={13} className="text-neutral-400" />
                      {submitResult.passed_count}/{submitResult.total_count} testcases passed
                    </span>
                    <span className="flex items-center gap-1 rounded-lg bg-white px-2.5 py-1.5 ring-1 ring-neutral-200">
                      <Clock size={13} className="text-neutral-400" />
                      Runtime {submitResult.runtime_ms.toFixed(1)}ms
                      {submitResult.runtime_percentile !== null && (
                        <span className="text-neutral-500"> -- faster than {submitResult.runtime_percentile}% of {LANGUAGE_LABEL[submitResult.language] ?? submitResult.language} submissions</span>
                      )}
                    </span>
                  </div>

                  {submitResult.optimization_nudge && (
                    <div className="flex gap-2.5 rounded-xl bg-gradient-to-br from-orange-50 to-amber-50 p-3 ring-1 ring-orange-200">
                      <Zap size={18} className="mt-0.5 shrink-0 text-orange-500" />
                      <div>
                        <p className="text-xs font-bold uppercase tracking-wide text-orange-700">Room to optimize -- shift out of brute force</p>
                        <p className="mt-0.5 text-sm text-orange-900">{submitResult.optimization_nudge}</p>
                      </div>
                    </div>
                  )}


                  {submitResult.status === "PASSED" && (language === "python" || language === "javascript") && (
                    <div className="rounded-xl bg-white p-3 ring-1 ring-neutral-200">
                      {!complexityMutation.data && !complexityMutation.isPending && (
                        <Button variant="ghost" onClick={() => complexityMutation.mutate()} className="flex items-center gap-1.5 !px-3 !py-1.5 !text-xs">
                          <ActivitySquare size={13} /> Test how it scales
                        </Button>
                      )}
                      {complexityMutation.isPending && <Spinner label="Re-running your code at larger sizes (a few seconds)..." />}
                      {complexityMutation.data && (
                        <div className="flex flex-col gap-2">
                          <p className="flex items-center gap-1.5 text-xs font-bold uppercase tracking-wide text-neutral-500">
                            <ActivitySquare size={13} /> How your code scales
                          </p>
                          {!complexityMutation.data.supported ? (
                            <p className="text-sm text-neutral-500">{complexityMutation.data.reason}</p>
                          ) : (
                            <>
                              <div className="flex flex-wrap gap-2 font-mono text-xs">
                                {complexityMutation.data.samples.map((s) => (
                                  <span key={s.size} className={`rounded-lg px-2 py-1 ring-1 ${s.status === "EXECUTED" ? "bg-neutral-50 ring-neutral-200" : "bg-red-50 text-red-700 ring-red-200"}`}>
                                    n={s.size}: {s.status === "EXECUTED" ? `${s.runtime_ms?.toFixed(1)}ms` : s.status}
                                  </span>
                                ))}
                              </div>
                              {complexityMutation.data.likely_matches_expected === false && (
                                <p className="flex items-center gap-1.5 text-sm font-semibold text-amber-700">
                                  <Zap size={14} /> Measured growth looks worse than this problem&apos;s expected {complexityMutation.data.expected_complexity}
                                </p>
                              )}
                              {complexityMutation.data.likely_matches_expected === true && (
                                <p className="flex items-center gap-1.5 text-sm font-semibold text-emerald-700">
                                  <CheckCircle2 size={14} /> Measured growth is consistent with this problem&apos;s expected {complexityMutation.data.expected_complexity}
                                </p>
                              )}
                              <p className="text-xs text-neutral-500">{complexityMutation.data.explanation}</p>
                            </>
                          )}
                          <button onClick={() => complexityMutation.reset()} className="self-start text-xs font-medium text-indigo-600 hover:underline">
                            Dismiss
                          </button>
                        </div>
                      )}
                    </div>
                  )}

                  <CaseTabs count={submitResult.test_results.length} selected={selectedCase} onSelect={setSelectedCase} results={submitResult.test_results} />
                  {submitResult.test_results[selectedCase] && (
                    <div className="rounded-lg bg-white p-3 font-mono text-xs ring-1 ring-neutral-200">
                      {submitResult.test_results[selectedCase].is_hidden ? (
                        <p className="text-neutral-500">Hidden test case -- input/output are not shown, but the pass/fail result above is real.</p>
                      ) : (
                        <>
                          <div>Input: {JSON.stringify(submitResult.test_results[selectedCase].input)}</div>
                          <div>Expected: {JSON.stringify(submitResult.test_results[selectedCase].expected)}</div>
                          <div>Output: {JSON.stringify(submitResult.test_results[selectedCase].actual)}</div>
                          {submitResult.test_results[selectedCase].error && (
                            <div className="mt-1 text-red-600">{submitResult.test_results[selectedCase].error}</div>
                          )}
                        </>
                      )}
                    </div>
                  )}

                  {submitResult.test_results[selectedCase] && !submitResult.test_results[selectedCase].passed
                    && !submitResult.test_results[selectedCase].is_hidden
                    && (language === "python" || language === "javascript" || language === "java") && (
                    <div className="rounded-xl bg-white p-3 ring-1 ring-neutral-200">
                      {!traceMutation.data && !traceMutation.isPending && (
                        <Button
                          variant="ghost"
                          onClick={() => traceMutation.mutate(submitResult.test_results[selectedCase].input as unknown[])}
                          className="flex items-center gap-1.5 !px-3 !py-1.5 !text-xs"
                        >
                          <ActivitySquare size={13} /> Watch your code run on this input
                        </Button>
                      )}
                      {traceMutation.isPending && <Spinner label="Stepping through your code..." />}
                      {traceMutation.data && (
                        traceMutation.data.supported ? (
                          <OwnCodeTrace
                            sourceLines={traceMutation.data.source_lines} steps={traceMutation.data.steps}
                            result={traceMutation.data.result} status={traceMutation.data.status}
                            errorMessage={traceMutation.data.error_message} truncated={traceMutation.data.truncated}
                          />
                        ) : (
                          <p className="text-sm text-neutral-500">{traceMutation.data.reason}</p>
                        )
                      )}
                    </div>
                  )}

                  {submitResult.diagnosis && (
                    <div className="rounded-lg bg-neutral-50 p-3 text-sm">
                      <p className="font-semibold text-neutral-900">
                        {DIAGNOSIS_LABEL[submitResult.diagnosis.primary_issue] ?? submitResult.diagnosis.primary_issue}{" "}
                        ({Math.round(submitResult.diagnosis.confidence * 100)}% sure)
                      </p>
                      <ul className="mt-1 list-inside list-disc text-neutral-600">
                        {submitResult.diagnosis.evidence.map((e, i) => (
                          <li key={i}>{e}</li>
                        ))}
                      </ul>
                      <p className="mt-1 text-neutral-500">Recommended: {submitResult.diagnosis.recommendation}</p>

                      <div className="mt-3 border-t border-neutral-200 pt-3">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-2">
                            <span className="text-xs font-semibold uppercase tracking-wide text-neutral-500">Plain-language explanation</span>
                            <AiLabel />
                          </div>
                          <Button variant="ghost" onClick={() => explainMutation.mutate()} disabled={explainMutation.isPending}>
                            {explainMutation.isPending ? "..." : "Explain"}
                          </Button>
                        </div>
                        {explainMutation.isError && (
                          <p className="mt-2 text-xs text-red-600">Local model isn&apos;t available -- see README for the one-time download step.</p>
                        )}
                        {explainMutation.data && <p className="mt-2 text-neutral-700">{explainMutation.data.explanation}</p>}
                      </div>
                    </div>
                  )}
                  {submitResult.updated_mastery !== null && (
                    <p className="text-sm text-neutral-600">
                      Updated progress on this concept: {Math.round(submitResult.updated_mastery * 100)}%
                    </p>
                  )}
                  {submitResult.repeat_solve_note && (
                    <p className="rounded-lg bg-amber-50 p-2 text-xs text-amber-800">{submitResult.repeat_solve_note}</p>
                  )}
                  <button
                    onClick={() => {
                      setSubmitResult(null);
                      setConsoleTab("testcase");
                      setSelectedCase(0);
                    }}
                    className="self-start text-xs font-medium text-indigo-600 hover:underline"
                  >
                    Back to testcases
                  </button>
                </div>
              ) : (
                <>
                  <div className="flex border-b border-neutral-200 bg-neutral-50">
                    {(["testcase", "result"] as const).map((tab) => (
                      <button
                        key={tab}
                        onClick={() => setConsoleTab(tab)}
                        disabled={tab === "result" && !runResult}
                        className={`px-4 py-2 text-xs font-semibold capitalize transition disabled:cursor-not-allowed disabled:opacity-40 ${
                          consoleTab === tab ? "border-b-2 border-indigo-500 bg-white text-indigo-700" : "text-neutral-500 hover:text-neutral-800"
                        }`}
                      >
                        {tab === "testcase" ? "Testcase" : "Test Result"}
                      </button>
                    ))}
                  </div>
                  <div className="flex flex-col gap-3 p-3">
                    {consoleTab === "testcase" && (
                      <>
                        <CaseTabs count={p.visible_test_cases.length} selected={selectedCase} onSelect={setSelectedCase} />
                        {p.visible_test_cases[selectedCase] && (
                          <div className="rounded-lg bg-neutral-50 p-3 font-mono text-xs">
                            {p.visible_test_cases[selectedCase].args.map((arg, i) => (
                              <div key={i} className="mb-1">
                                <span className="text-neutral-500">{p.param_names[i] ?? `arg${i}`} =</span>{" "}
                                <span className="text-neutral-900">{JSON.stringify(arg)}</span>
                              </div>
                            ))}
                            <div className="mt-1 text-neutral-500">expected = {JSON.stringify(p.visible_test_cases[selectedCase].expected_output)}</div>
                          </div>
                        )}
                        <p className="text-xs text-neutral-400">Hit Run to check your code against these example testcases -- it won&apos;t count as an attempt.</p>
                      </>
                    )}
                    {consoleTab === "result" && runResult && (
                      <>
                        <p className={`flex items-center gap-1.5 text-sm font-semibold ${runResult.status === "PASSED" ? "text-emerald-700" : "text-red-600"}`}>
                          {runResult.status === "PASSED" ? <CheckCircle2 size={16} /> : <XCircle size={16} />}
                          {runResult.status === "PASSED" ? "Accepted" : "Wrong Answer"} -- {runResult.passed_count}/{runResult.total_count} passed
                          <span className="font-normal text-neutral-400">({runResult.runtime_ms.toFixed(1)}ms)</span>
                        </p>
                        <CaseTabs count={runResult.test_results.length} selected={selectedCase} onSelect={setSelectedCase} results={runResult.test_results} />
                        {runResult.test_results[selectedCase] && (
                          <div className="rounded-lg bg-neutral-50 p-3 font-mono text-xs">
                            <div>Input: {JSON.stringify(runResult.test_results[selectedCase].input)}</div>
                            <div>Expected: {JSON.stringify(runResult.test_results[selectedCase].expected)}</div>
                            <div>Output: {JSON.stringify(runResult.test_results[selectedCase].actual)}</div>
                            {runResult.test_results[selectedCase].error && (
                              <div className="mt-1 text-red-600">{runResult.test_results[selectedCase].error}</div>
                            )}
                          </div>
                        )}
                        {runResult.test_results[selectedCase] && !runResult.test_results[selectedCase].passed
                          && (language === "python" || language === "javascript" || language === "java") && (
                          <div className="rounded-xl bg-neutral-50 p-3 ring-1 ring-neutral-200">
                            {!traceMutation.data && !traceMutation.isPending && (
                              <Button
                                variant="ghost"
                                onClick={() => traceMutation.mutate(runResult.test_results[selectedCase].input as unknown[])}
                                className="flex items-center gap-1.5 !px-3 !py-1.5 !text-xs"
                              >
                                <ActivitySquare size={13} /> Watch your code run on this input
                              </Button>
                            )}
                            {traceMutation.isPending && <Spinner label="Stepping through your code..." />}
                            {traceMutation.data && (
                              traceMutation.data.supported ? (
                                <OwnCodeTrace
                                  sourceLines={traceMutation.data.source_lines} steps={traceMutation.data.steps}
                                  result={traceMutation.data.result} status={traceMutation.data.status}
                                  errorMessage={traceMutation.data.error_message} truncated={traceMutation.data.truncated}
                                />
                              ) : (
                                <p className="text-sm text-neutral-500">{traceMutation.data.reason}</p>
                              )
                            )}
                          </div>
                        )}
                      </>
                    )}
                  </div>
                </>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default function ProblemPage() {
  return (
    <ProtectedRoute>
      <ProblemContent />
    </ProtectedRoute>
  );
}
