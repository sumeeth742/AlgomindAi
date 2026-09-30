"use client";

import { StepControls, StepNote, useSteps } from "./shared";

export interface TreeNode {
  id: string;
  val: number | string;
  left: string | null;
  right: string | null;
}

export interface TreeStep {
  visited: string[];
  current: string | null;
  note: string;
}

export function TreeViz({ nodes, rootId, steps }: { nodes: TreeNode[]; rootId: string; steps: TreeStep[] }) {
  const state = useSteps(steps.length);
  const step = steps[state.index];
  const nodeMap = new Map(nodes.map((n) => [n.id, n]));

  const positions = new Map<string, { x: number; y: number }>();
  let counter = 0;
  let maxY = 0;
  function layout(id: string | null, depth: number) {
    if (!id) return;
    const node = nodeMap.get(id);
    if (!node) return;
    layout(node.left, depth + 1);
    positions.set(id, { x: counter++, y: depth });
    maxY = Math.max(maxY, depth);
    layout(node.right, depth + 1);
  }
  layout(rootId, 0);

  const maxX = Math.max(1, counter - 1);
  const width = Math.max(280, (maxX + 1) * 64);
  const height = (maxY + 1) * 72 + 40;
  const px = (x: number) => (counter <= 1 ? width / 2 : (x / maxX) * (width - 60) + 30);
  const py = (y: number) => y * 72 + 30;

  return (
    <div className="flex flex-col gap-3">
      <svg width="100%" viewBox={`0 0 ${width} ${height}`} className="mx-auto max-w-full">
        {nodes.map((node) => {
          const pos = positions.get(node.id);
          if (!pos) return null;
          return [node.left, node.right].map((childId) => {
            if (!childId) return null;
            const cpos = positions.get(childId);
            if (!cpos) return null;
            return (
              <line
                key={node.id + childId} x1={px(pos.x)} y1={py(pos.y)} x2={px(cpos.x)} y2={py(cpos.y)}
                stroke="#d4d4d4" strokeWidth={2}
              />
            );
          });
        })}
        {nodes.map((node) => {
          const pos = positions.get(node.id);
          if (!pos) return null;
          const visited = step.visited.includes(node.id);
          const isCurrent = step.current === node.id;
          return (
            <g key={node.id}>
              <circle
                cx={px(pos.x)} cy={py(pos.y)} r={18}
                fill={isCurrent ? "#fbbf24" : visited ? "#6ee7b7" : "#ffffff"}
                stroke={isCurrent ? "#d97706" : visited ? "#059669" : "#d4d4d4"} strokeWidth={2}
              />
              <text x={px(pos.x)} y={py(pos.y) + 5} textAnchor="middle" fontSize={13} fontFamily="monospace" fill="#374151">
                {node.val}
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
