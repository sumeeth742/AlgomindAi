"use client";

import { StepControls, StepNote, useSteps } from "./shared";

export interface GrowthStep {
  n: number;
  values: { label: string; ops: number; color: string }[];
  note: string;
}

export function GrowthChartViz({ steps }: { steps: GrowthStep[] }) {
  const state = useSteps(steps.length);
  const step = steps[state.index];
  const maxOps = Math.max(...step.values.map((v) => v.ops), 1);

  return (
    <div className="flex flex-col gap-3">
      <p className="text-center font-mono text-sm text-neutral-500">n = {step.n.toLocaleString()}</p>
      <div className="flex flex-col gap-2">
        {step.values.map((v, i) => (
          <div key={i} className="flex items-center gap-2">
            <span className="w-24 shrink-0 font-mono text-xs text-neutral-600">{v.label}</span>
            <div className="h-5 flex-1 rounded-full bg-neutral-100">
              <div
                className="h-5 rounded-full transition-all duration-300"
                style={{ width: `${Math.min(100, (v.ops / maxOps) * 100)}%`, backgroundColor: v.color }}
              />
            </div>
            <span className="w-20 shrink-0 text-right font-mono text-xs text-neutral-500">{v.ops.toLocaleString()}</span>
          </div>
        ))}
      </div>
      <StepNote>{step.note}</StepNote>
      <StepControls state={state} total={steps.length} />
    </div>
  );
}
