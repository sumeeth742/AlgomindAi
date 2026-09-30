"use client";

import { useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  Brain, Code2, Layers, Link2 as LinkIcon, Network, RotateCcw, ShieldCheck, Sparkles, Wifi,
} from "lucide-react";
import { useAuth } from "@/lib/auth";
import { Spinner } from "@/components/ui";

const LINK_PRIMARY = "rounded-xl bg-gradient-to-br from-emerald-500 to-teal-500 px-6 py-3 text-base font-semibold text-white shadow-md shadow-emerald-500/30 transition-all hover:shadow-lg hover:shadow-emerald-500/40 active:scale-95";
const LINK_GHOST = "rounded-xl border-2 border-neutral-200 bg-white px-6 py-3 text-base font-semibold text-neutral-700 transition-all hover:border-neutral-300 hover:bg-neutral-50 active:scale-95";

// Every number here is queried live from the real seeded database, not a
// round marketing figure -- kept in sync with README's own honesty section.
const STATS = [
  { value: "148", label: "DSA problems, reference-verified" },
  { value: "28", label: "DSA skill nodes" },
  { value: "44", label: "System Design lessons" },
  { value: "14", label: "Networking lessons" },
];

const PILLARS = [
  {
    icon: Code2, title: "DSA", gradient: "from-indigo-500 to-blue-400",
    desc: "148 problems across 28 skills, every expected output computed by executing the real reference solution -- pattern recognition, reasoning, and code are graded separately, not lumped into one pass/fail.",
  },
  {
    icon: Network, title: "System Design", gradient: "from-purple-500 to-fuchsia-400",
    desc: "44 lessons, 9 case studies scaled across startup/growth/global tiers, and 4 low-level design exercises -- critiqued by a real rule-based engine that checks your actual architecture, not a vibe check.",
  },
  {
    icon: Wifi, title: "Computer Networks", gradient: "from-blue-500 to-cyan-400",
    desc: "14 lessons from OSI fundamentals through TLS and sockets -- several with real, technically accurate narrated diagrams showing exactly how the protocol behaves, hop by hop.",
  },
];

const FEATURES = [
  {
    icon: ShieldCheck, title: "Honest feedback, always", gradient: "from-emerald-500 to-teal-400",
    desc: "Every score comes from real code execution, a real trace, or a real trained model with its accuracy disclosed -- never a fabricated number, and never hidden when a feature's accuracy is genuinely weak.",
  },
  {
    icon: Brain, title: "Local AI coaches, no API key", gradient: "from-violet-500 to-purple-400",
    desc: "Habit profiling, plan-quality scoring, reasoning gap diffs -- small classical ML models trained on this platform's own real data, running entirely on this server.",
  },
  {
    icon: Layers, title: "Full mock interview loop", gradient: "from-rose-500 to-pink-400",
    desc: "One DSA problem, one System Design case, one behavioral question -- chained into a single timed session, with every round graded by the same real engines you practice with.",
  },
  {
    icon: RotateCcw, title: "Spaced repetition that's real", gradient: "from-amber-500 to-orange-400",
    desc: "A genuine SM-2 scheduler tracks what you're actually forgetting and resurfaces it right before you would have -- not a generic \"come back tomorrow\" reminder.",
  },
  {
    icon: LinkIcon, title: "Cross-domain concept bridges", gradient: "from-sky-500 to-cyan-400",
    desc: "Real computed links between DSA, System Design, and Networks lessons, so \"Sliding Window\" and \"TCP Sliding Window\" stop being taught as two unrelated ideas.",
  },
  {
    icon: Sparkles, title: "Narrated animated walkthroughs", gradient: "from-teal-500 to-emerald-400",
    desc: "Step-by-step protocol and architecture diagrams that narrate themselves aloud using your browser's own voice -- built from real technical detail, not decorative animation.",
  },
];

