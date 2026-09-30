"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { CheckCircle2, RotateCcw } from "lucide-react";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import { Button, Card, PageHero, Spinner } from "@/components/ui";
import { api } from "@/lib/api";
import { DueReviewOut } from "@/lib/types";

const RESULTS: { key: string; label: string; variant: "danger" | "primary" | "secondary" | "ghost" }[] = [
  { key: "again", label: "Forgot it", variant: "danger" },
  { key: "hard", label: "Hard to recall", variant: "secondary" },
  { key: "good", label: "Recalled it", variant: "primary" },
  { key: "easy", label: "Instant recall", variant: "ghost" },
];

function RetentionContent() {
  const queryClient = useQueryClient();
  const dueQ = useQuery({
    queryKey: ["retention-due"],
    queryFn: async () => (await api.get<DueReviewOut[]>("/retention/due")).data,
  });

  const submitReview = useMutation({
    mutationFn: async ({ reviewId, result }: { reviewId: string; result: string }) =>
      (await api.post(`/retention/${reviewId}/submit`, { result })).data,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["retention-due"] });
      queryClient.invalidateQueries({ queryKey: ["dashboard"] });
    },
  });

  if (dueQ.isLoading) return <Spinner label="Loading reviews..." />;

  return (
    <>
      {dueQ.data?.length === 0 && (
        <Card>
          <p className="flex items-center gap-2 text-sm text-neutral-500">
            <CheckCircle2 size={16} className="text-emerald-500" /> Nothing due right now -- come back later.
          </p>
        </Card>
      )}
      <div className="flex flex-col gap-4">
        {dueQ.data?.map((r) => (
          <Card key={r.review_id}>
            <p className="font-semibold text-neutral-900">{r.skill_name}</p>
            <p className="text-sm text-neutral-500">
              Repetition #{r.repetitions} -- interval was {r.interval_days} day(s)
            </p>
            <p className="mt-2 text-sm text-neutral-700">
              Recall from memory: what problem clues point to this skill, and how would you implement it?
            </p>
            <div className="mt-3 flex flex-wrap gap-2">
              {RESULTS.map((res) => (
                <Button
                  key={res.key} variant={res.variant}
                  onClick={() => submitReview.mutate({ reviewId: r.review_id, result: res.key })}
                  disabled={submitReview.isPending}
                >
                  {res.label}
                </Button>
              ))}
            </div>
          </Card>
        ))}
      </div>
    </>
  );
}

export default function RetentionPage() {
  return (
    <ProtectedRoute>
      <PageHero
        icon={RotateCcw} title="Retention Reviews" gradient="from-amber-500 to-orange-400"
        subtitle="Try to recall each skill from memory first -- that retrieval effort is what builds retention."
      />
      <RetentionContent />
    </ProtectedRoute>
  );
}
