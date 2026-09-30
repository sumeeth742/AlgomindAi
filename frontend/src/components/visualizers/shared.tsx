"use client";

import { useEffect, useState } from "react";
import { Pause, Play, RotateCcw, SkipBack, SkipForward } from "lucide-react";

export function useSteps(totalSteps: number, autoPlayMs = 1100) {
  const [index, setIndex] = useState(0);
  const [playing, setPlaying] = useState(false);

  // Guards against a real crash: when a caller re-renders this same component
  // instance with a shorter `steps` array (e.g. switching between two lesson
  // diagrams without a `key` forcing a remount), the previous `index` can be
  // left pointing past the end of the new array, and `steps[index]` would be
  // undefined everywhere it's read. Clamp back into range instead.
  useEffect(() => {
    if (index > totalSteps - 1) {
      // eslint-disable-next-line react-hooks/set-state-in-effect -- necessary reactive clamp, not derivable at render time without this
      setIndex(Math.max(0, totalSteps - 1));
    }
  }, [totalSteps, index]);

  useEffect(() => {
    if (!playing) return;
    if (index >= totalSteps - 1) {
      // eslint-disable-next-line react-hooks/set-state-in-effect
      setPlaying(false);
      return;
    }
    const t = setTimeout(() => setIndex((i) => Math.min(i + 1, totalSteps - 1)), autoPlayMs);
    return () => clearTimeout(t);
  }, [playing, index, totalSteps, autoPlayMs]);

  return {
    index,
    playing,
    setPlaying,
    next: () => setIndex((i) => Math.min(i + 1, totalSteps - 1)),
    prev: () => setIndex((i) => Math.max(i - 1, 0)),
    reset: () => {
      setIndex(0);
      setPlaying(false);
    },
    isFirst: index === 0,
    isLast: index === totalSteps - 1,
  };
}

type StepState = ReturnType<typeof useSteps>;

export function StepControls({ state, total }: { state: StepState; total: number }) {
  const btn = "flex h-8 w-8 items-center justify-center rounded-full border border-neutral-200 text-neutral-600 hover:bg-neutral-50 disabled:opacity-30 disabled:hover:bg-transparent";
  return (
    <div className="flex items-center justify-center gap-2">
      <button onClick={state.reset} className={btn} aria-label="Reset" type="button">
        <RotateCcw size={14} />
      </button>
      <button onClick={state.prev} disabled={state.isFirst} className={btn} aria-label="Previous step" type="button">
        <SkipBack size={14} />
      </button>
      <button
        onClick={() => state.setPlaying((p) => !p)}
        className="flex h-9 w-9 items-center justify-center rounded-full bg-emerald-600 text-white hover:bg-emerald-700"
        aria-label={state.playing ? "Pause" : "Play"} type="button"
      >
        {state.playing ? <Pause size={15} /> : <Play size={15} />}
      </button>
      <button onClick={state.next} disabled={state.isLast} className={btn} aria-label="Next step" type="button">
        <SkipForward size={14} />
      </button>
      <span className="ml-2 font-mono text-xs text-neutral-400">
        {state.index + 1}/{total}
      </span>
    </div>
  );
}

export function StepNote({ children }: { children: string }) {
  return (
    <p className="min-h-[2.5rem] rounded-lg bg-neutral-50 px-3 py-2 text-center text-sm text-neutral-700">
      {children}
    </p>
  );
}
