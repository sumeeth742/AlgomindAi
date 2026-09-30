"use client";

import { useMutation, useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { CheckCircle2, XCircle } from "lucide-react";
import { api } from "@/lib/api";
import { NetworkQuizAnswerOut, NetworkQuizQuestionOut } from "@/lib/types";

function QuizQuestionCard({ question }: { question: NetworkQuizQuestionOut }) {
  const [selected, setSelected] = useState<number | null>(null);
  const [result, setResult] = useState<NetworkQuizAnswerOut | null>(null);

  const submit = useMutation({
    mutationFn: async (selected_index: number) =>
      (await api.post<NetworkQuizAnswerOut>("/networks/quiz/answer", { question_id: question.id, selected_index })).data,
    onSuccess: (data) => setResult(data),
  });

  return (
    <div className="rounded-xl border border-neutral-200 bg-white p-4">
      <p className="mb-3 text-sm font-semibold text-neutral-900">{question.question}</p>
      <div className="flex flex-col gap-2">
        {question.options.map((opt, i) => {
          const isSelected = selected === i;
          const isCorrect = result && i === result.correct_index;
          const isWrongPick = result && isSelected && !result.correct;
          return (
            <button
              key={i}
              disabled={!!result}
              onClick={() => setSelected(i)}
              className={`flex items-center justify-between rounded-lg border px-3 py-2 text-left text-sm transition-colors ${
                result
                  ? isCorrect
                    ? "border-emerald-400 bg-emerald-50 text-emerald-800"
                    : isWrongPick
                    ? "border-red-300 bg-red-50 text-red-700"
                    : "border-neutral-200 text-neutral-500"
                  : isSelected
                  ? "border-blue-500 bg-blue-50"
                  : "border-neutral-200 hover:border-blue-300"
              }`}
            >
              {opt}
              {result && isCorrect && <CheckCircle2 size={16} className="shrink-0 text-emerald-600" />}
              {result && isWrongPick && <XCircle size={16} className="shrink-0 text-red-500" />}
            </button>
          );
        })}
      </div>
      {!result ? (
        <button
          disabled={selected === null || submit.isPending}
          onClick={() => selected !== null && submit.mutate(selected)}
          className="mt-3 rounded-lg bg-blue-600 px-4 py-1.5 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-40"
        >
          Check answer
        </button>
      ) : (
        <p className={`mt-3 rounded-lg p-2.5 text-xs ${result.correct ? "bg-emerald-50 text-emerald-800" : "bg-amber-50 text-amber-800"}`}>
          {result.explanation}
        </p>
      )}
    </div>
  );
}

/** A short practice quiz attached to one Networks lesson -- the immediate-
 * feedback assessment layer this curriculum otherwise lacks (no coding
 * problems the way DSA has, no case studies the way System Design has). */
export function NetworkQuiz({ lessonSlug }: { lessonSlug: string }) {
  const quizQ = useQuery({
    queryKey: ["network-quiz", lessonSlug],
    queryFn: async () => (await api.get<NetworkQuizQuestionOut[]>(`/networks/lessons/${lessonSlug}/quiz`)).data,
  });

  if (!quizQ.data || quizQ.data.length === 0) return null;

  return (
    <div className="mt-6">
      <p className="mb-3 flex items-center gap-1.5 text-xs font-bold uppercase tracking-wide text-blue-700">
        Practice: check your understanding
      </p>
      <div className="flex flex-col gap-3">
        {quizQ.data.map((q) => (
          <QuizQuestionCard key={q.id} question={q} />
        ))}
      </div>
    </div>
  );
}
