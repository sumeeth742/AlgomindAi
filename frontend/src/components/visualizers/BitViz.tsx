"use client";

import { StepControls, StepNote, useSteps } from "./shared";

export interface BitStep {
  bits: (0 | 1)[];
  note: string;
  highlight?: number[];
  decimal?: number;
}

export function BitViz({ steps }: { steps: BitStep[] }) {
  const state = useSteps(steps.length);
  const step = steps[state.index];
  const hl = new Set(step.highlight ?? []);

  return (
    <div className="flex flex-col gap-3">
      <div className="flex justify-center gap-1.5">
        {step.bits.map((b, i) => (
          <div
            key={i}
            className={`flex h-11 w-9 items-center justify-center rounded-lg border-2 font-mono text-base font-bold transition-colors ${
              hl.has(i) ? "border-amber-400 bg-amber-100 text-amber-800"
              : b === 1 ? "border-emerald-400 bg-emerald-100 text-emerald-800"
              : "border-neutral-200 bg-white text-neutral-400"
            }`}
          >
            {b}
          </div>
        ))}
      </div>
      {step.decimal !== undefined && (
        <p className="text-center text-sm text-neutral-600">
          = <span className="font-mono font-semibold text-emerald-700">{step.decimal}</span> in decimal
        </p>
      )}
      <StepNote>{step.note}</StepNote>
      <StepControls state={state} total={steps.length} />
    </div>
  );
}
