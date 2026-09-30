"use client";

import { ArrowRight, Compass } from "lucide-react";

export interface ConceptMapItem {
  key: string;
  label: string;
}

/** A small orientation strip shown before a lesson's content: where this
 * concept sits relative to what comes before it and what it leads to, using
 * whatever real relationship data the caller has (an authored prerequisite
 * graph for DSA skills, or level/category adjacency for system design
 * lessons) -- never a fabricated dependency. Renders nothing if there's
 * genuinely no before/after relationship to show. */
export function ConceptMapStrip({ before, currentLabel, after, onNavigate }: {
  before: ConceptMapItem[]; currentLabel: string; after: ConceptMapItem[]; onNavigate?: (key: string) => void;
}) {
  if (before.length === 0 && after.length === 0) return null;

  return (
    <div className="mb-4 flex flex-wrap items-center gap-1.5 rounded-xl bg-sky-50 px-3 py-2.5 text-xs ring-1 ring-sky-100">
      <Compass size={13} className="mr-1 shrink-0 text-sky-500" />
      {before.map((item, i) => (
        <span key={item.key} className="flex items-center gap-1.5">
          <button
            onClick={() => onNavigate?.(item.key)}
            disabled={!onNavigate}
            className="rounded-full bg-white px-2.5 py-1 font-medium text-neutral-600 ring-1 ring-neutral-200 transition-colors hover:ring-sky-300 disabled:cursor-default"
          >
            {item.label}
          </button>
          {i === before.length - 1 && <ArrowRight size={12} className="text-neutral-400" />}
        </span>
      ))}

      <span className="rounded-full bg-sky-600 px-2.5 py-1 font-semibold text-white">{currentLabel}</span>

      {after.map((item, i) => (
        <span key={item.key} className="flex items-center gap-1.5">
          {i === 0 && <ArrowRight size={12} className="text-neutral-400" />}
          <button
            onClick={() => onNavigate?.(item.key)}
            disabled={!onNavigate}
            className="rounded-full bg-white px-2.5 py-1 font-medium text-neutral-600 ring-1 ring-neutral-200 transition-colors hover:ring-sky-300 disabled:cursor-default"
          >
            {item.label}
          </button>
        </span>
      ))}
    </div>
  );
}
