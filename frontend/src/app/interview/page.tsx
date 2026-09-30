"use client";

import { useMutation, useQuery } from "@tanstack/react-query";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { Layers, MessageSquare } from "lucide-react";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import { Button, Card, PageHero } from "@/components/ui";
import { api } from "@/lib/api";
import { ProblemListItem, StartInterviewResponse, SystemDesignCaseOut } from "@/lib/types";

function InterviewContent() {
  const router = useRouter();
  const [type, setType] = useState<"dsa" | "system_design">("dsa");
  const [problemSlug, setProblemSlug] = useState("");
  const [caseSlug, setCaseSlug] = useState("");

  const problemsQ = useQuery({
    queryKey: ["problems"],
    queryFn: async () => (await api.get<ProblemListItem[]>("/problems")).data,
  });
  const casesQ = useQuery({
    queryKey: ["sd-cases"],
    queryFn: async () => (await api.get<SystemDesignCaseOut[]>("/system-design/cases")).data,
  });

  const startMutation = useMutation({
    mutationFn: async () =>
      (
        await api.post<StartInterviewResponse>("/interviews/start", {
          type,
          problem_slug: type === "dsa" ? problemSlug : undefined,
          case_slug: type === "system_design" ? caseSlug : undefined,
        })
      ).data,
    onSuccess: (data) => router.push(`/interview/${data.session_id}`),
  });

  return (
    <div className="mx-auto max-w-lg">
      <PageHero
        icon={MessageSquare} title="Mock Interview" gradient="from-pink-500 to-rose-400"
        subtitle="Walks through real interview questions step by step and checks whether you covered the key points -- a small local AI can add extra commentary, but it never decides your score."
      />
      <Card className="flex flex-col gap-4">
        <div className="flex gap-4 text-sm">
          <label className="flex items-center gap-1.5">
            <input type="radio" checked={type === "dsa"} onChange={() => setType("dsa")} /> DSA
          </label>
          <label className="flex items-center gap-1.5">
            <input type="radio" checked={type === "system_design"} onChange={() => setType("system_design")} /> System Design
          </label>
        </div>

        {type === "dsa" && (
          <select value={problemSlug} onChange={(e) => setProblemSlug(e.target.value)} className="rounded-lg border border-neutral-300 px-2 py-2 text-sm">
            <option value="">Choose a problem...</option>
            {problemsQ.data?.map((p) => <option key={p.slug} value={p.slug}>{p.title}</option>)}
          </select>
        )}
        {type === "system_design" && (
          <select value={caseSlug} onChange={(e) => setCaseSlug(e.target.value)} className="rounded-lg border border-neutral-300 px-2 py-2 text-sm">
            <option value="">Choose a case study...</option>
            {casesQ.data?.map((c) => <option key={c.slug} value={c.slug}>{c.title}</option>)}
          </select>
        )}

        <Button onClick={() => startMutation.mutate()} disabled={startMutation.isPending || (type === "dsa" ? !problemSlug : !caseSlug)}>
          Start Interview
        </Button>
      </Card>

      <Link
        href="/interview/full-loop"
        className="mt-4 flex items-center justify-between gap-3 rounded-xl border border-rose-200 bg-rose-50 p-3 text-sm hover:border-rose-300"
      >
        <span className="flex items-center gap-1.5 font-medium text-rose-900">
          <Layers size={15} className="text-rose-600" /> Full Mock Interview Loop -- one DSA problem + one System Design case + one behavioral question, timed back-to-back
        </span>
        <span className="font-semibold text-rose-700">Start &rarr;</span>
      </Link>
    </div>
  );
}

export default function InterviewPage() {
  return (
    <ProtectedRoute>
      <InterviewContent />
    </ProtectedRoute>
  );
}
