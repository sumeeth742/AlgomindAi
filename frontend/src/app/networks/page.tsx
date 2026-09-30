"use client";

import { useQuery } from "@tanstack/react-query";
import { useSearchParams } from "next/navigation";
import { Eye, Wifi } from "lucide-react";
import { useMemo, useState } from "react";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import { ComicPanels } from "@/components/ComicPanels";
import { ConceptBridgePanel } from "@/components/ConceptBridgePanel";
import { ConceptMapStrip } from "@/components/ConceptMapStrip";
import { LessonActs } from "@/components/LessonActs";
import { LessonCoachPanel } from "@/components/LessonCoachPanel";
import { NetworkQuiz } from "@/components/NetworkQuiz";
import { Card, PageHero, Spinner } from "@/components/ui";
import { FlowDiagram } from "@/components/visualizers/FlowDiagram";
import { api } from "@/lib/api";
import { NETWORK_VISUALIZATIONS } from "@/lib/networkVisualizations";
import { LessonConceptMapOut, NetworkLessonOut } from "@/lib/types";

// Every network lesson's `category` maps to one of these five real groupings
// covering the whole curriculum end to end -- from physical topology all the
// way up to application-level socket programming -- so a learner can see the
// complete, bounded scope of the syllabus rather than one flat list.
const CATEGORY_ORDER = ["fundamentals", "data-link-network", "transport", "security", "application-practice"];
const CATEGORY_LABEL: Record<string, string> = {
  fundamentals: "Fundamentals",
  "data-link-network": "Data Link & Network Layer",
  transport: "Transport Layer",
  security: "Network Security",
  "application-practice": "Application Layer & Practice",
};

type ViewMode = "deep" | "simple";

function NetworksContent() {
  const searchParams = useSearchParams();
  const [openLesson, setOpenLesson] = useState<string | null>(() => searchParams.get("lesson"));
  const [viewMode, setViewMode] = useState<ViewMode>("deep");

  const lessonsQ = useQuery({
    queryKey: ["network-lessons"],
    queryFn: async () => (await api.get<NetworkLessonOut[]>("/networks/lessons")).data,
  });

  const byCategory = useMemo(() => {
    const map = new Map<string, NetworkLessonOut[]>();
    for (const l of lessonsQ.data ?? []) {
      map.set(l.category, [...(map.get(l.category) ?? []), l]);
    }
    for (const list of map.values()) list.sort((a, b) => a.level - b.level);
    return map;
  }, [lessonsQ.data]);

  const activeLesson = (lessonsQ.data ?? []).find((l) => l.slug === openLesson);

  const conceptMapQ = useQuery({
    queryKey: ["network-lesson-concept-map", openLesson],
    queryFn: async () => (await api.get<LessonConceptMapOut>(`/networks/lessons/${openLesson}/concept-map`)).data,
    enabled: !!openLesson,
  });

  return (
    <div className="flex flex-col gap-6">
      <div className="grid gap-4 lg:grid-cols-[1fr_1.5fr]">
        <div className="flex flex-col gap-4">
          {lessonsQ.isLoading && <Spinner label="Loading lessons..." />}
          {CATEGORY_ORDER.filter((c) => byCategory.has(c)).map((category) => (
            <div key={category}>
              <h2 className="mb-2 text-sm font-bold uppercase tracking-wide text-blue-700">
                {CATEGORY_LABEL[category] ?? category}
              </h2>
              <ul className="flex flex-col gap-2">
                {byCategory.get(category)!.map((l) => (
                  <li key={l.id}>
                    <button
                      onClick={() => setOpenLesson(l.slug)}
                      className={`w-full rounded-xl border p-3 text-left transition-colors ${
                        openLesson === l.slug ? "border-blue-500 bg-blue-50" : "border-neutral-200 bg-white hover:border-blue-300"
                      }`}
                    >
                      <span className="text-xs uppercase tracking-wide text-neutral-400">Level {l.level}</span>
                      <p className="font-medium text-neutral-900">{l.title}</p>
                    </button>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <Card className="lg:sticky lg:top-20 lg:self-start">
          {!activeLesson && <p className="text-sm text-neutral-500">Select a lesson.</p>}
          {activeLesson && (
            <>
              {NETWORK_VISUALIZATIONS[activeLesson.slug] && (
                <div className="mb-6 rounded-2xl bg-gradient-to-br from-sky-50 via-blue-50 to-cyan-50 p-4 ring-1 ring-sky-200">
                  <p className="mb-3 flex items-center gap-1.5 text-xs font-bold uppercase tracking-wide text-sky-700">
                    <Eye size={15} /> See it in action -- narrated walkthrough
                  </p>
                  <FlowDiagram key={activeLesson.slug} {...NETWORK_VISUALIZATIONS[activeLesson.slug]} />
                </div>
              )}
              {conceptMapQ.data && (
                <ConceptMapStrip
                  before={conceptMapQ.data.previous ? [{ key: conceptMapQ.data.previous.slug, label: conceptMapQ.data.previous.title }] : []}
                  currentLabel={conceptMapQ.data.current.title}
                  after={conceptMapQ.data.next ? [{ key: conceptMapQ.data.next.slug, label: conceptMapQ.data.next.title }] : []}
                  onNavigate={setOpenLesson}
                />
              )}

              {activeLesson.comic_script.length > 0 && (
                <div className="mb-4 flex gap-1 rounded-lg bg-neutral-100 p-1 text-sm font-medium">
                  <button
                    onClick={() => setViewMode("deep")}
                    className={`flex-1 rounded-md px-3 py-1.5 transition-colors ${
                      viewMode === "deep" ? "bg-white text-blue-700 shadow-sm" : "text-neutral-500 hover:text-neutral-800"
                    }`}
                  >
                    Deep lesson
                  </button>
                  <button
                    onClick={() => setViewMode("simple")}
                    className={`flex-1 rounded-md px-3 py-1.5 transition-colors ${
                      viewMode === "simple" ? "bg-white text-blue-700 shadow-sm" : "text-neutral-500 hover:text-neutral-800"
                    }`}
                  >
                    Simple version 💬
                  </button>
                </div>
              )}

              {viewMode === "deep" || activeLesson.comic_script.length === 0 ? (
                <LessonActs key={openLesson} markdown={activeLesson.content_markdown} size="lg" />
              ) : (
                <ComicPanels panels={activeLesson.comic_script} />
              )}

              {activeLesson.practical_connection && (
                <div className="mt-4 rounded-lg bg-blue-50 p-3 text-sm text-blue-800">
                  <span className="font-semibold">Practical connection: </span>{activeLesson.practical_connection}
                </div>
              )}

              <NetworkQuiz lessonSlug={activeLesson.slug} />

              <LessonCoachPanel basePath={`/networks/lessons/${activeLesson.slug}`} />
              <ConceptBridgePanel domain="networks" itemKey={activeLesson.slug} />
            </>
          )}
        </Card>
      </div>
    </div>
  );
}

export default function NetworksPage() {
  return (
    <ProtectedRoute>
      <PageHero
        icon={Wifi} title="Computer Networks" gradient="from-blue-500 to-cyan-400"
        subtitle="A genuinely separate, deep curriculum -- from physical topology and MAC addressing all the way up to TLS, VPNs, and socket programming."
      />
      <NetworksContent />
    </ProtectedRoute>
  );
}
