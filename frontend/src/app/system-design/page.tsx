"use client";

import { useQuery } from "@tanstack/react-query";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { Compass, Eye, Layers, Network } from "lucide-react";
import { useMemo, useState } from "react";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import { ComicPanels } from "@/components/ComicPanels";
import { ConceptBridgePanel } from "@/components/ConceptBridgePanel";
import { ConceptMapStrip } from "@/components/ConceptMapStrip";
import { LessonActs } from "@/components/LessonActs";
import { LessonCoachPanel } from "@/components/LessonCoachPanel";
import { TrackTierPanel } from "@/components/TrackTierPanel";
import { Badge, Card, PageHero, Spinner } from "@/components/ui";
import { FlowDiagram } from "@/components/visualizers/FlowDiagram";
import { api } from "@/lib/api";
import { SD_VISUALIZATIONS } from "@/lib/sdVisualizations";
import { LessonConceptMapOut, LLDCaseOut, SystemDesignCaseOut, SystemDesignLessonOut } from "@/lib/types";

const TIER_ORDER = ["startup", "growth", "global"];
const TIER_LABEL: Record<string, string> = { startup: "Startup", growth: "Growth", global: "Global" };

// Every lesson's `category` maps into exactly one of these three tracks --
// a real, exhaustive split of the whole syllabus so a learner picking a
// track sees a complete, bounded curriculum for it, never a partial slice
// mixed in with unrelated topics.
type Track = "foundations" | "lld" | "hld";
const CATEGORY_TRACK: Record<string, Track> = {
  foundations: "foundations",
  lld: "lld",
  databases: "hld",
  scalability: "hld",
  caching: "hld",
  messaging: "hld",
  "distributed-systems": "hld",
  "advanced-components": "hld",
  estimation: "hld",
  "real-world-systems": "hld",
};

const TRACK_ORDER: Track[] = ["foundations", "lld", "hld"];
const TRACK_META: Record<Track, { label: string; subtitle: string; icon: typeof Compass; gradient: string }> = {
  foundations: {
    label: "System Design Foundations",
    subtitle: "The shared vocabulary both tracks below build on -- clients, servers, HTTP.",
    icon: Compass, gradient: "from-emerald-500 to-teal-400",
  },
  lld: {
    label: "Low-Level Design",
    subtitle: "Classes, relationships, and patterns -- how you structure code inside one service.",
    icon: Layers, gradient: "from-indigo-500 to-blue-400",
  },
  hld: {
    label: "High-Level Design",
    subtitle: "Scaling, caching, databases, and distributed systems -- how services fit together.",
    icon: Network, gradient: "from-purple-500 to-fuchsia-400",
  },
};

function CaseFamily({ cases }: { cases: SystemDesignCaseOut[] }) {
  const sorted = [...cases].sort(
    (a, b) => TIER_ORDER.indexOf(a.scale_tier ?? "") - TIER_ORDER.indexOf(b.scale_tier ?? "")
  );
  const [tier, setTier] = useState(sorted[0]?.scale_tier ?? "");
  const active = sorted.find((c) => c.scale_tier === tier) ?? sorted[0];
  if (!active) return null;

  return (
    <Card className="h-full transition-shadow hover:shadow-md">
      <div className="flex items-center justify-between gap-2">
        <p className="font-semibold text-neutral-900">{active.title}</p>
        <Badge>{active.difficulty}</Badge>
      </div>
      {sorted.length > 1 && (
        <div className="mt-2 flex gap-1 rounded-lg bg-neutral-100 p-1 text-xs font-medium">
          {sorted.map((c) => (
            <button
              key={c.slug}
              onClick={(e) => {
                e.preventDefault();
                setTier(c.scale_tier ?? "");
              }}
              className={`flex-1 rounded-md px-2 py-1 transition-colors ${
                c.scale_tier === tier ? "bg-white text-purple-700 shadow-sm" : "text-neutral-500 hover:text-neutral-800"
              }`}
            >
              {TIER_LABEL[c.scale_tier ?? ""] ?? c.scale_tier}
            </button>
          ))}
        </div>
      )}
      {active.scale_description && (
        <p className="mt-2 text-xs italic text-neutral-500">{active.scale_description}</p>
      )}
      <p className="mt-1 text-sm text-neutral-600">{active.description_markdown}</p>
      <Link href={`/system-design/${active.slug}`} className="mt-3 inline-block text-sm font-semibold text-purple-600 hover:underline">
        Open case study &rarr;
      </Link>
    </Card>
  );
}

