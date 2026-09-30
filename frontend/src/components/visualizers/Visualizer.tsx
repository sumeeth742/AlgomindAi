"use client";

import { VisualizationConfig } from "@/lib/visualizations";
import { ArrayPointerViz } from "./ArrayPointerViz";
import { StackViz } from "./StackViz";
import { LinkedListViz } from "./LinkedListViz";
import { TreeViz } from "./TreeViz";
import { GraphViz } from "./GraphViz";
import { GridViz } from "./GridViz";
import { HashMapViz } from "./HashMapViz";
import { BitViz } from "./BitViz";
import { QueueViz } from "./QueueViz";
import { GrowthChartViz } from "./GrowthChartViz";

export function Visualizer({ config }: { config: VisualizationConfig }) {
  switch (config.type) {
    case "array":
      return <ArrayPointerViz array={config.array} steps={config.steps} valueLabel={config.valueLabel} />;
    case "stack":
      return <StackViz steps={config.steps} />;
    case "linkedlist":
      return <LinkedListViz steps={config.steps} />;
    case "tree":
      return <TreeViz nodes={config.nodes} rootId={config.rootId} steps={config.steps} />;
    case "graph":
      return <GraphViz nodes={config.nodes} edges={config.edges} steps={config.steps} />;
    case "grid":
      return <GridViz rowLabels={config.rowLabels} colLabels={config.colLabels} steps={config.steps} />;
    case "hashmap":
      return <HashMapViz steps={config.steps} />;
    case "bits":
      return <BitViz steps={config.steps} />;
    case "queue":
      return <QueueViz steps={config.steps} frontLabel={config.frontLabel} backLabel={config.backLabel} />;
    case "growth":
      return <GrowthChartViz steps={config.steps} />;
  }
}
