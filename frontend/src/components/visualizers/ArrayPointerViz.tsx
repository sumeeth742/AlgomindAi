"use client";

import { StepControls, StepNote, useSteps } from "./shared";

export interface ArrayStep {
  pointers: Record<string, number>;
  highlight?: number[];
  note: string;
  runningValue?: string;
  eliminated?: [number, number]; // [fromIndex, toIndex] inclusive range greyed out (binary search)
}

const POINTER_COLORS: Record<string, string> = {
  L: "text-sky-600", left: "text-sky-600", lo: "text-sky-600",
  R: "text-rose-600", right: "text-rose-600", hi: "text-rose-600",
  i: "text-emerald-600", mid: "text-violet-600", window: "text-amber-600",
};
const POINTER_DOTS: Record<string, string> = {
  L: "bg-sky-500", left: "bg-sky-500", lo: "bg-sky-500",
  R: "bg-rose-500", right: "bg-rose-500", hi: "bg-rose-500",
  i: "bg-emerald-500", mid: "bg-violet-500", window: "bg-amber-500",
};

export function ArrayPointerViz({ array, steps, valueLabel }: { array: (number | string)[]; steps: ArrayStep[]; valueLabel?: string }) {
  const state = useSteps(steps.length);
  const step = steps[state.index];
  const highlight = new Set(step.highlight ?? []);
  const pointersByIndex = new Map<number, string[]>();
  for (const [name, idx] of Object.entries(step.pointers)) {
    if (!pointersByIndex.has(idx)) pointersByIndex.set(idx, []);
    pointersByIndex.get(idx)!.push(name);
  }
  const activePointerNames = Object.keys(step.pointers);

  return (
    <div className="flex flex-col gap-3">
      {activePointerNames.length > 0 && (
        <div className="flex flex-wrap justify-center gap-3">
          {activePointerNames.map((name) => (
            <span key={name} className="flex items-center gap-1 text-xs font-semibold text-neutral-500">
              <span className={`h-2 w-2 rounded-full ${POINTER_DOTS[name] ?? "bg-neutral-400"}`} />
              {name}
            </span>
          ))}
        </div>
      )}
      <div className="flex flex-wrap items-end justify-center gap-2 overflow-x-auto py-2">
        {array.map((val, i) => {
          const isEliminated = step.eliminated && i >= step.eliminated[0] && i <= step.eliminated[1];
          const isHighlighted = highlight.has(i);
          return (
            <div key={i} className="flex flex-col items-center gap-1">
              <div className="flex h-5 flex-col items-center justify-end gap-0.5">
                {(pointersByIndex.get(i) ?? []).map((name) => (
                  <span key={name} className={`text-[11px] font-bold leading-none ${POINTER_COLORS[name] ?? "text-neutral-500"}`}>
                    {name}
                  </span>
                ))}
              </div>
              <div
                className={`flex h-11 w-11 items-center justify-center rounded-xl border-2 font-mono text-sm font-bold transition-all ${
                  isEliminated ? "border-neutral-100 bg-neutral-50 text-neutral-300"
                  : isHighlighted ? "border-emerald-500 bg-gradient-to-br from-emerald-400 to-teal-400 text-white shadow-md shadow-emerald-500/30"
                  : "border-neutral-200 bg-white text-neutral-700"
                }`}
              >
                {val}
              </div>
              <span className="font-mono text-[10px] text-neutral-300">{i}</span>
            </div>
          );
        })}
      </div>
      {step.runningValue !== undefined && (
        <p className="flex items-center justify-center gap-2 text-sm text-neutral-600">
          {valueLabel ?? "value"}:
          <span className="rounded-full bg-emerald-100 px-3 py-0.5 font-mono font-bold text-emerald-800">{step.runningValue}</span>
        </p>
      )}
      <StepNote>{step.note}</StepNote>
      <StepControls state={state} total={steps.length} />
    </div>
  );
}
