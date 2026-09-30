"use client";

import { useMutation } from "@tanstack/react-query";
import { useState } from "react";
import { MessageCircleQuestion, PencilLine, Sparkles } from "lucide-react";
import { api } from "@/lib/api";
import { AskLessonResponse, ExplainBackResponse } from "@/lib/types";

const TIER_TONE: Record<string, string> = {
  STRONG: "bg-emerald-50 text-emerald-800 ring-emerald-200",
  ADEQUATE: "bg-amber-50 text-amber-800 ring-amber-200",
  WEAK: "bg-red-50 text-red-800 ring-red-200",
};

/** Two lesson-level learning aids, shared across DSA skills, System Design
 * lessons, and Networks lessons -- `basePath` is the API prefix for the
 * specific lesson (e.g. "/skills/SLIDING_WINDOW" or
 * "/system-design/lessons/caching-fundamentals"), which both POST endpoints
 * hang off of ("/ask" and "/explain-back"). */
export function LessonCoachPanel({ basePath }: { basePath: string }) {
  const [question, setQuestion] = useState("");
  const [explanation, setExplanation] = useState("");

  const askMutation = useMutation({
    mutationFn: async (q: string) => (await api.post<AskLessonResponse>(`${basePath}/ask`, { question: q })).data,
  });
  const explainMutation = useMutation({
    mutationFn: async (text: string) => (await api.post<ExplainBackResponse>(`${basePath}/explain-back`, { explanation: text })).data,
  });

  return (
    <div className="mt-6 flex flex-col gap-4 border-t border-neutral-200 pt-5">
      <div>
        <p className="mb-2 flex items-center gap-1.5 text-xs font-bold uppercase tracking-wide text-sky-700">
          <MessageCircleQuestion size={14} /> Stuck on something? Ask
        </p>
        <div className="flex gap-2">
          <input
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="e.g. why does this need a hashmap instead of a plain loop?"
            className="flex-1 rounded-lg border border-neutral-300 px-2.5 py-1.5 text-sm outline-none focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
            onKeyDown={(e) => { if (e.key === "Enter" && question.trim()) askMutation.mutate(question); }}
          />
          <button
            onClick={() => question.trim() && askMutation.mutate(question)}
            disabled={!question.trim() || askMutation.isPending}
            className="rounded-lg bg-sky-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-sky-700 disabled:opacity-40"
          >
            {askMutation.isPending ? "Thinking..." : "Ask"}
          </button>
        </div>
        {askMutation.data && (
          <p className="mt-2 rounded-lg bg-sky-50 p-2.5 text-sm text-sky-900 ring-1 ring-sky-200">{askMutation.data.answer}</p>
        )}
        {askMutation.isError && (
          <p className="mt-2 text-xs text-red-600">Couldn&apos;t get an answer -- the local AI model may not be available on the server.</p>
        )}
      </div>

      <div>
        <p className="mb-2 flex items-center gap-1.5 text-xs font-bold uppercase tracking-wide text-violet-700">
          <PencilLine size={14} /> Explain it back, in your own words
        </p>
        <textarea
          value={explanation}
          onChange={(e) => setExplanation(e.target.value)}
          rows={3}
          placeholder="Pretend you're teaching this to a friend -- what is it, and why does it work?"
          className="w-full rounded-lg border border-neutral-300 px-2.5 py-1.5 text-sm outline-none focus:border-violet-500 focus:ring-2 focus:ring-violet-100"
        />
        <button
          onClick={() => explanation.trim() && explainMutation.mutate(explanation)}
          disabled={!explanation.trim() || explainMutation.isPending}
          className="mt-2 flex items-center gap-1.5 rounded-lg bg-violet-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-violet-700 disabled:opacity-40"
        >
          <Sparkles size={14} /> {explainMutation.isPending ? "Checking..." : "Check my explanation"}
        </button>
        {explainMutation.data && (
          <div className={`mt-2 rounded-lg p-2.5 text-sm ring-1 ${TIER_TONE[explainMutation.data.quality_tier] ?? "bg-neutral-50 text-neutral-700 ring-neutral-200"}`}>
            <p className="font-semibold">{explainMutation.data.quality_tier}</p>
            <p className="mt-0.5">{explainMutation.data.coaching_tip}</p>
          </div>
        )}
      </div>
    </div>
  );
}
