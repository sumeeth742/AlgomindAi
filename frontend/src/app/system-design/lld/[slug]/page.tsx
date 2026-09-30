"use client";

import { useMutation, useQuery } from "@tanstack/react-query";
import { useParams } from "next/navigation";
import { useState } from "react";
import { BookOpen, Lightbulb, Plus, Trash2 } from "lucide-react";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import { LessonActs } from "@/components/LessonActs";
import { Markdown } from "@/components/Markdown";
import { Button, Card, Spinner } from "@/components/ui";
import { api } from "@/lib/api";
import { LLDAttemptResponse, LLDCaseOut, LLDClassIn } from "@/lib/types";

function emptyClass(): LLDClassIn {
  return { name: "", fields: [], methods: [], extends: null, implements: [] };
}

function ClassEditor({ cls, onChange, onRemove }: {
  cls: LLDClassIn; onChange: (c: LLDClassIn) => void; onRemove: () => void;
}) {
  return (
    <Card className="relative">
      <button onClick={onRemove} className="absolute right-3 top-3 text-neutral-400 hover:text-red-600" title="Remove class">
        <Trash2 size={15} />
      </button>
      <input
        value={cls.name}
        onChange={(e) => onChange({ ...cls, name: e.target.value })}
        placeholder="Class name, e.g. ParkingSpot"
        className="w-full rounded-lg border border-neutral-300 px-2 py-1.5 text-sm font-semibold outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100"
      />
      <div className="mt-2 grid gap-2 sm:grid-cols-2">
        <div>
          <label className="text-xs font-medium text-neutral-500">Fields (comma-separated)</label>
          <input
            value={cls.fields.join(", ")}
            onChange={(e) => onChange({ ...cls, fields: e.target.value.split(",").map((s) => s.trim()).filter(Boolean) })}
            placeholder="licensePlate, size"
            className="mt-0.5 w-full rounded-lg border border-neutral-300 px-2 py-1 text-sm outline-none focus:border-indigo-500"
          />
        </div>
        <div>
          <label className="text-xs font-medium text-neutral-500">Methods (comma-separated)</label>
          <input
            value={cls.methods.join(", ")}
            onChange={(e) => onChange({ ...cls, methods: e.target.value.split(",").map((s) => s.trim()).filter(Boolean) })}
            placeholder="getSize, isAvailable"
            className="mt-0.5 w-full rounded-lg border border-neutral-300 px-2 py-1 text-sm outline-none focus:border-indigo-500"
          />
        </div>
        <div>
          <label className="text-xs font-medium text-neutral-500">Extends (parent class name)</label>
          <input
            value={cls.extends ?? ""}
            onChange={(e) => onChange({ ...cls, extends: e.target.value.trim() || null })}
            placeholder="Vehicle"
            className="mt-0.5 w-full rounded-lg border border-neutral-300 px-2 py-1 text-sm outline-none focus:border-indigo-500"
          />
        </div>
        <div>
          <label className="text-xs font-medium text-neutral-500">Implements (comma-separated interfaces)</label>
          <input
            value={cls.implements.join(", ")}
            onChange={(e) => onChange({ ...cls, implements: e.target.value.split(",").map((s) => s.trim()).filter(Boolean) })}
            placeholder="Drivable"
            className="mt-0.5 w-full rounded-lg border border-neutral-300 px-2 py-1 text-sm outline-none focus:border-indigo-500"
          />
        </div>
      </div>
    </Card>
  );
}

