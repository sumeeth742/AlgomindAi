import { ReactNode } from "react";

export function Card({ children, className = "" }: { children: ReactNode; className?: string }) {
  return (
    <div className={`rounded-2xl border border-neutral-200 bg-white p-4 shadow-sm sm:p-5 ${className}`}>
      {children}
    </div>
  );
}

export function SectionTitle({ children, subtitle }: { children: ReactNode; subtitle?: string }) {
  return (
    <div className="mb-4">
      <h1 className="text-xl font-bold tracking-tight text-neutral-900 sm:text-2xl">{children}</h1>
      {subtitle && <p className="mt-1 text-sm text-neutral-500">{subtitle}</p>}
    </div>
  );
}

/** A vivid gradient header banner, used at the top of every page so the app
 * reads as colorful throughout, not just in isolated accents. */
export function PageHero({
  icon: Icon, title, subtitle, gradient,
}: {
  icon: React.ComponentType<{ size?: number; className?: string }>;
  title: string;
  subtitle: string;
  gradient: string;
}) {
  return (
    <div className={`mb-6 overflow-hidden rounded-2xl bg-gradient-to-br ${gradient} p-5 text-white shadow-lg sm:p-7`}>
      <div className="flex items-center gap-3.5">
        <span className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-white/20">
          <Icon size={24} />
        </span>
        <div>
          <h1 className="text-xl font-bold sm:text-2xl">{title}</h1>
          <p className="mt-0.5 text-sm text-white/85">{subtitle}</p>
        </div>
      </div>
    </div>
  );
}

export function Badge({ children, tone = "neutral" }: { children: ReactNode; tone?: "neutral" | "emerald" | "amber" | "red" | "purple" | "sky" | "pink" }) {
  const tones: Record<string, string> = {
    neutral: "bg-neutral-100 text-neutral-700",
    emerald: "bg-emerald-100 text-emerald-700",
    amber: "bg-amber-100 text-amber-700",
    red: "bg-red-100 text-red-700",
    purple: "bg-purple-100 text-purple-700",
    sky: "bg-sky-100 text-sky-700",
    pink: "bg-pink-100 text-pink-700",
  };
  return <span className={`rounded-full px-2.5 py-0.5 text-xs font-bold ${tones[tone]}`}>{children}</span>;
}

// A vivid, deterministic color identity per chapter name -- same chapter always
// gets the same color family, so a learner can spot "this is the same topic" at
// a glance. Each entry gives every surface a card needs: a pill badge, a solid
// dot/bar, a light tint for a selected/active background, a ring for emphasis,
// and a strong text color -- all from the same hue, so nothing looks washed out.
const CHAPTER_PALETTE: { badge: string; dot: string; solidBg: string; softBg: string; ring: string; text: string; gradient: string }[] = [
  { badge: "bg-emerald-100 text-emerald-700", dot: "bg-emerald-500", solidBg: "bg-emerald-500", softBg: "bg-emerald-50", ring: "ring-emerald-400", text: "text-emerald-700", gradient: "from-emerald-500 to-teal-400" },
  { badge: "bg-sky-100 text-sky-700", dot: "bg-sky-500", solidBg: "bg-sky-500", softBg: "bg-sky-50", ring: "ring-sky-400", text: "text-sky-700", gradient: "from-sky-500 to-cyan-400" },
  { badge: "bg-amber-100 text-amber-700", dot: "bg-amber-500", solidBg: "bg-amber-500", softBg: "bg-amber-50", ring: "ring-amber-400", text: "text-amber-700", gradient: "from-amber-500 to-orange-400" },
  { badge: "bg-purple-100 text-purple-700", dot: "bg-purple-500", solidBg: "bg-purple-500", softBg: "bg-purple-50", ring: "ring-purple-400", text: "text-purple-700", gradient: "from-purple-500 to-fuchsia-400" },
  { badge: "bg-pink-100 text-pink-700", dot: "bg-pink-500", solidBg: "bg-pink-500", softBg: "bg-pink-50", ring: "ring-pink-400", text: "text-pink-700", gradient: "from-pink-500 to-rose-400" },
  { badge: "bg-indigo-100 text-indigo-700", dot: "bg-indigo-500", solidBg: "bg-indigo-500", softBg: "bg-indigo-50", ring: "ring-indigo-400", text: "text-indigo-700", gradient: "from-indigo-500 to-blue-400" },
  { badge: "bg-teal-100 text-teal-700", dot: "bg-teal-500", solidBg: "bg-teal-500", softBg: "bg-teal-50", ring: "ring-teal-400", text: "text-teal-700", gradient: "from-teal-500 to-emerald-400" },
  { badge: "bg-orange-100 text-orange-700", dot: "bg-orange-500", solidBg: "bg-orange-500", softBg: "bg-orange-50", ring: "ring-orange-400", text: "text-orange-700", gradient: "from-orange-500 to-amber-400" },
  { badge: "bg-violet-100 text-violet-700", dot: "bg-violet-500", solidBg: "bg-violet-500", softBg: "bg-violet-50", ring: "ring-violet-400", text: "text-violet-700", gradient: "from-violet-500 to-purple-400" },
  { badge: "bg-rose-100 text-rose-700", dot: "bg-rose-500", solidBg: "bg-rose-500", softBg: "bg-rose-50", ring: "ring-rose-400", text: "text-rose-700", gradient: "from-rose-500 to-pink-400" },
];

