"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useParams } from "next/navigation";
import { useState } from "react";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import { AiLabel, Button, Card, SectionTitle } from "@/components/ui";
import { api } from "@/lib/api";
import { AnswerResponse, InterviewMessageOut, InterviewReport } from "@/lib/types";

function InterviewSessionContent() {
  const params = useParams<{ sessionId: string }>();
  const sessionId = params.sessionId;
  const queryClient = useQueryClient();

  const [messages, setMessages] = useState<InterviewMessageOut[] | null>(null);
  const [answer, setAnswer] = useState("");
  const [finished, setFinished] = useState(false);
  const [lastCommentary, setLastCommentary] = useState<string | null>(null);

  const reportQ = useQuery({
    queryKey: ["interview-report", sessionId],
    queryFn: async () => (await api.get<InterviewReport>(`/interviews/${sessionId}/report`)).data,
    enabled: messages === null,
  });

  const answerMutation = useMutation({
    mutationFn: async () => (await api.post<AnswerResponse>(`/interviews/${sessionId}/answer`, { content: answer })).data,
    onSuccess: (data) => {
      setMessages((prev) => [...(prev ?? []), { role: "candidate", stage: data.stage, content: answer }, ...data.messages]);
      setLastCommentary(data.commentary);
      setAnswer("");
      if (data.finished) {
        setFinished(true);
        queryClient.invalidateQueries({ queryKey: ["dashboard"] });
      }
    },
  });

  const transcript = messages ?? reportQ.data?.transcript ?? [];
  const isFinished = finished || (reportQ.data ? reportQ.data.stages_completed >= reportQ.data.total_stages : false);

  return (
    <div className="mx-auto max-w-2xl">
      <SectionTitle>Mock Interview</SectionTitle>
      <Card className="flex flex-col gap-3">
        {transcript.map((m, i) => (
          <div key={i} className={`flex ${m.role === "interviewer" ? "justify-start" : "justify-end"}`}>
            <div
              className={`max-w-[85%] rounded-2xl px-3.5 py-2 text-sm ${
                m.role === "interviewer" ? "bg-neutral-100 text-neutral-800" : "bg-emerald-600 text-white"
              }`}
            >
              {m.content}
            </div>
          </div>
        ))}
        {answerMutation.isPending && (
          <div className="flex justify-start">
            <div className="max-w-[85%] rounded-2xl bg-neutral-100 px-3.5 py-2 text-sm text-neutral-400">...</div>
          </div>
        )}
      </Card>

      {lastCommentary && (
        <div className="mt-3 flex items-start gap-2 rounded-xl border border-violet-200 bg-violet-50 p-3 text-sm text-violet-900">
          <AiLabel />
          <span>{lastCommentary}</span>
        </div>
      )}

      {!isFinished ? (
        <div className="mt-4 flex flex-col gap-2 sm:flex-row">
          <textarea
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
            placeholder="Type your answer..."
            className="flex-1 rounded-lg border border-neutral-300 px-3 py-2 text-sm outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100"
            rows={3}
          />
          <Button onClick={() => answerMutation.mutate()} disabled={!answer.trim() || answerMutation.isPending} className="sm:self-end">
            Send
          </Button>
        </div>
      ) : (
        <div className="mt-4 rounded-xl border border-emerald-300 bg-emerald-50 p-4 text-sm">
          <p className="font-semibold text-emerald-900">Interview complete.</p>
          {reportQ.data && <p className="text-emerald-800">{reportQ.data.summary}</p>}
        </div>
      )}
    </div>
  );
}

export default function InterviewSessionPage() {
  return (
    <ProtectedRoute>
      <InterviewSessionContent />
    </ProtectedRoute>
  );
}
