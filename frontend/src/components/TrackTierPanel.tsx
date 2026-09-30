"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import Link from "next/link";
import { Award, CheckCircle2, XCircle } from "lucide-react";
import { useEffect, useState } from "react";
import { Spinner } from "@/components/ui";
import { api } from "@/lib/api";
import {
  QuizAnswerResponse, TrackAssessmentCheckOut, TrackAssessmentStartOut, TrackTierStatusOut,
} from "@/lib/types";

const TIER_STYLE: Record<string, string> = {
  novice: "bg-neutral-100 text-neutral-600",
  practitioner: "bg-sky-100 text-sky-700",
  expert: "bg-amber-100 text-amber-700",
};
const TIER_LABEL: Record<string, string> = { novice: "Novice", practitioner: "Practitioner", expert: "Expert" };

export function TrackTierBadge({ tier }: { tier: string }) {
  return (
    <span className={`inline-flex items-center gap-1 rounded-full px-2.5 py-1 text-xs font-bold uppercase tracking-wide ${TIER_STYLE[tier] ?? TIER_STYLE.novice}`}>
      <Award size={12} /> {TIER_LABEL[tier] ?? tier}
    </span>
  );
}

function itemHref(kind: string, slug: string): string | null {
  if (kind === "case") return `/system-design/${slug}`;
  if (kind === "problem") return `/problems/${slug}`;
  return null;
}

function QuizItem({ track, assessmentId, questionId, question, options, onAnswered }: {
  track: string; assessmentId: string; questionId: string; question: string; options: string[];
  onAnswered: () => void;
}) {
  const [result, setResult] = useState<QuizAnswerResponse | null>(null);
  const answerMutation = useMutation({
    mutationFn: async (selected_index: number) =>
      (await api.post<QuizAnswerResponse>(`/tracks/${track}/tier-assessment/${assessmentId}/quiz-answer`, {
        question_id: questionId, selected_index,
      })).data,
    onSuccess: (r) => {
      setResult(r);
      onAnswered();
    },
  });

  return (
    <div className="rounded-lg bg-white p-2.5 text-sm">
      <p className="font-medium text-neutral-800">{question}</p>
      <div className="mt-1.5 flex flex-col gap-1">
        {options.map((opt, i) => (
          <button
            key={i}
            onClick={() => !result && answerMutation.mutate(i)}
            disabled={!!result || answerMutation.isPending}
            className={`rounded-md border px-2 py-1 text-left text-xs transition-colors ${
              result && i === result.correct_index ? "border-emerald-400 bg-emerald-50 text-emerald-800" : "border-neutral-200 hover:bg-neutral-50"
            }`}
          >
            {opt}
          </button>
        ))}
      </div>
      {result && (
        <p className={`mt-1.5 text-xs ${result.correct ? "text-emerald-600" : "text-red-600"}`}>
          {result.correct ? "Correct." : "Incorrect."} {result.explanation}
        </p>
      )}
    </div>
  );
}