function HeroLanding() {
  return (
    <div className="flex flex-col gap-14 py-8 sm:py-12">
      <section className="text-center">
        <p className="mx-auto mb-5 inline-flex items-center gap-1.5 rounded-full bg-white px-3 py-1 text-xs font-bold uppercase tracking-widest text-emerald-700 shadow-sm ring-1 ring-emerald-200">
          <Sparkles size={13} /> DSA + System Design + Networks, one adaptive platform
        </p>
        <h1 className="mx-auto max-w-3xl text-4xl font-extrabold tracking-tight text-neutral-900 sm:text-5xl">
          ALGOMIND <span className="bg-gradient-to-br from-emerald-500 to-teal-500 bg-clip-text text-transparent">AI</span>
        </h1>
        <p className="mx-auto mt-4 max-w-xl text-sm font-semibold uppercase tracking-widest text-neutral-400">
          Learn to recognize, reason, solve, remember, design, apply
        </p>
        <p className="mx-auto mt-5 max-w-2xl text-lg text-neutral-600">
          Practice coding problems, design real systems, and learn how networks actually work -- all in one place,
          with clear feedback at every step so you know exactly what to work on next.
        </p>
        <div className="mt-8 flex flex-wrap items-center justify-center gap-3">
          <Link href="/register" className={LINK_PRIMARY}>Get started free</Link>
          <Link href="/login" className={LINK_GHOST}>Log in</Link>
        </div>
      </section>

      <section className="grid grid-cols-2 gap-3 sm:grid-cols-4">
        {STATS.map((s) => (
          <div key={s.label} className="rounded-2xl border border-neutral-200 bg-white p-4 text-center shadow-sm">
            <p className="text-2xl font-extrabold text-emerald-600 sm:text-3xl">{s.value}</p>
            <p className="mt-1 text-xs font-medium text-neutral-500">{s.label}</p>
          </div>
        ))}
      </section>

      <section>
        <h2 className="mb-4 text-center text-xl font-bold text-neutral-900 sm:text-2xl">Three curricula, one adaptive system</h2>
        <div className="grid gap-4 sm:grid-cols-3">
          {PILLARS.map((p) => (
            <div key={p.title} className="rounded-2xl border border-neutral-200 bg-white p-5 shadow-sm">
              <span className={`flex h-11 w-11 items-center justify-center rounded-xl bg-gradient-to-br text-white shadow-sm ${p.gradient}`}>
                <p.icon size={20} />
              </span>
              <h3 className="mt-3 font-bold text-neutral-900">{p.title}</h3>
              <p className="mt-1.5 text-sm leading-relaxed text-neutral-600">{p.desc}</p>
            </div>
          ))}
        </div>
      </section>

      <section>
        <h2 className="mb-4 text-center text-xl font-bold text-neutral-900 sm:text-2xl">What makes this different</h2>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {FEATURES.map((f) => (
            <div key={f.title} className="rounded-2xl border border-neutral-200 bg-white p-5 shadow-sm">
              <span className={`flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br text-white shadow-sm ${f.gradient}`}>
                <f.icon size={18} />
              </span>
              <h3 className="mt-3 text-sm font-bold text-neutral-900">{f.title}</h3>
              <p className="mt-1.5 text-sm leading-relaxed text-neutral-600">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="overflow-hidden rounded-2xl bg-gradient-to-br from-emerald-500 via-teal-500 to-sky-500 p-8 text-center text-white shadow-lg sm:p-10">
        <h2 className="text-2xl font-bold sm:text-3xl">Ready to start?</h2>
        <p className="mx-auto mt-2 max-w-md text-white/85">Free to use -- no credit card, and nothing to configure since every AI feature runs locally.</p>
        <Link href="/register" className="mt-6 inline-block rounded-xl bg-white px-6 py-3 text-sm font-bold text-emerald-700 shadow-md transition-all hover:bg-emerald-50 active:scale-95">
          Create your account
        </Link>
      </section>
    </div>
  );
}

export default function Home() {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && user) router.push("/dashboard");
  }, [user, loading, router]);

  if (loading) return <div className="flex min-h-screen items-center justify-center"><Spinner label="Loading..." /></div>;
  if (user) return null;

  return <HeroLanding />;
}
