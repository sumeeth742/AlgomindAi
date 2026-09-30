"use client";

import { useEffect, useState } from "react";
import { Volume2, VolumeX } from "lucide-react";
import { StepControls, StepNote, useSteps } from "./shared";

export interface FlowNode {
  id: string;
  label: string;
  sublabel?: string;
  col: number; // grid column, 0-indexed
  row: number; // grid row, 0-indexed
  color?: string; // hex fill, defaults to neutral
}

export interface FlowEdge {
  from: string;
  to: string;
  label?: string;
  dashed?: boolean;
}

export interface FlowStep {
  activeNodes?: string[]; // ids to highlight; omit to highlight all
  activeEdges?: number[]; // indices into the edges array to highlight; omit for none
  note: string;
}

const COL_W = 110;
const ROW_H = 90;
const BOX_W = 92;
const BOX_H = 48;

export function FlowDiagram({ nodes, edges, steps }: { nodes: FlowNode[]; edges: FlowEdge[]; steps: FlowStep[] }) {
  const state = useSteps(steps.length);
  // `state.index` can briefly point past the end of a shorter `steps` array
  // (e.g. switching lessons re-renders this same component with fewer steps,
  // before useSteps' own clamping effect has run) -- clamp right here too, at
  // the point of use, so this never reads an out-of-bounds `undefined` step.
  const step = steps[Math.min(state.index, steps.length - 1)];
  const [narrate, setNarrate] = useState(false);
  // Checked only after mount (never at module scope) so server-rendered and
  // first-client-render markup always agree -- speechSynthesis is a
  // browser-only API and doesn't exist during SSR.
  const [speechSupported, setSpeechSupported] = useState(false);
  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect -- one-time browser-API detection, can't run during SSR
    setSpeechSupported(typeof window !== "undefined" && "speechSynthesis" in window);
  }, []);

  // Reads the real per-step "note" text aloud as you step or auto-play through
  // the diagram -- the browser's own local speech synthesis, no API key, no
  // recorded audio -- turning the existing step-through diagram into something
  // that plays like a narrated walkthrough instead of requiring silent reading.
  useEffect(() => {
    if (!narrate || !speechSupported) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(step.note);
    utterance.rate = 1.0;
    window.speechSynthesis.speak(utterance);
    return () => window.speechSynthesis.cancel();
  }, [narrate, speechSupported, step.note]);

  useEffect(() => {
    if (!speechSupported) return;
    return () => window.speechSynthesis.cancel();
  }, [speechSupported]);
  const maxCol = Math.max(...nodes.map((n) => n.col));
  const maxRow = Math.max(...nodes.map((n) => n.row));
  const width = (maxCol + 1) * COL_W + 40;
  const height = (maxRow + 1) * ROW_H + 30;

  const center = (n: FlowNode) => ({ x: n.col * COL_W + BOX_W / 2 + 20, y: n.row * ROW_H + BOX_H / 2 + 15 });
  const nodeMap = new Map(nodes.map((n) => [n.id, n]));
  const activeNodes = new Set(step.activeNodes ?? nodes.map((n) => n.id));
  const activeEdges = new Set(step.activeEdges ?? []);
  const highlightingEdges = step.activeEdges !== undefined;

  return (
    <div className="flex flex-col gap-3">
      <svg viewBox={`0 0 ${width} ${height}`} className="mx-auto w-full max-w-md">
        <defs>
          <marker id="flow-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
            <path d="M0,0 L8,4 L0,8 z" fill="#a3a3a3" />
          </marker>
          <marker id="flow-arrow-active" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
            <path d="M0,0 L8,4 L0,8 z" fill="#059669" />
          </marker>
        </defs>
        {edges.map((e, i) => {
          const a = nodeMap.get(e.from);
          const b = nodeMap.get(e.to);
          if (!a || !b) return null;
          const pa = center(a);
          const pb = center(b);
          const isActive = highlightingEdges && activeEdges.has(i);
          return (
            <g key={i}>
              <line
                x1={pa.x} y1={pa.y} x2={pb.x} y2={pb.y}
                stroke={isActive ? "#059669" : "#d4d4d4"} strokeWidth={isActive ? 2.5 : 2}
                strokeDasharray={e.dashed ? "4 3" : undefined}
                markerEnd={`url(#flow-arrow${isActive ? "-active" : ""})`}
              />
              {e.label && isActive && (
                <text x={(pa.x + pb.x) / 2} y={(pa.y + pb.y) / 2 - 6} fontSize={9} fontWeight="bold" fill="#047857" textAnchor="middle">
                  {e.label}
                </text>
              )}
            </g>
          );
        })}
        {nodes.map((n) => {
          const p = center(n);
          const isActive = activeNodes.has(n.id);
          const fill = isActive ? (n.color ?? "#059669") : "#e5e5e5";
          return (
            <g key={n.id} opacity={isActive ? 1 : 0.55}>
              <rect x={p.x - BOX_W / 2} y={p.y - BOX_H / 2} width={BOX_W} height={BOX_H} rx={10} fill={fill} />
              <text x={p.x} y={p.y - (n.sublabel ? 3 : -4)} textAnchor="middle" fontSize={11} fontWeight="bold" fill="#ffffff">
                {n.label}
              </text>
              {n.sublabel && (
                <text x={p.x} y={p.y + 12} textAnchor="middle" fontSize={9} fill="#ffffff" opacity={0.85}>
                  {n.sublabel}
                </text>
              )}
            </g>
          );
        })}
      </svg>
      <StepNote>{step.note}</StepNote>
      <div className="flex items-center justify-center gap-2">
        {steps.length > 1 && <StepControls state={state} total={steps.length} />}
        {speechSupported && (
          <button
            onClick={() => setNarrate((n) => !n)}
            className={`flex h-8 w-8 items-center justify-center rounded-full border ${
              narrate ? "border-emerald-300 bg-emerald-50 text-emerald-700" : "border-neutral-200 text-neutral-500 hover:bg-neutral-50"
            }`}
            aria-label={narrate ? "Mute narration" : "Narrate this step aloud"}
            title={narrate ? "Mute narration" : "Narrate this step aloud"}
            type="button"
          >
            {narrate ? <Volume2 size={14} /> : <VolumeX size={14} />}
          </button>
        )}
      </div>
    </div>
  );
}
