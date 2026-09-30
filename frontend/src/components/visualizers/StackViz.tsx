"use client";

import { StepControls, StepNote, useSteps } from "./shared";

export interface StackStep {
  stack: (string | number)[];
  note: string;
  action?: "push" | "pop" | "none";
}

export function StackViz({ steps }: { steps: StackStep[] }) {
  const state = useSteps(steps.length);
  const step = steps[state.index];

  return (
    <div className="flex flex-col gap-3">
      <div className="flex min-h-[180px] flex-col-reverse items-center justify-start gap-1.5 rounded-xl bg-neutral-50 p-3">
        {step.stack.length === 0 && <p className="mb-auto pt-16 text-sm text-neutral-400">empty stack</p>}
        {step.stack.map((val, i) => {
          const isTop = i === step.stack.length - 1;
          return (
            <div
              key={i}
              className={`flex h-9 w-24 items-center justify-center rounded-lg border-2 font-mono text-sm font-medium transition-colors ${
                isTop && step.action !== "none" ? "border-amber-400 bg-amber-100 text-amber-800" : "border-neutral-300 bg-white text-neutral-700"
              }`}
            >
              {val}
            </div>
          );
        })}
      </div>
      <p className="text-center text-xs text-neutral-400">top of stack is highest in the diagram</p>
      <StepNote>{step.note}</StepNote>
      <StepControls state={state} total={steps.length} />
    </div>
  );
}
