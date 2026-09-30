"use client";

import { useMemo, useState } from "react";
import { Gauge } from "lucide-react";
import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis, CartesianGrid, Legend } from "recharts";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import { Card, PageHero } from "@/components/ui";

interface Complexity {
  key: string;
  label: string;
  color: string;
  fn: (n: number) => number;
  // Beyond this N, the real value is too astronomically large to be a
  // meaningful data point (and would break the chart's scale) -- shown as
  // "computationally infeasible" in the table instead of a fabricated number.
  feasibleUpTo: number;
}

const COMPLEXITIES: Complexity[] = [
  { key: "constant", label: "O(1)", color: "#0891b2", fn: () => 1, feasibleUpTo: Infinity },
  { key: "log", label: "O(log n)", color: "#059669", fn: (n) => Math.log2(Math.max(1, n)), feasibleUpTo: Infinity },
  { key: "linear", label: "O(n)", color: "#2563eb", fn: (n) => n, feasibleUpTo: Infinity },
  { key: "linearithmic", label: "O(n log n)", color: "#7c3aed", fn: (n) => n * Math.log2(Math.max(1, n)), feasibleUpTo: Infinity },
  { key: "quadratic", label: "O(n^2)", color: "#d97706", fn: (n) => n * n, feasibleUpTo: 100000 },
  { key: "exponential", label: "O(2^n)", color: "#dc2626", fn: (n) => Math.pow(2, n), feasibleUpTo: 60 },
];

// A real, memorized reference point -- a fast modern CPU does roughly this
// many simple operations per second -- so "operations" can be translated
// into an honest, rough real-world time estimate for the table below.
const OPS_PER_SECOND = 1e8;

function formatOps(ops: number): string {
  if (!isFinite(ops)) return "infeasible";
  if (ops < 1000) return Math.round(ops).toLocaleString();
  if (ops < 1e6) return `${(ops / 1e3).toFixed(1)}K`;
  if (ops < 1e9) return `${(ops / 1e6).toFixed(1)}M`;
  if (ops < 1e12) return `${(ops / 1e9).toFixed(1)}B`;
  return ops.toExponential(2);
}

function formatTime(ops: number): string {
  const seconds = ops / OPS_PER_SECOND;
  if (!isFinite(seconds) || seconds > 3.15e7 * 1e6) return "longer than the age of the universe";
  if (seconds < 0.001) return "instant";
  if (seconds < 1) return `${(seconds * 1000).toFixed(1)}ms`;
  if (seconds < 60) return `${seconds.toFixed(1)}s`;
  if (seconds < 3600) return `${(seconds / 60).toFixed(1)} min`;
  if (seconds < 86400) return `${(seconds / 3600).toFixed(1)} hours`;
  if (seconds < 3.15e7) return `${(seconds / 86400).toFixed(1)} days`;
  return `${(seconds / 3.15e7).toExponential(2)} years`;
}

// Log-spaced slider: position 0-100 maps to N from 1 to 1,000,000, so
// dragging feels smooth across every order of magnitude instead of the
// slider being useless for anything past a few thousand.
function sliderToN(pos: number): number {
  return Math.round(Math.pow(10, (pos / 100) * 6));
}
function nToSlider(n: number): number {
  return (Math.log10(Math.max(1, n)) / 6) * 100;
}

export default function ComplexityPlaygroundPage() {
  const [sliderPos, setSliderPos] = useState(nToSlider(100));
  const n = sliderToN(sliderPos);

  const chartData = useMemo(() => {
    const points: Record<string, number>[] = [];
    const steps = 40;
    for (let i = 0; i <= steps; i++) {
      const pointN = Math.max(1, Math.round(Math.pow(10, (i / steps) * Math.log10(n))));
      const row: Record<string, number> = { n: pointN };
      for (const c of COMPLEXITIES) {
        row[c.key] = pointN <= c.feasibleUpTo ? c.fn(pointN) : NaN;
      }
      points.push(row);
    }
    return points;
  }, [n]);

  return (
    <ProtectedRoute>
      <PageHero
        icon={Gauge} title="Complexity Growth Playground" gradient="from-cyan-500 to-blue-500"
        subtitle="Drag the slider and watch, live, why an O(n^2) solution that looks fine on a small example can be unusable at real scale."
      />

      <Card>
        <div className="mb-4">
          <div className="mb-1 flex items-baseline justify-between">
            <label className="text-sm font-semibold text-neutral-900">Input size (n)</label>
            <span className="font-mono text-lg font-bold text-cyan-700">{n.toLocaleString()}</span>
          </div>
          <input
            type="range" min={0} max={100} step={0.5} value={sliderPos}
            onChange={(e) => setSliderPos(Number(e.target.value))}
            className="w-full accent-cyan-600"
          />
          <div className="mt-1 flex justify-between text-[10px] text-neutral-400">
            <span>1</span><span>100</span><span>10,000</span><span>1,000,000</span>
          </div>
        </div>

        <div className="h-72 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData} margin={{ top: 5, right: 10, left: 0, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e5e5" />
              <XAxis dataKey="n" scale="log" domain={["auto", "auto"]} tick={{ fontSize: 10 }} tickFormatter={(v) => formatOps(v)} />
              <YAxis scale="log" domain={["auto", "auto"]} tick={{ fontSize: 10 }} tickFormatter={(v) => formatOps(v)} />
              <Tooltip formatter={(v) => formatOps(Number(v))} labelFormatter={(v) => `n = ${Number(v).toLocaleString()}`} />
              <Legend wrapperStyle={{ fontSize: 12 }} />
              {COMPLEXITIES.map((c) => (
                <Line key={c.key} type="monotone" dataKey={c.key} name={c.label} stroke={c.color} dot={false} strokeWidth={2} connectNulls={false} />
              ))}
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="mt-5 overflow-x-auto">
          <table className="w-full min-w-[500px] text-left text-sm">
            <thead className="text-neutral-500">
              <tr>
                <th className="py-1.5 pr-3 font-medium">Complexity</th>
                <th className="py-1.5 pr-3 font-medium">Operations at n = {n.toLocaleString()}</th>
                <th className="py-1.5 font-medium">~ real time (at 10^8 ops/sec)</th>
              </tr>
            </thead>
            <tbody>
              {COMPLEXITIES.map((c) => {
                const feasible = n <= c.feasibleUpTo;
                const ops = feasible ? c.fn(n) : Infinity;
                return (
                  <tr key={c.key} className="border-t border-neutral-100">
                    <td className="py-1.5 pr-3 font-mono font-semibold" style={{ color: c.color }}>{c.label}</td>
                    <td className="py-1.5 pr-3 font-mono">{feasible ? formatOps(ops) : "computationally infeasible"}</td>
                    <td className="py-1.5 text-neutral-600">{feasible ? formatTime(ops) : "-- would never finish"}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        <p className="mt-4 text-xs text-neutral-500">
          Both axes are on a log scale, which is why a straight line here can still mean explosive real growth --
          it&apos;s what lets six wildly different growth rates share one readable chart. The 10^8 ops/sec figure is
          a real, commonly-cited rough benchmark for a modern CPU doing simple operations, used here only to turn
          an abstract operation count into a relatable time estimate.
        </p>
      </Card>
    </ProtectedRoute>
  );
}
