"use client";

import { StepControls, StepNote, useSteps } from "./shared";
import { TraceStepOut } from "@/lib/types";

function formatValue(v: unknown): string {
  if (v === null || v === undefined) return "null";
  if (typeof v === "object" && v !== null && "__type__" in (v as Record<string, unknown>)) {
    const obj = v as { __type__: string; values: unknown[] };
    return `${obj.__type__ === "linked_list" ? "list" : "tree"}(${JSON.stringify(obj.values)})`;
  }
  return JSON.stringify(v);
}

export function OwnCodeTrace({
  sourceLines, steps, result, status, errorMessage, truncated,
}: {
  sourceLines: string[];
  steps: TraceStepOut[];
  result: unknown;
  status: string | null;
  errorMessage: string | null;
  truncated: boolean;
}) {
  const state = useSteps(Math.max(steps.length, 1));
  if (steps.length === 0) {
    return <p className="text-sm text-neutral-500">No steps were recorded before this ran.</p>;
  }
  const step = steps[state.index];
  const varNames = Object.keys(step.locals);

  return (
    <div className="flex flex-col gap-3">
      <div className="overflow-hidden rounded-lg bg-neutral-900 font-mono text-xs">
        {sourceLines.map((line, i) => {
          const lineNo = i + 1;
          const isCurrent = lineNo === step.line;
          return (
            <div
              key={i}
              className={`flex gap-3 px-3 py-0.5 ${isCurrent ? "bg-emerald-500/20 border-l-2 border-emerald-400" : "border-l-2 border-transparent"}`}
            >
              <span className="w-5 shrink-0 text-right text-neutral-500">{lineNo}</span>
              <span className={isCurrent ? "text-emerald-300" : "text-neutral-300"}>
                {line || " "}
              </span>
            </div>
          );
        })}
      </div>

      <StepControls state={state} total={steps.length} />
      <StepNote>
        {`${step.depth > 1 ? `Recursion depth ${step.depth} -- ` : ""}About to run line ${step.line}`}
      </StepNote>

      <div className="rounded-lg bg-neutral-50 p-3">
        <p className="mb-1.5 text-xs font-semibold uppercase tracking-wide text-neutral-500">Variables at this step</p>
        {varNames.length === 0 ? (
          <p className="text-xs text-neutral-400">(none yet)</p>
        ) : (
          <div className="flex flex-col gap-1 font-mono text-xs">
            {varNames.map((name) => (
              <div key={name} className="flex gap-2">
                <span className="text-indigo-600">{name} =</span>
                <span className="text-neutral-800">{formatValue(step.locals[name])}</span>
              </div>
            ))}
          </div>
        )}
      </div>

      {state.isLast && (
        <div className="rounded-lg bg-white p-2 text-xs ring-1 ring-neutral-200">
          {status === "ok" ? (
            <span className="text-neutral-700">Finished -- returned <span className="font-mono">{formatValue(result)}</span></span>
          ) : (
            <span className="text-red-600">Crashed here: {errorMessage}</span>
          )}
        </div>
      )}
      {truncated && (
        <p className="text-xs text-neutral-400">Trace stopped after 500 steps (this run kept going, e.g. a long loop) -- shown up to that point.</p>
      )}
    </div>
  );
}
