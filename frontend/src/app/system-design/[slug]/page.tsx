"use client";

import { useMutation, useQuery } from "@tanstack/react-query";
import { useParams } from "next/navigation";
import { useState } from "react";
import { BookOpen } from "lucide-react";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import { LessonActs } from "@/components/LessonActs";
import { Markdown } from "@/components/Markdown";
import { Button, Card, Spinner } from "@/components/ui";
import { api } from "@/lib/api";
import { SystemDesignAttemptResponse, SystemDesignCaseOut } from "@/lib/types";

const COMPONENT_TYPES = [
  "client", "load_balancer", "server", "database", "cache", "queue", "cdn", "object_storage", "search",
];

interface Node { id: string; type: string }
interface Edge { source: string; target: string }

function CaseContent() {
  const params = useParams<{ slug: string }>();
  const slug = params.slug;

  const caseQ = useQuery({
    queryKey: ["sd-case", slug],
    queryFn: async () => (await api.get<SystemDesignCaseOut>(`/system-design/cases/${slug}`)).data,
  });

  const [nodes, setNodes] = useState<Node[]>([]);
  const [edgeSource, setEdgeSource] = useState("");
  const [edgeTarget, setEdgeTarget] = useState("");
  const [edges, setEdges] = useState<Edge[]>([]);
  const [estFields, setEstFields] = useState<{ key: string; value: string }[]>([{ key: "", value: "" }]);
  const [result, setResult] = useState<SystemDesignAttemptResponse | null>(null);
  const [showEditorial, setShowEditorial] = useState(false);

  function addNode(type: string) {
    const count = nodes.filter((n) => n.type === type).length + 1;
    setNodes((prev) => [...prev, { id: `${type}_${count}`, type }]);
  }

  const attemptMutation = useMutation({
    mutationFn: async () => {
      const estimation_answers: Record<string, number> = {};
      for (const f of estFields) {
        if (f.key && f.value) estimation_answers[f.key] = Number(f.value);
      }
      return (
        await api.post<SystemDesignAttemptResponse>(`/system-design/cases/${slug}/attempt`, {
          nodes, edges, estimation_answers,
        })
      ).data;
    },
    onSuccess: setResult,
  });

  if (caseQ.isLoading) return <Spinner label="Loading case study..." />;
  if (!caseQ.data) return <p className="text-red-600">Case not found.</p>;
  const c = caseQ.data;

  return (
    <div className="flex flex-col gap-6">
      <div>
        <div className="flex flex-wrap items-center gap-2">
          <h1 className="text-xl font-bold text-neutral-900 sm:text-2xl">{c.title}</h1>
          {c.scale_tier && (
            <span className="rounded-full bg-purple-100 px-2.5 py-0.5 text-xs font-semibold uppercase tracking-wide text-purple-700">
              {c.scale_tier} scale
            </span>
          )}
        </div>
        {c.scale_description && <p className="mt-1 text-sm italic text-neutral-500">{c.scale_description}</p>}
        <Markdown>{c.description_markdown}</Markdown>
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        <Card>
          <h3 className="font-semibold text-neutral-900">Functional requirements</h3>
          <ul className="list-inside list-disc text-sm text-neutral-700">
            {c.functional_requirements.map((f, i) => <li key={i}>{f}</li>)}
          </ul>
        </Card>
        <Card>
          <h3 className="font-semibold text-neutral-900">Non-functional requirements</h3>
          <ul className="list-inside list-disc text-sm text-neutral-700">
            {c.non_functional_requirements.map((f, i) => <li key={i}>{f}</li>)}
          </ul>
        </Card>
      </div>

      <Card>
        <h3 className="font-semibold text-neutral-900">Estimation</h3>
        <p className="text-sm text-neutral-600">{c.estimation_prompt}</p>
        <div className="mt-2 flex flex-col gap-2">
          {estFields.map((f, i) => (
            <div key={i} className="flex gap-2">
              <input
                placeholder="field name, e.g. write_qps" value={f.key}
                onChange={(e) => setEstFields((prev) => prev.map((x, j) => (j === i ? { ...x, key: e.target.value } : x)))}
                className="flex-1 rounded border border-neutral-300 px-2 py-1 text-sm"
              />
              <input
                placeholder="value" value={f.value} type="number"
                onChange={(e) => setEstFields((prev) => prev.map((x, j) => (j === i ? { ...x, value: e.target.value } : x)))}
                className="w-32 rounded border border-neutral-300 px-2 py-1 text-sm"
              />
            </div>
          ))}
          <button
            onClick={() => setEstFields((prev) => [...prev, { key: "", value: "" }])}
            className="w-fit text-sm text-emerald-700 underline"
          >
            + add field
          </button>
        </div>
      </Card>

      <Card>
        <h3 className="font-semibold text-neutral-900">Architecture</h3>
        <p className="mb-2 text-sm text-neutral-600">Click a component to add it, then connect components below.</p>
        <div className="flex flex-wrap gap-2">
          {COMPONENT_TYPES.map((t) => (
            <button key={t} onClick={() => addNode(t)} className="rounded border border-neutral-300 px-2 py-1 text-xs hover:bg-neutral-50">
              + {t}
            </button>
          ))}
        </div>

        <div className="mt-4 flex flex-wrap gap-2">
          {nodes.map((n) => (
            <span key={n.id} className="rounded-full bg-indigo-600 px-3 py-1 text-xs text-white">
              {n.id}
              <button onClick={() => setNodes((prev) => prev.filter((x) => x.id !== n.id))} className="ml-2 text-indigo-200 hover:text-white">x</button>
            </span>
          ))}
        </div>

        <div className="mt-4 flex items-center gap-2">
          <select value={edgeSource} onChange={(e) => setEdgeSource(e.target.value)} className="rounded border border-neutral-300 px-2 py-1 text-sm">
            <option value="">from...</option>
            {nodes.map((n) => <option key={n.id} value={n.id}>{n.id}</option>)}
          </select>
          <span>→</span>
          <select value={edgeTarget} onChange={(e) => setEdgeTarget(e.target.value)} className="rounded border border-neutral-300 px-2 py-1 text-sm">
            <option value="">to...</option>
            {nodes.map((n) => <option key={n.id} value={n.id}>{n.id}</option>)}
          </select>
          <button
            onClick={() => {
              if (edgeSource && edgeTarget) {
                setEdges((prev) => [...prev, { source: edgeSource, target: edgeTarget }]);
                setEdgeSource(""); setEdgeTarget("");
              }
            }}
            className="rounded bg-indigo-600 px-3 py-1 text-sm text-white hover:bg-indigo-700"
          >
            connect
          </button>
        </div>
        <ul className="mt-2 flex flex-col gap-1 text-sm text-neutral-600">
          {edges.map((e, i) => (
            <li key={i}>
              {e.source} → {e.target}
              <button onClick={() => setEdges((prev) => prev.filter((_, j) => j !== i))} className="ml-2 text-red-500">remove</button>
            </li>
          ))}
        </ul>

        <Button onClick={() => attemptMutation.mutate()} disabled={attemptMutation.isPending || nodes.length === 0} className="mt-4 w-full sm:w-auto">
          Submit design for critique
        </Button>
      </Card>

      {result && (
        <Card>
          <h3 className="font-semibold text-neutral-900">Critique -- score {Math.round(result.score * 100)}%</h3>
          {result.missing_components.length > 0 && (
            <p className="mt-2 text-sm text-red-600">Missing: {result.missing_components.join(", ")}</p>
          )}
          {result.unjustified_components.length > 0 && (
            <p className="mt-1 text-sm text-amber-700">Unjustified additions: {result.unjustified_components.join(", ")}</p>
          )}
          {result.why_questions.length > 0 && (
            <ul className="mt-2 list-inside list-disc text-sm text-neutral-700">
              {result.why_questions.map((q, i) => <li key={i}>{q}</li>)}
            </ul>
          )}
          {result.scope_coach && (
            <div className="mt-3 rounded-lg bg-violet-50 p-2.5 ring-1 ring-violet-200">
              <p className="text-xs font-bold uppercase tracking-wide text-violet-700">
                AI scope coach: {result.scope_coach.scope_verdict.replaceAll("_", " ")}
              </p>
              <p className="mt-0.5 text-xs text-violet-900">{result.scope_coach.coaching_tip}</p>
            </div>
          )}
          <div className="mt-3 flex flex-col gap-1 text-sm">
            {Object.entries(result.estimation_feedback).map(([field, fb]) => (
              <p key={field} className={fb.status === "reasonable" ? "text-emerald-700" : "text-amber-700"}>
                {field}: {fb.status} (you said {fb.submitted ?? "nothing"}, order of magnitude expected ~{fb.expected_order_of_magnitude} {fb.unit})
              </p>
            ))}
          </div>
        </Card>
      )}

      {result && (
        <Card>
          {!showEditorial ? (
            <button
              onClick={() => setShowEditorial(true)}
              className="flex items-center gap-2 text-sm font-semibold text-purple-700 hover:underline"
            >
              <BookOpen size={15} /> See the editorial -- the intended design and why
            </button>
          ) : (
            <>
              <p className="mb-3 flex items-center gap-1.5 text-xs font-bold uppercase tracking-wide text-purple-600">
                <BookOpen size={14} /> Editorial
              </p>
              <LessonActs key={slug} markdown={c.editorial_markdown} />
            </>
          )}
        </Card>
      )}
    </div>
  );
}

export default function CasePage() {
  return (
    <ProtectedRoute>
      <CaseContent />
    </ProtectedRoute>
  );
}
