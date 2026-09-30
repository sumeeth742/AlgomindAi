"use client";

import { StepControls, StepNote, useSteps } from "./shared";

export interface LinkedListNode {
  id: string;
  val: number | string;
  next: string | null; // node id, or null for terminal
}

export interface LinkedListStep {
  nodes: LinkedListNode[];
  pointers: Record<string, string | null>; // pointer name -> node id (or null)
  note: string;
}

const POINTER_COLORS: Record<string, string> = {
  prev: "text-neutral-500", curr: "text-emerald-600", next: "text-sky-600", head: "text-violet-600",
};

export function LinkedListViz({ steps }: { steps: LinkedListStep[] }) {
  const state = useSteps(steps.length);
  const step = steps[state.index];
  const pointersByNode = new Map<string, string[]>();
  for (const [name, id] of Object.entries(step.pointers)) {
    if (id === null) continue;
    if (!pointersByNode.has(id)) pointersByNode.set(id, []);
    pointersByNode.get(id)!.push(name);
  }
  const nullPointers = Object.entries(step.pointers).filter(([, id]) => id === null).map(([name]) => name);

  return (
    <div className="flex flex-col gap-3">
      <div className="flex flex-wrap items-center justify-center gap-1 overflow-x-auto py-3">
        {step.nodes.map((node, i) => (
          <div key={node.id} className="flex items-center gap-1">
            <div className="flex flex-col items-center gap-1">
              <div className="flex h-4 gap-1">
                {(pointersByNode.get(node.id) ?? []).map((name) => (
                  <span key={name} className={`text-[10px] font-bold leading-none ${POINTER_COLORS[name] ?? "text-neutral-500"}`}>{name}</span>
                ))}
              </div>
              <div className="flex h-10 w-10 items-center justify-center rounded-full border-2 border-emerald-400 bg-emerald-50 font-mono text-sm font-medium text-emerald-800">
                {node.val}
              </div>
            </div>
            {i < step.nodes.length - 1 && (
              <span className={`font-mono text-lg ${node.next === step.nodes[i + 1]?.id ? "text-neutral-400" : "text-rose-400"}`}>
                {node.next === step.nodes[i + 1]?.id ? "→" : "×"}
              </span>
            )}
          </div>
        ))}
        <span className="font-mono text-sm text-neutral-300">→ null</span>
      </div>
      {nullPointers.length > 0 && (
        <p className="text-center text-xs text-neutral-400">
          {nullPointers.map((n) => <span key={n} className={`mx-1 font-bold ${POINTER_COLORS[n] ?? ""}`}>{n} = null</span>)}
        </p>
      )}
      <StepNote>{step.note}</StepNote>
      <StepControls state={state} total={steps.length} />
    </div>
  );
}