type ViewMode = "deep" | "simple";

function SystemDesignContent() {
  const searchParams = useSearchParams();
  const [track, setTrack] = useState<Track>("foundations");
  const [openLesson, setOpenLesson] = useState<string | null>(() => searchParams.get("lesson"));
  const [viewMode, setViewMode] = useState<ViewMode>("deep");

  const lessonsQ = useQuery({
    queryKey: ["sd-lessons"],
    queryFn: async () => (await api.get<SystemDesignLessonOut[]>("/system-design/lessons")).data,
  });
  const casesQ = useQuery({
    queryKey: ["sd-cases"],
    queryFn: async () => (await api.get<SystemDesignCaseOut[]>("/system-design/cases")).data,
    enabled: track === "hld",
  });
  const lldCasesQ = useQuery({
    queryKey: ["lld-cases"],
    queryFn: async () => (await api.get<LLDCaseOut[]>("/lld/cases")).data,
    enabled: track === "lld",
  });

  const trackLessons = useMemo(
    () => (lessonsQ.data ?? []).filter((l) => (CATEGORY_TRACK[l.category] ?? "hld") === track),
    [lessonsQ.data, track]
  );
  const activeLesson = (lessonsQ.data ?? []).find((l) => l.slug === openLesson);

  const conceptMapQ = useQuery({
    queryKey: ["sd-lesson-concept-map", openLesson],
    queryFn: async () => (await api.get<LessonConceptMapOut>(`/system-design/lessons/${openLesson}/concept-map`)).data,
    enabled: !!openLesson,
  });

  const families = new Map<string, SystemDesignCaseOut[]>();
  for (const c of casesQ.data ?? []) {
    const key = c.base_slug ?? c.slug;
    families.set(key, [...(families.get(key) ?? []), c]);
  }

  function selectTrack(t: Track) {
    setTrack(t);
    setOpenLesson(null);
  }

  return (
    <div className="flex flex-col gap-6">
      <TrackTierPanel track="system_design" label="System Design" />

      <div className="grid gap-3 sm:grid-cols-3">
        {TRACK_ORDER.map((t) => {
          const meta = TRACK_META[t];
          const active = track === t;
          return (
            <button
              key={t}
              onClick={() => selectTrack(t)}
              className={`flex items-start gap-3 rounded-2xl border p-4 text-left transition-all ${
                active ? "border-transparent bg-gradient-to-br text-white shadow-md " + meta.gradient : "border-neutral-200 bg-white hover:border-neutral-300"
              }`}
            >
              <span className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-xl ${active ? "bg-white/20" : "bg-neutral-100"}`}>
                <meta.icon size={18} className={active ? "text-white" : "text-neutral-500"} />
              </span>
              <div>
                <p className="font-semibold">{meta.label}</p>
                <p className={`mt-0.5 text-xs ${active ? "text-white/85" : "text-neutral-500"}`}>{meta.subtitle}</p>
              </div>
            </button>
          );
        })}
      </div>

      {track === "hld" && (
        <div>
          <h2 className="mb-1 text-lg font-semibold text-neutral-900">Case Studies</h2>
          <p className="mb-3 text-sm text-neutral-500">
            Same problem, three real-world scales -- switch tiers to see how the correct answer actually changes as
            scale grows, not just how the numbers get bigger.
          </p>
          <div className="grid gap-3 sm:grid-cols-2">
            {casesQ.isLoading && <Spinner label="Loading case studies..." />}
            {[...families.entries()].map(([key, cases]) => (
              <CaseFamily key={key} cases={cases} />
            ))}
          </div>
        </div>
      )}

      {track === "lld" && (
        <div>
          <h2 className="mb-1 text-lg font-semibold text-neutral-900">LLD Practice</h2>
          <p className="mb-3 text-sm text-neutral-500">
            Practical low-level design exercises -- declare the classes you&apos;d build, and get real feedback on
            missing responsibilities, unjustified classes, and whether you actually used inheritance/interfaces
            where the problem calls for it.
          </p>
          <div className="grid gap-3 sm:grid-cols-3">
            {lldCasesQ.isLoading && <Spinner label="Loading LLD exercises..." />}
            {lldCasesQ.data?.map((c) => (
              <Link key={c.id} href={`/system-design/lld/${c.slug}`}>
                <Card className="h-full transition-shadow hover:shadow-md">
                  <div className="flex items-center justify-between gap-2">
                    <p className="font-semibold text-neutral-900">{c.title}</p>
                    <Badge>{c.difficulty}</Badge>
                  </div>
                  <p className="mt-1 text-sm text-neutral-600">{c.description_markdown}</p>
                </Card>
              </Link>
            ))}
          </div>
        </div>
      )}

      <div>
        <h2 className="mb-3 text-lg font-semibold text-neutral-900">
          {TRACK_META[track].label} Lessons
        </h2>
        <div className="grid gap-4 lg:grid-cols-[1fr_1.5fr]">
          <ul className="flex flex-col gap-2">
            {lessonsQ.isLoading && <Spinner label="Loading lessons..." />}
            {trackLessons.map((l) => (
              <li key={l.id}>
                <button
                  onClick={() => setOpenLesson(l.slug)}
                  className={`w-full rounded-xl border p-3 text-left transition-colors ${
                    openLesson === l.slug ? "border-emerald-500 bg-emerald-50" : "border-neutral-200 bg-white hover:border-emerald-300"
                  }`}
                >
                  <span className="text-xs uppercase tracking-wide text-neutral-400">Level {l.level} -- {l.category}</span>
                  <p className="font-medium text-neutral-900">{l.title}</p>
                </button>
              </li>
            ))}
          </ul>
          <Card className="lg:sticky lg:top-20 lg:self-start">
            {!activeLesson && <p className="text-sm text-neutral-500">Select a lesson.</p>}
            {activeLesson && (
              <>
                {SD_VISUALIZATIONS[activeLesson.slug] && (
                  <div className="mb-6 rounded-2xl bg-gradient-to-br from-emerald-50 via-teal-50 to-sky-50 p-4 ring-1 ring-emerald-200">
                    <p className="mb-3 flex items-center gap-1.5 text-xs font-bold uppercase tracking-wide text-emerald-700">
                      <Eye size={15} /> See it in action -- narrated walkthrough
                    </p>
                    <FlowDiagram key={activeLesson.slug} {...SD_VISUALIZATIONS[activeLesson.slug]} />
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
                        viewMode === "deep" ? "bg-white text-purple-700 shadow-sm" : "text-neutral-500 hover:text-neutral-800"
                      }`}
                    >
                      Deep lesson
                    </button>
                    <button
                      onClick={() => setViewMode("simple")}
                      className={`flex-1 rounded-md px-3 py-1.5 transition-colors ${
                        viewMode === "simple" ? "bg-white text-purple-700 shadow-sm" : "text-neutral-500 hover:text-neutral-800"
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
                {activeLesson.dsa_connection && (
                  <div className="mt-4 rounded-lg bg-emerald-50 p-3 text-sm text-emerald-800">
                    <span className="font-semibold">DSA connection: </span>{activeLesson.dsa_connection}
                  </div>
                )}

                <LessonCoachPanel basePath={`/system-design/lessons/${openLesson}`} />
                <ConceptBridgePanel domain="system_design" itemKey={`${openLesson}`} />
              </>
            )}
          </Card>
        </div>
      </div>
    </div>
  );
}

export default function SystemDesignPage() {
  return (
    <ProtectedRoute>
      <PageHero
        icon={Network} title="System Design" gradient="from-purple-500 to-fuchsia-400"
        subtitle="Foundations, Low-Level Design, and High-Level Design -- three complete tracks, not one mixed list."
      />
      <SystemDesignContent />
    </ProtectedRoute>
  );
}
