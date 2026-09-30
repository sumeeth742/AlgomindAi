"use client";

import { useQuery } from "@tanstack/react-query";
import Link from "next/link";
import { Trophy } from "lucide-react";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import { Badge, Card, PageHero, Spinner } from "@/components/ui";
import { api } from "@/lib/api";
import { ContestOut } from "@/lib/types";

const STATUS_TONE: Record<ContestOut["status"], "emerald" | "amber" | "neutral"> = {
  live: "emerald",
  upcoming: "amber",
  ended: "neutral",
};
const STATUS_LABEL: Record<ContestOut["status"], string> = {
  live: "Live now",
  upcoming: "Upcoming",
  ended: "Ended",
};

function formatDate(iso: string): string {
  return new Date(iso + "Z").toLocaleString(undefined, {
    month: "short", day: "numeric", hour: "numeric", minute: "2-digit",
  });
}

function ContestsContent() {
  const contestsQ = useQuery({
    queryKey: ["contests"],
    queryFn: async () => (await api.get<ContestOut[]>("/contests")).data,
  });

  const contests = contestsQ.data ?? [];
  const order: Record<ContestOut["status"], number> = { live: 0, upcoming: 1, ended: 2 };
  const sorted = [...contests].sort((a, b) => order[a.status] - order[b.status]);

  return (
    <div className="flex flex-col gap-3">
      {contestsQ.isLoading && <Spinner label="Loading contests..." />}
      {!contestsQ.isLoading && sorted.length === 0 && (
        <p className="text-sm text-neutral-500">No contests scheduled yet.</p>
      )}
      {sorted.map((c) => (
        <Link key={c.id} href={`/contests/${c.id}`}>
          <Card className="transition-shadow hover:shadow-md">
            <div className="flex flex-wrap items-center justify-between gap-2">
              <p className="font-semibold text-neutral-900">{c.title}</p>
              <Badge tone={STATUS_TONE[c.status]}>{STATUS_LABEL[c.status]}</Badge>
            </div>
            <p className="mt-1 text-sm text-neutral-500">
              {formatDate(c.start_at)} -- {formatDate(c.end_at)} -- {c.problem_count} problem{c.problem_count === 1 ? "" : "s"}
            </p>
          </Card>
        </Link>
      ))}
    </div>
  );
}

export default function ContestsPage() {
  return (
    <ProtectedRoute>
      <PageHero
        icon={Trophy} title="Contests" gradient="from-yellow-500 to-amber-400"
        subtitle="Timed, competitive rounds -- solve for real under a clock, no hints, ranked on a live leaderboard."
      />
      <ContestsContent />
    </ProtectedRoute>
  );
}
