"use client";

import { useMutation, useQuery } from "@tanstack/react-query";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useMemo, useState } from "react";
import { CheckCircle2, Circle, Code2, EyeOff, MinusCircle } from "lucide-react";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import { Badge, Button, ChapterBadge, PageHero, Spinner } from "@/components/ui";
import { api } from "@/lib/api";
import { BlindPracticeOut, ProblemListItem, SkillOut } from "@/lib/types";

const DIFFICULTY_TONE: Record<string, "emerald" | "amber" | "red" | "purple"> = {
  easy: "emerald", medium: "amber", hard: "red", expert: "purple",
};

const DIFFICULTIES = ["easy", "medium", "hard", "expert"];
const STATUSES = [
  { value: "", label: "Any status" },
  { value: "solved", label: "Solved" },
  { value: "attempted", label: "Attempted, not solved" },
  { value: "untried", label: "Not tried yet" },
];

function StatusIcon({ p }: { p: ProblemListItem }) {
  if (p.solved) return <CheckCircle2 size={16} className="text-emerald-600" />;
  if (p.attempted) return <MinusCircle size={16} className="text-amber-500" />;
  return <Circle size={16} className="text-neutral-300" />;
}

function ProblemsContent() {
  const router = useRouter();
  const [skillFilter, setSkillFilter] = useState("");
  const [difficultyFilter, setDifficultyFilter] = useState("");
  const [statusFilter, setStatusFilter] = useState("");

  const blindMutation = useMutation({
    mutationFn: async () => (await api.get<BlindPracticeOut>("/problems/blind/random")).data,
    onSuccess: (data) => {
      if (data.available && data.problem_slug) router.push(`/problems/${data.problem_slug}?mode=blind`);
    },
  });

  const skillsQ = useQuery({
    queryKey: ["skills"],
    queryFn: async () => (await api.get<SkillOut[]>("/skills")).data,
  });
  const problemsQ = useQuery({
    queryKey: ["problems"],
    queryFn: async () => (await api.get<ProblemListItem[]>("/problems")).data,
  });

  const filtered = useMemo(() => {
    return (problemsQ.data ?? []).filter((p) => {
      if (skillFilter && p.primary_skill_key !== skillFilter) return false;
      if (difficultyFilter && p.difficulty !== difficultyFilter) return false;
      if (statusFilter === "solved" && !p.solved) return false;
      if (statusFilter === "attempted" && !(p.attempted && !p.solved)) return false;
      if (statusFilter === "untried" && p.attempted) return false;
      return true;
    });
  }, [problemsQ.data, skillFilter, difficultyFilter, statusFilter]);

  const skillsUsed = useMemo(() => {
    const keys = new Set((problemsQ.data ?? []).map((p) => p.primary_skill_key));
    return (skillsQ.data ?? []).filter((s) => keys.has(s.key));
  }, [problemsQ.data, skillsQ.data]);

  const chapterByKey = useMemo(
    () => new Map((skillsQ.data ?? []).map((s) => [s.key, s.chapter])),
    [skillsQ.data]
  );

  const solvedCount = (problemsQ.data ?? []).filter((p) => p.solved).length;

  if (problemsQ.isLoading) return <Spinner label="Loading problems..." />;

  return (
    <>
      <div className="mb-4 flex flex-wrap items-center gap-3">
        <select
          value={skillFilter} onChange={(e) => setSkillFilter(e.target.value)}
          className="rounded-lg border border-neutral-300 px-3 py-1.5 text-sm"
        >
          <option value="">All skills</option>
          {skillsUsed.map((s) => <option key={s.key} value={s.key}>{s.name}</option>)}
        </select>
        <select
          value={difficultyFilter} onChange={(e) => setDifficultyFilter(e.target.value)}
          className="rounded-lg border border-neutral-300 px-3 py-1.5 text-sm"
        >
          <option value="">All difficulties</option>
          {DIFFICULTIES.map((d) => <option key={d} value={d}>{d}</option>)}
        </select>
        <select
          value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}
          className="rounded-lg border border-neutral-300 px-3 py-1.5 text-sm"
        >
          {STATUSES.map((s) => <option key={s.value} value={s.value}>{s.label}</option>)}
        </select>
        {(skillFilter || difficultyFilter || statusFilter) && (
          <button
            onClick={() => { setSkillFilter(""); setDifficultyFilter(""); setStatusFilter(""); }}
            className="text-sm text-neutral-500 underline"
          >
            Clear filters
          </button>
        )}
        <span className="ml-auto self-center text-sm text-neutral-400">
          {solvedCount}/{(problemsQ.data ?? []).length} solved -- showing {filtered.length}
        </span>
      </div>

      <div className="mb-4 flex items-center justify-between gap-3 rounded-xl border border-indigo-200 bg-indigo-50 p-3">
        <div>
          <p className="flex items-center gap-1.5 text-sm font-medium text-indigo-900">
            <EyeOff size={15} /> Blind Practice
          </p>
          <p className="text-xs text-indigo-700">
            A random problem, no skill or difficulty hint -- forces you to recognize the pattern yourself instead of already knowing it from the chapter you clicked into.
          </p>
        </div>
        <Button variant="secondary" onClick={() => blindMutation.mutate()} disabled={blindMutation.isPending}>
          {blindMutation.isPending ? "Picking..." : "Start"}
        </Button>
      </div>

      <div className="overflow-hidden rounded-xl border border-neutral-200 bg-white shadow-sm">
        <div className="overflow-x-auto">
          <table className="w-full min-w-[560px] text-left text-sm">
            <thead className="bg-neutral-50 text-neutral-500">
              <tr>
                <th className="px-4 py-2.5 font-medium"></th>
                <th className="px-4 py-2.5 font-medium">Title</th>
                <th className="px-4 py-2.5 font-medium">Skill</th>
                <th className="px-4 py-2.5 font-medium">Difficulty</th>
                <th className="px-4 py-2.5 font-medium">Pattern Difficulty</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((p) => (
                <tr key={p.id} className="border-t border-neutral-100 hover:bg-neutral-50">
                  <td className="px-4 py-3"><StatusIcon p={p} /></td>
                  <td className="px-4 py-3">
                    <Link href={`/problems/${p.slug}`} className="font-medium text-emerald-700 hover:underline">
                      {p.title}
                    </Link>
                  </td>
                  <td className="px-4 py-3">
                    <ChapterBadge chapter={chapterByKey.get(p.primary_skill_key) ?? p.primary_skill_key} />
                  </td>
                  <td className="px-4 py-3">
                    <Badge tone={DIFFICULTY_TONE[p.difficulty]}>{p.difficulty}</Badge>
                  </td>
                  <td className="px-4 py-3 text-amber-500">{"★".repeat(p.pattern_difficulty)}<span className="text-neutral-200">{"★".repeat(5 - p.pattern_difficulty)}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}

export default function ProblemsPage() {
  return (
    <ProtectedRoute>
      <PageHero
        icon={Code2} title="Problems" gradient="from-indigo-500 to-blue-400"
        subtitle="Progress from easy familiar problems to unfamiliar variants -- not by problem count."
      />
      <ProblemsContent />
    </ProtectedRoute>
  );
}