function LLDCaseContent() {
  const params = useParams<{ slug: string }>();
  const slug = params.slug;

  const caseQ = useQuery({
    queryKey: ["lld-case", slug],
    queryFn: async () => (await api.get<LLDCaseOut>(`/lld/cases/${slug}`)).data,
  });

  const [classes, setClasses] = useState<LLDClassIn[]>([emptyClass()]);
  const [result, setResult] = useState<LLDAttemptResponse | null>(null);
  const [showEditorial, setShowEditorial] = useState(false);

  const attemptMutation = useMutation({
    mutationFn: async () => {
      const payload = { classes: classes.filter((c) => c.name.trim()) };
      return (await api.post<LLDAttemptResponse>(`/lld/cases/${slug}/attempt`, payload)).data;
    },
    onSuccess: setResult,
  });

  if (caseQ.isLoading) return <Spinner label="Loading case..." />;
  if (!caseQ.data) return <p className="text-red-600">Case not found.</p>;
  const c = caseQ.data;

  function updateClass(i: number, updated: LLDClassIn) {
    setClasses((prev) => prev.map((cls, j) => (j === i ? updated : cls)));
  }

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-xl font-bold text-neutral-900 sm:text-2xl">{c.title}</h1>
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

      {c.abstraction_hint && (
        <div className="flex items-start gap-2 rounded-xl border border-amber-200 bg-amber-50 px-3 py-2 text-sm text-amber-900">
          <Lightbulb size={16} className="mt-0.5 shrink-0 text-amber-500" />
          {c.abstraction_hint}
        </div>
      )}

      <div>
        <h3 className="mb-2 font-semibold text-neutral-900">Your classes</h3>
        <div className="flex flex-col gap-3">
          {classes.map((cls, i) => (
            <ClassEditor
              key={i} cls={cls}
              onChange={(updated) => updateClass(i, updated)}
              onRemove={() => setClasses((prev) => prev.filter((_, j) => j !== i))}
            />
          ))}
        </div>
        <button
          onClick={() => setClasses((prev) => [...prev, emptyClass()])}
          className="mt-3 flex items-center gap-1.5 text-sm font-semibold text-indigo-600 hover:underline"
        >
          <Plus size={15} /> Add class
        </button>

        <Button
          onClick={() => attemptMutation.mutate()}
          disabled={attemptMutation.isPending || classes.every((c) => !c.name.trim())}
          className="mt-4 w-full sm:w-auto"
        >
          Submit design for critique
        </Button>
      </div>

      {result && (
        <Card>
          <h3 className="font-semibold text-neutral-900">Critique -- score {Math.round(result.score * 100)}%</h3>
          {result.missing_classes.length > 0 && (
            <p className="mt-2 text-sm text-red-600">Missing: {result.missing_classes.join(", ")}</p>
          )}
          {result.extra_classes.length > 0 && (
            <p className="mt-1 text-sm text-amber-700">Unrecognized additions: {result.extra_classes.join(", ")}</p>
          )}
          <p className={`mt-1 text-sm ${result.uses_abstraction ? "text-emerald-700" : "text-amber-700"}`}>
            {result.uses_abstraction
              ? "Uses at least one inheritance/interface relationship."
              : "No inheritance/interface relationship detected -- review whether the problem calls for one."}
          </p>
          {result.god_classes.length > 0 && (
            <p className="mt-1 text-sm text-amber-700">Possible God Class (too many methods): {result.god_classes.join(", ")}</p>
          )}
          {result.why_questions.length > 0 && (
            <ul className="mt-2 list-inside list-disc text-sm text-neutral-700">
              {result.why_questions.map((q, i) => <li key={i}>{q}</li>)}
            </ul>
          )}
        </Card>
      )}

      {result && (
        <Card>
          {!showEditorial ? (
            <button
              onClick={() => setShowEditorial(true)}
              className="flex items-center gap-2 text-sm font-semibold text-indigo-700 hover:underline"
            >
              <BookOpen size={15} /> See the editorial -- the intended class design and why
            </button>
          ) : (
            <>
              <p className="mb-3 flex items-center gap-1.5 text-xs font-bold uppercase tracking-wide text-indigo-600">
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

export default function LLDCasePage() {
  return (
    <ProtectedRoute>
      <LLDCaseContent />
    </ProtectedRoute>
  );
}
