"use client";

import { useQuery } from "@tanstack/react-query";
import Link from "next/link";
import { ArrowRight, Brain, CheckCircle2, Flame, Lightbulb, RotateCcw, TrendingDown } from "lucide-react";
import { BarChart, Bar, Cell, XAxis, YAxis, ResponsiveContainer, Tooltip, CartesianGrid } from "recharts";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import { Card, SectionTitle, Spinner } from "@/components/ui";
import { api } from "@/lib/api";
import { DashboardOut, HabitProfileOut, RecommendationOut } from "@/lib/types";

// Plain-English versions of the habit profiler's internal category names.
const HABIT_LABEL: Record<string, string> = {
  STRONG_HABITS: "Strong habits",
  SKIPS_PLANNING: "Skips planning",
  HINT_DEPENDENT: "Leans on hints",
  TRIAL_AND_ERROR: "Trial and error",
  DEVELOPING: "Still finding your rhythm",
};

function DashboardContent() {
  const dashboardQ = useQuery({
    queryKey: ["dashboard"],
    queryFn: async () => (await api.get<DashboardOut>("/analytics/dashboard")).data,
  });
  const recsQ = useQuery({
    queryKey: ["recommendations"],
    queryFn: async () => (await api.get<RecommendationOut[]>("/recommendations")).data,
  });
  const habitQ = useQuery({
    queryKey: ["habit-profile"],
    queryFn: async () => (await api.get<HabitProfileOut>("/analytics/habit-profile")).data,
  });

  if (dashboardQ.isLoading) return <Spinner label="Loading dashboard..." />;
  if (dashboardQ.isError || !dashboardQ.data) return <p className="text-red-600">Could not load dashboard. Is the backend running?</p>;

  const d = dashboardQ.data;
  const DIM_COLORS = ["#059669", "#0284c7", "#d97706", "#9333ea", "#e11d48", "#4f46e5", "#0d9488"];
  const chartData = Object.values(d.interview_readiness).map((dim, i) => ({
    name: dim.label,
    score: dim.score !== null ? Math.round(dim.score * 100) : 0,
    color: DIM_COLORS[i % DIM_COLORS.length],
  }));

  return (
    <div className="flex flex-col gap-6 sm:gap-8">
      <div className="overflow-hidden rounded-2xl bg-gradient-to-br from-emerald-600 to-teal-500 p-6 text-white sm:p-8">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <p className="text-xs font-medium uppercase tracking-widest text-emerald-100">Interview Readiness</p>
            <p className="mt-2 text-3xl font-bold sm:text-4xl">
              {d.overall_readiness !== null ? `${Math.round(d.overall_readiness * 100)}%` : "Not enough data yet"}
            </p>
          </div>
          {d.current_streak_days > 0 && (
            <div className="flex items-center gap-2 rounded-xl bg-white/15 px-4 py-2">
              <Flame size={20} className="text-orange-300" />
              <div>
                <p className="text-lg font-bold leading-none">{d.current_streak_days}</p>
                <p className="text-[11px] text-emerald-100">day streak</p>
              </div>
            </div>
          )}
        </div>
        <p className="mt-2 max-w-xl text-sm text-emerald-50">
          {d.overall_readiness !== null
            ? `Based on ${d.total_submissions} submission(s) across the dimensions below.`
            : "Solve a few problems to get your first readiness read."}
        </p>
        <div className="mt-4 flex flex-wrap gap-5 text-sm text-emerald-50">
          <span className="flex items-center gap-1.5"><CheckCircle2 size={15} /> {d.total_solved} problem(s) solved</span>
          <span className="flex items-center gap-1.5"><RotateCcw size={15} /> {d.retention_due_count} review(s) due</span>
          <span className="flex items-center gap-1.5"><Flame size={15} /> active {d.active_days_last_30} of last 30 days</span>
        </div>
      </div>

      <Card>
        <ResponsiveContainer width="100%" height={260}>
          <BarChart data={chartData} layout="vertical" margin={{ left: 24 }}>
            <CartesianGrid strokeDasharray="3 3" horizontal={false} />
            <XAxis type="number" domain={[0, 100]} unit="%" />
            <YAxis type="category" dataKey="name" width={130} tick={{ fontSize: 12 }} />
            <Tooltip formatter={(v) => `${v}%`} />
            <Bar dataKey="score" radius={[0, 6, 6, 0]}>
              {chartData.map((entry, i) => <Cell key={i} fill={entry.color} />)}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
        <p className="mt-2 text-xs text-neutral-500">
          Bars at 0% with no submissions yet mean insufficient evidence, not a measured zero score.
        </p>
      </Card>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card>
          <h2 className="mb-3 flex items-center gap-2 font-semibold text-neutral-900">
            <Lightbulb size={16} className="text-amber-500" /> What to do next
          </h2>
          {recsQ.isLoading && <Spinner label="Loading recommendations..." />}
          {recsQ.data?.length === 0 && <p className="text-sm text-neutral-500">No recommendations yet -- start solving problems.</p>}
          <ul className="flex flex-col gap-4">
            {recsQ.data?.map((r) => (
              <li key={r.id} className="border-l-4 border-emerald-500 pl-3">
                <p className="font-medium text-neutral-900">{r.reason_what}</p>
                <p className="mt-0.5 text-sm text-neutral-600">
                  <span className="font-semibold">Why: </span>{r.reason_why}
                </p>
                <p className="mt-0.5 text-sm text-neutral-500">
                  <span className="font-semibold">Expected outcome: </span>{r.expected_outcome}
                </p>
                {r.problem_slug && (
                  <Link href={`/problems/${r.problem_slug}`} className="mt-1 inline-flex items-center gap-1 text-sm font-medium text-emerald-700 hover:underline">
                    Go to problem <ArrowRight size={14} />
                  </Link>
                )}
                {!r.problem_slug && r.skill_key && (
                  <Link href="/skills" className="mt-1 inline-flex items-center gap-1 text-sm font-medium text-emerald-700 hover:underline">
                    View skill <ArrowRight size={14} />
                  </Link>
                )}
              </li>
            ))}
          </ul>
        </Card>

        <Card>
          <h2 className="mb-3 flex items-center gap-2 font-semibold text-neutral-900">
            <TrendingDown size={16} className="text-red-500" /> Weakest active skills
          </h2>
          {d.weakest_skills.length === 0 && <p className="text-sm text-neutral-500">No skill data yet.</p>}
          <ul className="flex flex-col gap-2">
            {d.weakest_skills.map((s) => (
              <li key={s.skill_key} className="flex items-center justify-between text-sm">
                <span className="text-neutral-700">{s.skill_key}</span>
                <span className="font-mono text-neutral-900">{Math.round(s.mastery * 100)}%</span>
              </li>
            ))}
          </ul>
          <Link href="/retention" className="mt-4 inline-flex items-center gap-1 text-sm font-medium text-emerald-700 hover:underline">
            Go to retention reviews <ArrowRight size={14} />
          </Link>
        </Card>
      </div>

      {habitQ.data?.available && (
        <Card className="bg-gradient-to-br from-violet-50 to-fuchsia-50 ring-1 ring-violet-200">
          <h2 className="mb-2 flex items-center gap-2 font-semibold text-violet-900">
            <Brain size={16} className="text-violet-600" /> Your study habit: {habitQ.data.habit ? HABIT_LABEL[habitQ.data.habit] ?? habitQ.data.habit : ""}
          </h2>
          <p className="text-sm text-violet-800">{habitQ.data.coaching_tip}</p>
          <p className="mt-2 text-xs text-violet-500">
            Based on {habitQ.data.features?.n_submissions} real submissions across {habitQ.data.features?.n_problems_attempted} problems -- not a guess.
          </p>
        </Card>
      )}
    </div>
  );
}

export default function DashboardPage() {
  return (
    <ProtectedRoute>
      <SectionTitle subtitle="What should you learn next, not just how many problems you've solved.">
        Dashboard
      </SectionTitle>
      <DashboardContent />
    </ProtectedRoute>
  );
}