export function TrackTierPanel({ track, label }: { track: string; label: string }) {
  const queryClient = useQueryClient();
  const [startedAssessmentId, setStartedAssessmentId] = useState<string | null>(null);

  const statusQ = useQuery({
    queryKey: ["track-tier-status", track],
    queryFn: async () => (await api.get<TrackTierStatusOut>(`/tracks/${track}/tier-status`)).data,
  });

  // Deliberately never auto-resumes statusQ.data?.active_assessment_id -- an
  // in-progress assessment only becomes visible again via an explicit
  // "start" click in this session, so navigating away and back (a browser
  // back button, revisiting the page later) always shows a clean slate
  // instead of resurfacing the same items indefinitely.
  const assessmentId = startedAssessmentId;

  const checkQ = useQuery({
    queryKey: ["track-tier-check", track, assessmentId],
    queryFn: async () => (await api.post<TrackAssessmentCheckOut>(`/tracks/${track}/tier-assessment/${assessmentId}/check`)).data,
    enabled: !!assessmentId,
  });

  const startMutation = useMutation({
    mutationFn: async () => (await api.post<TrackAssessmentStartOut>(`/tracks/${track}/tier-assessment/start`)).data,
    onSuccess: (result) => {
      if (result.ok && result.assessment_id) {
        setStartedAssessmentId(result.assessment_id);
        queryClient.invalidateQueries({ queryKey: ["track-tier-status", track] });
      }
    },
  });

  useEffect(() => {
    if (checkQ.data?.status === "passed") {
      queryClient.invalidateQueries({ queryKey: ["track-tier-status", track] });
    }
  }, [checkQ.data?.status, queryClient, track]);

  if (statusQ.isLoading) return <Spinner label={`Loading ${label} tier...`} />;
  const status = statusQ.data;
  if (!status) return null;

  return (
    <div className="mb-6 rounded-2xl border border-neutral-200 bg-white p-4">
      <div className="flex items-center justify-between">
        <p className="flex items-center gap-1.5 text-xs font-bold uppercase tracking-wide text-neutral-500">
          <Award size={14} /> {label} tier
        </p>
        <TrackTierBadge tier={status.current_tier} />
      </div>

      {!status.next_tier && <p className="mt-2 text-sm text-emerald-700">Top tier reached for {label}.</p>}

      {status.next_tier && !assessmentId && (
        <div className="mt-2">
          <p className="text-sm text-neutral-600">
            Next: <span className="font-semibold">{TIER_LABEL[status.next_tier]}</span> -- {status.detail}
          </p>
          <button
            onClick={() => startMutation.mutate()}
            disabled={startMutation.isPending}
            className="mt-2 rounded-lg bg-sky-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-sky-700 disabled:opacity-50"
          >
            Start {TIER_LABEL[status.next_tier]} assessment
          </button>
          {startMutation.data && !startMutation.data.ok && (
            <p className="mt-1 text-xs text-red-600">{startMutation.data.reason}</p>
          )}
        </div>
      )}

      {assessmentId && (
        <div className="mt-2 rounded-xl bg-sky-50 p-3 ring-1 ring-sky-200">
          <p className="text-sm font-semibold text-sky-900">
            Assessment in progress -- clear all of these (aggregate score needs to reach 85%) to advance:
          </p>
          <ul className="mt-2 flex flex-col gap-2">
            {(checkQ.data?.checks ?? []).map((c) => {
              if (c.kind === "quiz" && !c.passed && c.options) {
                return (
                  <li key={c.slug}>
                    <QuizItem
                      track={track} assessmentId={assessmentId} questionId={c.slug} question={c.title}
                      options={c.options}
                      onAnswered={() => checkQ.refetch()}
                    />
                  </li>
                );
              }
              const href = itemHref(c.kind, c.slug);
              return (
                <li key={c.slug} className="flex items-center justify-between gap-2 rounded-lg bg-white px-2.5 py-1.5 text-sm">
                  {href ? (
                    <Link href={href} className="font-medium text-sky-700 hover:underline">{c.title}</Link>
                  ) : (
                    <span className="font-medium text-neutral-700">{c.title}</span>
                  )}
                  <span className={`flex items-center gap-1 text-xs ${c.passed ? "text-emerald-600" : "text-neutral-400"}`}>
                    {c.passed ? <CheckCircle2 size={14} /> : <XCircle size={14} />}
                    {Math.round(c.score * 100)}% -- {c.reason}
                  </span>
                </li>
              );
            })}
          </ul>
          <button
            onClick={() => checkQ.refetch()}
            disabled={checkQ.isFetching}
            className="mt-3 rounded-lg bg-sky-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-sky-700 disabled:opacity-50"
          >
            {checkQ.isFetching ? "Checking..." : "Check my assessment"}
          </button>
          {checkQ.data?.aggregate_score != null && (
            <p className="mt-2 text-xs text-neutral-500">Aggregate score: {Math.round(checkQ.data.aggregate_score * 100)}% (need 85%)</p>
          )}
          {checkQ.data?.status === "passed" && (
            <p className="mt-2 text-sm font-semibold text-emerald-700">Passed! {label} tier advanced to {TIER_LABEL[checkQ.data.target_tier]}.</p>
          )}
          {checkQ.data?.status === "failed" && (
            <p className="mt-2 text-sm font-semibold text-red-600">Not passed this attempt -- keep practicing and start a new assessment when ready.</p>
          )}
        </div>
      )}
    </div>
  );
}