export function chapterColor(chapter: string) {
  let hash = 0;
  for (let i = 0; i < chapter.length; i++) hash = (hash * 31 + chapter.charCodeAt(i)) >>> 0;
  return CHAPTER_PALETTE[hash % CHAPTER_PALETTE.length];
}

export function ChapterBadge({ chapter }: { chapter: string }) {
  const c = chapterColor(chapter);
  return (
    <span className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-bold ${c.badge}`}>
      <span className={`h-2 w-2 rounded-full ${c.dot}`} />
      {chapter}
    </span>
  );
}

/** A colored circular icon chip, e.g. for nav items and chapter headers. */
export function IconChip({ icon: Icon, gradient, size = 34 }: { icon: React.ComponentType<{ size?: number; className?: string }>; gradient: string; size?: number }) {
  return (
    <span
      className={`inline-flex shrink-0 items-center justify-center rounded-xl bg-gradient-to-br text-white shadow-sm ${gradient}`}
      style={{ width: size, height: size }}
    >
      <Icon size={size * 0.55} />
    </span>
  );
}

export function Button({
  children, onClick, disabled, variant = "primary", type = "button", className = "",
}: {
  children: ReactNode;
  onClick?: () => void;
  disabled?: boolean;
  variant?: "primary" | "secondary" | "ghost" | "danger";
  type?: "button" | "submit";
  className?: string;
}) {
  const base = "rounded-xl px-4 py-2 text-sm font-semibold transition-all active:scale-95 disabled:cursor-not-allowed disabled:opacity-50 disabled:active:scale-100";
  const variants: Record<string, string> = {
    primary: "bg-gradient-to-br from-emerald-500 to-teal-500 text-white shadow-md shadow-emerald-500/30 hover:shadow-lg hover:shadow-emerald-500/40",
    secondary: "bg-gradient-to-br from-indigo-500 to-violet-500 text-white shadow-md shadow-indigo-500/30 hover:shadow-lg hover:shadow-indigo-500/40",
    ghost: "border-2 border-neutral-200 text-neutral-700 hover:border-neutral-300 hover:bg-neutral-50",
    danger: "bg-gradient-to-br from-red-500 to-rose-500 text-white shadow-md shadow-red-500/30 hover:shadow-lg hover:shadow-red-500/40",
  };
  return (
    <button type={type} onClick={onClick} disabled={disabled} className={`${base} ${variants[variant]} ${className}`}>
      {children}
    </button>
  );
}

export function AiLabel() {
  return (
    <span className="inline-flex items-center gap-1 rounded-full bg-gradient-to-r from-violet-500 to-fuchsia-500 px-2.5 py-0.5 text-[10px] font-bold uppercase tracking-wide text-white">
      AI-generated
    </span>
  );
}

export function Spinner({ label }: { label?: string }) {
  return (
    <div className="flex items-center gap-2 text-sm text-neutral-500">
      <span className="h-3.5 w-3.5 animate-spin rounded-full border-2 border-neutral-300 border-t-emerald-600" />
      {label}
    </div>
  );
}
