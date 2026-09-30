"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import Link from "next/link";
import { useState } from "react";
import { CheckCircle2, Layers, XCircle } from "lucide-react";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import { Badge, Button, Card, PageHero, Spinner } from "@/components/ui";
import { api } from "@/lib/api";
import { MockLoopReportOut, MockLoopStartResponse, MockLoopStateOut } from "@/lib/types";

const STAGE_LABEL: Record<string, string> = {
  dsa: "Round 1: DSA", system_design: "Round 2: System Design", behavioral: "Round 3: Behavioral", completed: "Completed",
};
const STAGES = ["dsa", "system_design", "behavioral", "completed"];

function StageProgress({ stage }: { stage: string }) {
  const idx = STAGES.indexOf(stage);
  return (
    <div className="mb-4 flex items-center gap-1.5">
      {STAGES.map((s, i) => (
        <div key={s} className={`h-1.5 flex-1 rounded-full ${i <= idx ? "bg-rose-500" : "bg-neutral-200"}`} />
      ))}
    </div>
  );
}

function FullLoopContent() {
  const qc = useQueryClient();
  const [loopId, setLoopId] = useState<string | null>(null);
  const [behavioralAnswer, setBehavioralAnswer] = useState("");

  const startMutation = useMutation({
    mutationFn: async () => (await api.post<MockLoopStartResponse>("/interviews/full-loop/start")).data,
    onSuccess: (data) => setLoopId(data.loop_id),
  });

  const stateQ = useQuery({
    queryKey: ["mock-loop", loopId],
    queryFn: async () => (await api.get<MockLoopStateOut>(`/interviews/full-loop/${loopId}`)).data,
    enabled: !!loopId,
  });

  const syncDsaMutation = useMutation({
    mutationFn: async () => (await api.post<MockLoopStateOut>(`/interviews/full-loop/${loopId}/sync-dsa`)).data,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["mock-loop", loopId] }),
  });
  const syncSdMutation = useMutation({
    mutationFn: async () => (await api.post<MockLoopStateOut>(`/interviews/full-loop/${loopId}/sync-system-design`)).data,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["mock-loop", loopId] }),
  });
  const behavioralMutation = useMutation({
    mutationFn: async () => (await api.post<MockLoopStateOut>(`/interviews/full-loop/${loopId}/behavioral-answer`, { answer: behavioralAnswer })).data,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["mock-loop", loopId] }),
  });

  const reportQ = useQuery({
    queryKey: ["mock-loop-report", loopId],
    queryFn: async () => (await api.get<MockLoopReportOut>(`/interviews/full-loop/${loopId}/report`)).data,
    enabled: !!loopId && stateQ.data?.stage === "completed",
  });

  if (!loopId) {
    return (
      <Card className="mx-auto max-w-lg text-center">
        <p className="mb-4 text-sm text-neutral-600">
          A single timed mock &quot;onsite&quot;: one DSA problem, one System Design case, one behavioral question --
          each round is graded for real by the same engines this app already uses, not just logged.
        </p>
        <Button onClick={() => startMutation.mutate()} disabled={startMutation.isPending}>
          {startMutation.isPending ? "Setting up..." : "Start the full loop"}
        </Button>
      </Card>
    );
  }

  if (stateQ.isLoading || !stateQ.data) return <Spinner label="Loading loop..." />;
  const state = stateQ.data;

  return (
    <div className="mx-auto max-w-2xl">
      <StageProgress stage={state.stage} />

      {state.stage === "dsa" && (
        <Card>
          <h3 className="mb-2 font-semibold text-neutral-900">{STAGE_LABEL.dsa}</h3>
          <p className="mb-3 text-sm text-neutral-600">
            Solve the linked problem, then come back here and continue -- your real submission result carries over.
          </p>
          <div className="flex flex-wrap items-center gap-2">
            <Link href={`/problems/${state.dsa_problem_slug}`} className="rounded-lg bg-neutral-900 px-3 py-1.5 text-sm font-medium text-white hover:bg-neutral-800">
              Open problem: {state.dsa_problem_slug}
            </Link>
            <Button variant="secondary" onClick={() => syncDsaMutation.mutate()} disabled={syncDsaMutation.isPending}>
              I&apos;ve submitted -- continue
            </Button>
          </div>
          {syncDsaMutation.isError && <p className="mt-2 text-xs text-red-600">Submit a solution to the linked problem first.</p>}
        </Card>
      )}

      {state.stage === "system_design" && (
        <Card>
          <h3 className="mb-2 font-semibold text-neutral-900">{STAGE_LABEL.system_design}</h3>
          <p className="mb-1 text-xs text-emerald-700">Round 1 (DSA): {state.dsa_passed ? "Passed" : "Not passed"}</p>
          <p className="mb-3 text-sm text-neutral-600">
            Submit a design for the linked case, then continue -- your real critique score carries over.
          </p>
          <div className="flex flex-wrap items-center gap-2">
            <Link href={`/system-design/${state.sd_case_slug}`} className="rounded-lg bg-neutral-900 px-3 py-1.5 text-sm font-medium text-white hover:bg-neutral-800">
              Open case: {state.sd_case_slug}
            </Link>
            <Button variant="secondary" onClick={() => syncSdMutation.mutate()} disabled={syncSdMutation.isPending}>
              I&apos;ve submitted -- continue
            </Button>
          </div>
          {syncSdMutation.isError && <p className="mt-2 text-xs text-red-600">Submit a design for the linked case first.</p>}
        </Card>
      )}

      {state.stage === "behavioral" && (
        <Card>
          <h3 className="mb-2 font-semibold text-neutral-900">{STAGE_LABEL.behavioral}</h3>
          <p className="mb-1 text-xs text-emerald-700">
            Round 1 (DSA): {state.dsa_passed ? "Passed" : "Not passed"} -- Round 2 (System Design): {Math.round((state.sd_score ?? 0) * 100)}%
          </p>
          <p className="mb-3 rounded-lg bg-neutral-50 p-3 text-sm font-medium text-neutral-800">{state.behavioral_question}</p>
          <textarea
            value={behavioralAnswer}
            onChange={(e) => setBehavioralAnswer(e.target.value)}
            rows={5}
            placeholder="Answer as you would in a real interview -- situation, task, action, result."
            className="w-full rounded-lg border border-neutral-300 px-2.5 py-2 text-sm outline-none focus:border-rose-500 focus:ring-2 focus:ring-rose-100"
          />
          <Button className="mt-2" onClick={() => behavioralMutation.mutate()} disabled={!behavioralAnswer.trim() || behavioralMutation.isPending}>
            Submit answer
          </Button>
        </Card>
      )}

      {state.stage === "completed" && reportQ.data && (
        <Card>
          <h3 className="mb-4 font-semibold text-neutral-900">Full Loop Report</h3>
          <div className="flex flex-col gap-3">
            <div className="flex items-center gap-2 rounded-lg bg-neutral-50 p-3">
              {reportQ.data.dsa_passed ? <CheckCircle2 size={18} className="text-emerald-600" /> : <XCircle size={18} className="text-red-500" />}
              <div>
                <p className="text-sm font-semibold">DSA: {reportQ.data.dsa_problem_title}</p>
                <p className="text-xs text-neutral-500">
                  {reportQ.data.dsa_passed ? "Passed" : "Not passed"} -- {reportQ.data.dsa_passed_count}/{reportQ.data.dsa_total_count} test cases
                </p>
              </div>
            </div>
            <div className="rounded-lg bg-neutral-50 p-3">
              <p className="text-sm font-semibold">System Design: {reportQ.data.sd_case_title}</p>
              <p className="text-xs text-neutral-500">Critique score: {Math.round((reportQ.data.sd_score ?? 0) * 100)}%</p>
              {reportQ.data.sd_missing_components.length > 0 && (
                <p className="mt-1 text-xs text-red-600">Missing: {reportQ.data.sd_missing_components.join(", ")}</p>
              )}
              {reportQ.data.sd_unjustified_components.length > 0 && (
                <p className="mt-1 text-xs text-amber-700">Unjustified: {reportQ.data.sd_unjustified_components.join(", ")}</p>
              )}
            </div>
            <div className="rounded-lg bg-neutral-50 p-3">
              <p className="text-sm font-semibold">Behavioral</p>
              <p className="text-xs text-neutral-500">{reportQ.data.behavioral_question}</p>
              <Badge tone={reportQ.data.behavioral_tier === "STRONG_STAR_STRUCTURE" ? "emerald" : "amber"}>
                {reportQ.data.behavioral_tier?.replaceAll("_", " ")}
              </Badge>
              <p className="mt-1 text-xs text-neutral-600">{reportQ.data.behavioral_coaching_tip}</p>
            </div>
            <p className="rounded-lg bg-rose-50 p-3 text-sm text-rose-900 ring-1 ring-rose-200">{reportQ.data.overall_summary}</p>
          </div>
        </Card>
      )}
    </div>
  );
}

export default function FullLoopPage() {
  return (
    <ProtectedRoute>
      <PageHero
        icon={Layers} title="Full Mock Interview Loop" gradient="from-rose-500 to-pink-500"
        subtitle="One DSA problem, one System Design case, one behavioral question -- chained into a single graded session, each round verified for real."
      />
      <FullLoopContent />
    </ProtectedRoute>
  );
}
