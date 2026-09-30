"use client";

import { StepControls, StepNote, useSteps } from "./shared";

export interface GridStep {
  grid: (number | string | null)[][];
  current?: [number, number];
  note: string;
}

export function GridViz({ rowLabels, colLabels, steps }: { rowLabels: string[]; colLabels: string[]; steps: GridStep[] }) {
  const state = useSteps(steps.length);
  const step = steps[state.index];

  return (
    <div className="flex flex-col gap-3">
      <div className="overflow-x-auto">
        <table className="mx-auto border-separate [border-spacing:2px] text-xs">
          <thead>
            <tr>
              <th className="w-8" />
              {colLabels.map((c, j) => (
                <th key={j} className="w-8 pb-1 font-mono font-normal text-neutral-400">{c}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rowLabels.map((r, i) => (
              <tr key={i}>
                <th className="pr-1 font-mono font-normal text-neutral-400">{r}</th>
                {step.grid[i]?.map((val, j) => {
                  const isCurrent = step.current?.[0] === i && step.current?.[1] === j;
                  return (
                    <td
                      key={j}
                      className={`h-8 w-8 rounded-md text-center font-mono transition-colors ${
                        isCurrent ? "bg-amber-300 font-bold text-amber-900"
                        : val !== null ? "bg-emerald-100 text-emerald-800"
                        : "bg-neutral-100 text-neutral-300"
                      }`}
                    >
                      {val ?? "·"}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <StepNote>{step.note}</StepNote>
      <StepControls state={state} total={steps.length} />
    </div>
  );
}
