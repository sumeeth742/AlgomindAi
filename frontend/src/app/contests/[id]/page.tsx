"use client";

import { useQuery } from "@tanstack/react-query";
import Link from "next/link";
import { useParams } from "next/navigation";
import { Trophy, Medal } from "lucide-react";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import { Badge, Card, Spinner } from "@/components/ui";
import { api } from "@/lib/api";
import { ContestDetailOut, LeaderboardEntryOut } from "@/lib/types";

const STATUS_TONE: Record<ContestDetailOut["status"], "emerald" | "amber" | "neutral"> = {
  live: "emerald",
  upcoming: "amber",
  ended: "neutral",
};
const STATUS_LABEL: Record<ContestDetailOut["status"], string> = {
  live: "Live now",
  upcoming: "Upcoming",
  ended: "Ended",
};
const DIFFICULTY_TONE: Record<string, "emerald" | "amber" | "red" | "purple"> = {
  easy: "emerald", medium: "amber", hard: "red", expert: "purple",
};

function formatDate(iso: string): string {
  return new Date(iso + "Z").toLocaleString(undefined, {
    month: "short", day: "numeric", hour: "numeric", minute: "2-digit",
  });
}

function ContestDetailContent() {
  const params = useParams<{ id: string }>();
  const contestId = params.id;

  const contestQ = useQuery({
    queryKey: ["contest-detail", contestId],
    queryFn: async () => (await api.get<ContestDetailOut>(`/contests/${contestId}`)).data,
    refetchInterval: (q) => (q.state.data?.status === "live" ? 15000 : false),
  });

  const leaderboardQ = useQuery({
    queryKey: ["contest-leaderboard", contestId],
    queryFn: async () => (await api.get<LeaderboardEntryOut[]>(`/contests/${contestId}/leaderboard`)).data,
    refetchInterval: () => (contestQ.data?.status === "live" ? 15000 : false),
    enabled: !!contestQ.data,
  });

  if (contestQ.isLoading) return <Spinner label="Loading contest..." />;
  const c = contestQ.data;
  if (!c) return <p className="text-red-600">Contest not found.</p>;

  return (
    <div className="flex flex-col gap-6">
      <div className={`overflow-hidden rounded-2xl bg-gradient-to-br from-yellow-500 to-amber-400 p-5 text-white shadow-lg sm:p-7`}>
        <div className="flex items-center gap-3.5">
          <span className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-white/20">
            <Trophy size={24} />
          </span>
          <div>
            <div className="flex flex-wrap items-center gap-2">
              <h1 className="text-xl font-bold sm:text-2xl">{c.title}</h1>
              <Badge tone={STATUS_TONE[c.status]}>{STATUS_LABEL[c.status]}</Badge>
            </div>
            <p className="mt-0.5 text-sm text-white/85">
              {formatDate(c.start_at)} -- {formatDate(c.end_at)}
            </p>
          </div>
        </div>
      </div>

      {c.status === "upcoming" && (
        <Card>
          <p className="text-sm text-neutral-600">
            Problems for this contest aren&apos;t revealed until it starts. Come back at {formatDate(c.start_at)}.
          </p>
        </Card>
      )}

      {c.status !== "upcoming" && (
        <div className="grid gap-4 lg:grid-cols-[1.3fr_1fr]">
          <div>
            <h2 className="mb-3 text-lg font-semibold text-neutral-900">Problems</h2>
            <div className="flex flex-col gap-2.5">
              {c.problems.map((p) => (
                <Link
                  key={p.slug}
                  href={`/problems/${p.slug}?contestId=${c.id}&contestTitle=${encodeURIComponent(c.title)}`}
                >
                  <Card className="flex items-center justify-between transition-shadow hover:shadow-md">
                    <p className="font-medium text-neutral-900">{p.title}</p>
                    <Badge tone={DIFFICULTY_TONE[p.difficulty]}>{p.difficulty}</Badge>
                  </Card>
                </Link>
              ))}
            </div>
            {c.status === "ended" && (
              <p className="mt-3 text-xs text-neutral-400">
                This contest has ended -- you can still solve these for practice, but it no longer affects the leaderboard.
              </p>
            )}
          </div>

          <div>
            <h2 className="mb-3 flex items-center gap-1.5 text-lg font-semibold text-neutral-900">
              <Medal size={18} className="text-amber-500" /> Leaderboard
            </h2>
            <Card>
              {leaderboardQ.isLoading && <Spinner label="Loading leaderboard..." />}
              {leaderboardQ.data && leaderboardQ.data.length === 0 && (
                <p className="text-sm text-neutral-500">No one has scored yet -- be the first.</p>
              )}
              {leaderboardQ.data && leaderboardQ.data.length > 0 && (
                <ul className="flex flex-col gap-1.5">
                  {leaderboardQ.data.map((e) => (
                    <li key={e.rank} className="flex items-center justify-between gap-2 rounded-lg px-2 py-1.5 text-sm odd:bg-neutral-50">
                      <span className="flex items-center gap-2">
                        <span className="w-5 shrink-0 text-right font-mono text-xs text-neutral-400">#{e.rank}</span>
                        <span className="font-medium text-neutral-800">{e.user_name}</span>
                      </span>
                      <span className="text-xs text-neutral-500">{e.total_score} pts -- {e.problems_solved} solved</span>
                    </li>
                  ))}
                </ul>
              )}
            </Card>
          </div>
        </div>
      )}
    </div>
  );
}

export default function ContestDetailPage() {
  return (
    <ProtectedRoute>
      <ContestDetailContent />
    </ProtectedRoute>
  );
}
