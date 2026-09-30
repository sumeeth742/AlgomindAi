"use client";

interface ComicPanel {
  speaker: string; // "mira" | "dev"
  text: string;
}

const PERSONA: Record<string, { name: string; avatar: string; bg: string; ring: string; bubbleBg: string; align: "left" | "right" }> = {
  mira: { name: "Mira", avatar: "🙋", bg: "from-sky-500 to-cyan-400", ring: "ring-sky-200", bubbleBg: "bg-sky-50 border-sky-200", align: "left" },
  dev: { name: "Dev", avatar: "🧑‍💻", bg: "from-emerald-500 to-teal-400", ring: "ring-emerald-200", bubbleBg: "bg-emerald-50 border-emerald-200", align: "right" },
};

/** Renders a lesson's plain-language walkthrough as a continuous comic strip --
 * Mira (a curious learner) and Dev (a patient guide) talk through the concept
 * panel by panel, in everyday language with no unexplained jargon. This is a
 * second, easier path through the same material, not a replacement for the
 * full lesson -- some learners just need the "explain it like I'm five"
 * version before the dense version clicks. */
export function ComicPanels({ panels }: { panels: ComicPanel[] }) {
  if (!panels || panels.length === 0) return null;

  return (
    <div className="rounded-2xl border-2 border-neutral-900/10 bg-[repeating-linear-gradient(45deg,rgba(0,0,0,0.015)_0px,rgba(0,0,0,0.015)_1px,transparent_1px,transparent_8px)] bg-neutral-50 p-3 sm:p-5">
      <div className="mb-4 flex items-center gap-2">
        <span className="text-lg">💬</span>
        <p className="text-xs font-bold uppercase tracking-wide text-neutral-500">The simple version -- a conversation</p>
      </div>
      <div className="flex flex-col gap-3">
        {panels.map((panel, i) => {
          const p = PERSONA[panel.speaker] ?? PERSONA.dev;
          const isLeft = p.align === "left";
          return (
            <div
              key={i}
              className={`flex items-end gap-2.5 rounded-xl border-2 border-neutral-900/15 bg-white p-3 shadow-[3px_3px_0_rgba(0,0,0,0.06)] ${
                isLeft ? "flex-row" : "flex-row-reverse"
              }`}
            >
              <div
                className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-gradient-to-br ${p.bg} text-base ring-2 ${p.ring} sm:h-10 sm:w-10`}
                title={p.name}
              >
                {p.avatar}
              </div>
              <div className={`relative flex-1 rounded-2xl border px-3.5 py-2.5 text-sm leading-relaxed text-neutral-800 ${p.bubbleBg}`}>
                <p className="mb-0.5 text-[11px] font-bold uppercase tracking-wide text-neutral-400">{p.name}</p>
                {panel.text}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
