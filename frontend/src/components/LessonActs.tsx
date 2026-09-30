"use client";

import { useMemo, useState } from "react";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { Markdown } from "@/components/Markdown";

interface Act {
  title: string;
  body: string;
}

/** Splits a lesson's markdown on its "## " headings and groups them into up
 * to `numActs` roughly-even chunks -- adapts to however many sections a given
 * lesson actually has, rather than assuming a fixed template. The leading H1
 * (and any text before the first "## ") stays attached to Act 1. */
function splitIntoActs(markdown: string, numActs = 4): Act[] {
  const parts = markdown.split(/\n(?=## )/);
  const intro = parts[0] ?? "";
  const sections = parts.slice(1);
  if (sections.length === 0) return [{ title: "", body: markdown }];

  const perAct = Math.max(1, Math.ceil(sections.length / numActs));
  const acts: Act[] = [];
  for (let i = 0; i < sections.length; i += perAct) {
    const chunk = sections.slice(i, i + perAct);
    const firstHeading = chunk[0].split("\n")[0].replace(/^##\s*/, "").trim();
    acts.push({ title: firstHeading, body: chunk.join("\n") });
  }
  acts[0] = { ...acts[0], body: `${intro}\n${acts[0].body}` };
  return acts;
}

/** Presents a lesson one "act" (chunk of sections) at a time instead of one
 * long continuous scroll, with a brief optional reflection prompt between
 * acts -- a structural fix for information overload, not just a formatting
 * one. Callers should pass a `key` (e.g. the lesson slug) so React remounts
 * a fresh instance -- back at Act 1 -- whenever a different lesson opens,
 * rather than resetting state via an effect. */
export function LessonActs({ markdown, size = "base" }: { markdown: string; size?: "base" | "lg" }) {
  const acts = useMemo(() => splitIntoActs(markdown), [markdown]);
  const [current, setCurrent] = useState(0);
  const [reflection, setReflection] = useState("");

  const act = acts[current];
  const isLast = current === acts.length - 1;

  return (
    <div>
      {acts.length > 1 && (
        <>
          <div className="mb-3 flex items-center gap-1.5">
            {acts.map((_, i) => (
              <div key={i} className={`h-1.5 flex-1 rounded-full transition-colors ${i <= current ? "bg-emerald-500" : "bg-neutral-200"}`} />
            ))}
          </div>
          <p className="mb-2 text-xs font-bold uppercase tracking-wide text-neutral-400">
            Act {current + 1} of {acts.length}{act.title ? ` -- ${act.title}` : ""}
          </p>
        </>
      )}

      <Markdown size={size}>{act.body}</Markdown>

      {acts.length > 1 && (
        <>
          {!isLast && (
            <div className="mt-6 rounded-xl border border-dashed border-neutral-300 p-3">
              <label className="text-xs font-medium text-neutral-500">
                Before continuing (optional) -- what&apos;s the core idea so far, in your own words?
              </label>
              <textarea
                value={reflection}
                onChange={(e) => setReflection(e.target.value)}
                rows={2}
                placeholder="Jot a quick sentence, or skip this."
                className="mt-1 w-full rounded-lg border border-neutral-300 px-2 py-1.5 text-sm outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100"
              />
            </div>
          )}

          <div className="mt-4 flex items-center justify-between">
            <button
              onClick={() => setCurrent((c) => Math.max(0, c - 1))}
              disabled={current === 0}
              className="flex items-center gap-1 text-sm font-medium text-neutral-500 hover:text-neutral-800 disabled:opacity-30"
            >
              <ChevronLeft size={15} /> Back
            </button>
            {!isLast ? (
              <button
                onClick={() => {
                  setCurrent((c) => c + 1);
                  setReflection("");
                }}
                className="flex items-center gap-1 rounded-lg bg-emerald-600 px-4 py-2 text-sm font-medium text-white hover:bg-emerald-700"
              >
                Continue to Act {current + 2} <ChevronRight size={15} />
              </button>
            ) : (
              <span className="text-sm font-medium text-emerald-700">You&apos;ve reached the end -- see the key takeaway above.</span>
            )}
          </div>
        </>
      )}
    </div>
  );
}
