"use client";

import { StepControls, StepNote, useSteps } from "./shared";

export interface HashMapStep {
  entries: { key: string | number; value: string | number }[];
  note: string;
  highlightKey?: string | number;
}

export function HashMapViz({ steps }: { steps: HashMapStep[] }) {
  const state = useSteps(steps.length);
  const step = steps[state.index];

  return (
    <div className="flex flex-col gap-3">
      <div className="flex min-h-[80px] flex-wrap items-center justify-center gap-2 rounded-xl bg-neutral-50 p-3">
        {step.entries.length === 0 && <p className="text-sm text-neutral-400">empty map</p>}
        {step.entries.map((e, i) => {
          const hl = step.highlightKey !== undefined && e.key === step.highlightKey;
          return (
            <div
              key={i}
              className={`flex flex-col items-center rounded-xl border-2 px-3 py-1.5 transition-colors ${
                hl ? "border-amber-400 bg-amber-100" : "border-sky-300 bg-white"
              }`}
            >
              <span className="font-mono text-sm font-bold text-neutral-800">{e.key}</span>
              <span className="my-0.5 text-neutral-300">↓</span>
              <span className="font-mono text-sm font-semibold text-sky-700">{e.value}</span>
            </div>
          );
        })}
      </div>
      <StepNote>{step.note}</StepNote>
      <StepControls state={state} total={steps.length} />
    </div>
  );
}
