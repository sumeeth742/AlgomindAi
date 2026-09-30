"use client";

import { StepControls, StepNote, useSteps } from "./shared";

export interface GraphNode {
  id: string;
  label: string | number;
}

export interface GraphEdge {
  from: string;
  to: string;
  weight?: number;
  directed?: boolean;
}

export interface GraphStep {
  visited?: string[];
  current?: string | null;
  frontier?: string[];
  distances?: Record<string, number | string>;
  groups?: Record<string, number>; // union-find style component coloring
  note: string;
}

const GROUP_COLORS = ["#059669", "#0284c7", "#d97706", "#9333ea", "#e11d48", "#0d9488"];

function layoutCircular(ids: string[], width: number, height: number) {
  const cx = width / 2;
  const cy = height / 2;
  const r = Math.min(width, height) / 2 - 34;
  const pos: Record<string, { x: number; y: number }> = {};
  ids.forEach((id, i) => {
    const angle = (2 * Math.PI * i) / ids.length - Math.PI / 2;
    pos[id] = { x: cx + r * Math.cos(angle), y: cy + r * Math.sin(angle) };
  });
  return pos;
}

export function GraphViz({ nodes, edges, steps }: { nodes: GraphNode[]; edges: GraphEdge[]; steps: GraphStep[] }) {
  const state = useSteps(steps.length);
  const step = steps[state.index];
  const width = 300;
  const height = 220;
  const pos = layoutCircular(nodes.map((n) => n.id), width, height);
  const visited = new Set(step.visited ?? []);
  const frontier = new Set(step.frontier ?? []);

  return (
    <div className="flex flex-col gap-3">
      <svg viewBox={`0 0 ${width} ${height}`} className="mx-auto w-full max-w-xs">
        <defs>
          <marker id="viz-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
            <path d="M0,0 L8,4 L0,8 z" fill="#a3a3a3" />
          </marker>
        </defs>
        {edges.map((e, i) => {
          const a = pos[e.from];
          const b = pos[e.to];
          if (!a || !b) return null;
          return (
            <g key={i}>
              <line x1={a.x} y1={a.y} x2={b.x} y2={b.y} stroke="#d4d4d4" strokeWidth={2} markerEnd={e.directed ? "url(#viz-arrow)" : undefined} />
              {e.weight !== undefined && (
                <text x={(a.x + b.x) / 2} y={(a.y + b.y) / 2 - 4} fontSize={10} fill="#737373" textAnchor="middle">
                  {e.weight}
                </text>
              )}
            </g>
          );
        })}
        {nodes.map((n) => {
          const p = pos[n.id];
          if (!p) return null;
          const isCurrent = step.current === n.id;
          const isVisited = visited.has(n.id);
          const isFrontier = frontier.has(n.id);
          const groupColor = step.groups?.[n.id] !== undefined ? GROUP_COLORS[step.groups[n.id] % GROUP_COLORS.length] : undefined;
          const fill = isCurrent ? "#fbbf24" : groupColor ?? (isVisited ? "#6ee7b7" : isFrontier ? "#bae6fd" : "#ffffff");
          const stroke = isCurrent ? "#d97706" : groupColor ?? (isVisited ? "#059669" : "#d4d4d4");
          const dist = step.distances?.[n.id];
          return (
            <g key={n.id}>
              {dist !== undefined && (
                <text x={p.x} y={p.y - 22} textAnchor="middle" fontSize={10} fontWeight="bold" fill="#059669">
                  {dist}
                </text>
              )}
              <circle cx={p.x} cy={p.y} r={16} fill={fill} stroke={stroke} strokeWidth={2} />
              <text x={p.x} y={p.y + 4} textAnchor="middle" fontSize={12} fontFamily="monospace" fill="#374151">
                {n.label}
              </text>
            </g>
          );
        })}
      </svg>
      <StepNote>{step.note}</StepNote>
      <StepControls state={state} total={steps.length} />
    </div>
  );
}
