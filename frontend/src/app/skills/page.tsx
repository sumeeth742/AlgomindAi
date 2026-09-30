"use client";

import { useQuery } from "@tanstack/react-query";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { Eye, GitBranch, Gauge, Lightbulb, Lock, Shuffle } from "lucide-react";
import { useMemo, useState } from "react";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import { ComicPanels } from "@/components/ComicPanels";
import { ConceptBridgePanel } from "@/components/ConceptBridgePanel";
import { ConceptMapStrip } from "@/components/ConceptMapStrip";
import { LessonActs } from "@/components/LessonActs";
import { LessonCoachPanel } from "@/components/LessonCoachPanel";
import { TrackTierPanel } from "@/components/TrackTierPanel";
import { Card, ChapterBadge, PageHero, Spinner, chapterColor } from "@/components/ui";
import { Visualizer } from "@/components/visualizers/Visualizer";
import { api } from "@/lib/api";
import { ConceptMapOut, SkillLessonOut, SkillOut, SkillReadinessOut, TransferChallengeOut, UserSkillOut } from "@/lib/types";
import { VISUALIZATIONS } from "@/lib/visualizations";

type ViewMode = "deep" | "simple";

function SkillsContent() {
  const searchParams = useSearchParams();
  const [openSkill, setOpenSkill] = useState<string | null>(() => searchParams.get("skill"));
  const [viewMode, setViewMode] = useState<ViewMode>("deep");

  const skillsQ = useQuery({
    queryKey: ["skills"],
    queryFn: async () => (await api.get<SkillOut[]>("/skills")).data,
  });
  const myGraphQ = useQuery({
    queryKey: ["my-skill-graph"],
    queryFn: async () => (await api.get<UserSkillOut[]>("/skills/graph/mine")).data,
  });
  const readinessQ = useQuery({
    queryKey: ["skill-readiness"],
    queryFn: async () => (await api.get<SkillReadinessOut[]>("/skills/readiness")).data,
  });
  const lessonQ = useQuery({
    queryKey: ["lesson", openSkill],
    queryFn: async () => (await api.get<SkillLessonOut>(`/skills/${openSkill}/lesson`)).data,
    enabled: !!openSkill,
  });
  const transferQ = useQuery({
    queryKey: ["transfer-challenge", openSkill],
    queryFn: async () => (await api.get<TransferChallengeOut>(`/skills/${openSkill}/transfer-challenge`)).data,
    enabled: !!openSkill,
  });
  const conceptMapQ = useQuery({
    queryKey: ["concept-map", openSkill],
    queryFn: async () => (await api.get<ConceptMapOut>(`/skills/${openSkill}/concept-map`)).data,
    enabled: !!openSkill,
  });

  const masteryByKey = new Map((myGraphQ.data ?? []).map((u) => [u.skill_key, u]));
  const readinessByKey = new Map((readinessQ.data ?? []).map((r) => [r.skill_key, r]));

  const chapters = useMemo(() => {
    const groups = new Map<string, SkillOut[]>();
    for (const s of skillsQ.data ?? []) {
      if (!groups.has(s.chapter)) groups.set(s.chapter, []);
      groups.get(s.chapter)!.push(s);
    }
    return Array.from(groups.entries());
  }, [skillsQ.data]);

  return (
    <div className="flex flex-col gap-6">
      <TrackTierPanel track="dsa" label="DSA" />

      <Link
        href="/skills/complexity-playground"
        className="flex items-center justify-between gap-3 rounded-xl border border-cyan-200 bg-cyan-50 p-3 text-sm hover:border-cyan-300"
      >
        <span className="flex items-center gap-1.5 font-medium text-cyan-900">
          <Gauge size={15} className="text-cyan-600" /> Complexity Growth Playground -- drag a slider, watch O(n^2) explode in real time
        </span>
        <span className="font-semibold text-cyan-700">Open &rarr;</span>
      </Link>
      <div className="grid gap-6 lg:grid-cols-[1fr_1.3fr]">
      <div className="flex flex-col gap-5">
        {skillsQ.isLoading && <Spinner label="Loading skills..." />}
        {chapters.map(([chapter, skills]) => {
          const c = chapterColor(chapter);
          return (
            <div key={chapter}>
              <div className="mb-2"><ChapterBadge chapter={chapter} /></div>
              <ul className="flex flex-col gap-2.5">
                {skills.map((s) => {
                  const us = masteryByKey.get(s.key);
                  const mastery = us?.mastery ?? 0;
                  const active = openSkill === s.key;
                  const readiness = readinessByKey.get(s.key);
                  const locked = readiness && !readiness.ready;
                  return (
                    <li key={s.id}>
                      <button
                        onClick={() => setOpenSkill(s.key)}
                        className={`w-full rounded-2xl p-3.5 text-left shadow-sm transition-all hover:-translate-y-0.5 hover:shadow-md ${
                          active ? `${c.softBg} ring-2 ${c.ring}` : "bg-white"
                        }`}
                      >
                        <div className="flex items-center justify-between">
                          <span className="flex items-center gap-1.5 font-semibold text-neutral-900">
                            {locked && <Lock size={12} className="text-neutral-400" />}
                            {s.name}
                          </span>
                          <span className={`rounded-full px-2 py-0.5 font-mono text-[10px] font-bold ${c.badge}`}>Lv{s.level}</span>
                        </div>
                        <div className="mt-2.5 h-2.5 w-full rounded-full bg-neutral-100">
                          <div className={`h-2.5 rounded-full bg-gradient-to-r ${c.gradient} transition-all`} style={{ width: `${Math.max(4, Math.round(mastery * 100))}%` }} />
                        </div>
                        <div className="mt-1.5 text-xs text-neutral-500">
                          {us ? `${Math.round(mastery * 100)}% progress -- ${us.attempts} attempt(s)` : "Not started"}
                        </div>
                        {locked && (
                          <div className="mt-1 text-xs font-medium text-amber-600">
                            Suggested first: {readiness!.unmet_prerequisites.join(", ")}
                          </div>
                        )}
                      </button>
                    </li>
                  );
                })}
              </ul>
            </div>
          );
        })}
      </div>

      <Card className="lg:sticky lg:top-20 lg:self-start">
        {!openSkill && <p className="text-sm text-neutral-500">Select a skill to view its lesson.</p>}
        {openSkill && lessonQ.isLoading && <Spinner label="Loading lesson..." />}
        {lessonQ.data && (
          <>
            {lessonQ.data.mnemonic && (
              <div className="mb-4 flex gap-2.5 rounded-2xl bg-gradient-to-br from-amber-50 to-orange-50 p-3.5 ring-1 ring-amber-200">
                <Lightbulb size={18} className="mt-0.5 shrink-0 text-amber-500" />
                <div>
                  <p className="text-xs font-bold uppercase tracking-wide text-amber-700">Memory hook</p>
                  <p className="mt-0.5 text-sm font-medium text-amber-900">{lessonQ.data.mnemonic}</p>
                </div>
              </div>
            )}
            {VISUALIZATIONS[lessonQ.data.key] && (
              <div className="mb-6 rounded-2xl bg-gradient-to-br from-emerald-50 via-teal-50 to-sky-50 p-4 ring-1 ring-emerald-200">
                <p className="mb-3 flex items-center gap-1.5 text-xs font-bold uppercase tracking-wide text-emerald-700">
                  <Eye size={15} /> See it in action
                </p>
                <Visualizer config={VISUALIZATIONS[lessonQ.data.key]} />
              </div>
            )}

            {conceptMapQ.data && (
              <ConceptMapStrip
                before={conceptMapQ.data.prerequisites.map((p) => ({ key: p.key, label: p.name }))}
                currentLabel={conceptMapQ.data.current.name}
                after={conceptMapQ.data.unlocks.map((u) => ({ key: u.key, label: u.name }))}
                onNavigate={setOpenSkill}
              />
            )}

            {lessonQ.data.comic_script.length > 0 && (
              <div className="mb-4 flex gap-1 rounded-lg bg-neutral-100 p-1 text-sm font-medium">
                <button
                  onClick={() => setViewMode("deep")}
                  className={`flex-1 rounded-md px-3 py-1.5 transition-colors ${
                    viewMode === "deep" ? "bg-white text-sky-700 shadow-sm" : "text-neutral-500 hover:text-neutral-800"
                  }`}
                >
                  Deep lesson
                </button>
                <button
                  onClick={() => setViewMode("simple")}
                  className={`flex-1 rounded-md px-3 py-1.5 transition-colors ${
                    viewMode === "simple" ? "bg-white text-sky-700 shadow-sm" : "text-neutral-500 hover:text-neutral-800"
                  }`}
                >
                  Simple version 💬
                </button>
              </div>
            )}

            {viewMode === "deep" || lessonQ.data.comic_script.length === 0 ? (
              <LessonActs key={openSkill} markdown={lessonQ.data.concept_markdown} size="lg" />
            ) : (
              <ComicPanels panels={lessonQ.data.comic_script} />
            )}

            {transferQ.data && (
              <div className="mt-6 rounded-xl border border-violet-200 bg-violet-50 p-3">
                <p className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wide text-violet-700">
                  <Shuffle size={14} /> Try it on a new problem
                </p>
                <p className="mt-1 text-sm text-violet-900">{transferQ.data.reason}</p>
                {transferQ.data.available && transferQ.data.problem_slug && (
                  <Link
                    href={`/problems/${transferQ.data.problem_slug}?mode=transfer`}
                    className="mt-2 inline-block rounded-lg bg-violet-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-violet-700"
                  >
                    Try: {transferQ.data.problem_title}
                  </Link>
                )}
              </div>
            )}

            <LessonCoachPanel basePath={`/skills/${openSkill}`} />
            <ConceptBridgePanel domain="dsa" itemKey={`${openSkill}`} />
          </>
        )}
      </Card>
      </div>
    </div>
  );
}

export default function SkillsPage() {
  return (
    <ProtectedRoute>
      <PageHero
        icon={GitBranch} title="DSA Concepts" gradient="from-sky-500 to-cyan-400"
        subtitle="Your progress is tracked one concept at a time, not by chapter -- see exactly where you're weak."
      />
      <SkillsContent />
    </ProtectedRoute>
  );
}
