"use client";

import { StepControls, StepNote, useSteps } from "./shared";

export interface QueueStep {
  queue: (string | number)[];
  note: string;
  action?: "enqueue" | "dequeue" | "none";
}

export function QueueViz({ steps, frontLabel = "front", backLabel = "back" }: { steps: QueueStep[]; frontLabel?: string; backLabel?: string }) {
  const state = useSteps(steps.length);
  const step = steps[state.index];

  return (
    <div className="flex flex-col gap-3">
      <div className="flex min-h-[64px] items-center justify-center gap-1.5 rounded-xl bg-neutral-50 p-3">
        {frontLabel && <span className="mr-1 text-xs font-medium text-neutral-400">{frontLabel}</span>}
        {step.queue.length === 0 && <p className="text-sm text-neutral-400">empty</p>}
        {step.queue.map((val, i) => (
          <div
            key={i}
            className={`flex h-10 w-10 items-center justify-center rounded-lg border-2 font-mono text-sm font-medium transition-colors ${
              i === 0 && step.action !== "none" ? "border-amber-400 bg-amber-100 text-amber-800" : "border-sky-300 bg-white text-sky-700"
            }`}
          >
            {val}
          </div>
        ))}
        {backLabel && <span className="ml-1 text-xs font-medium text-neutral-400">{backLabel}</span>}
      </div>
      <StepNote>{step.note}</StepNote>
      <StepControls state={state} total={steps.length} />
    </div>
  );
}
