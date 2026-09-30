"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { LayoutDashboard, GitBranch, Code2, RotateCcw, Network, NotebookText, Wifi, MessageSquare, Trophy, LogOut } from "lucide-react";
import { useAuth } from "@/lib/auth";

const LINKS = [
  { href: "/dashboard", label: "Dashboard", Icon: LayoutDashboard, gradient: "from-emerald-500 to-teal-400", soft: "bg-emerald-50 text-emerald-700" },
  { href: "/skills", label: "DSA Concepts", Icon: GitBranch, gradient: "from-sky-500 to-cyan-400", soft: "bg-sky-50 text-sky-700" },
  { href: "/problems", label: "Problems", Icon: Code2, gradient: "from-indigo-500 to-blue-400", soft: "bg-indigo-50 text-indigo-700" },
  { href: "/contests", label: "Contests", Icon: Trophy, gradient: "from-yellow-500 to-amber-400", soft: "bg-yellow-50 text-yellow-700" },
  { href: "/retention", label: "Retention", Icon: RotateCcw, gradient: "from-amber-500 to-orange-400", soft: "bg-amber-50 text-amber-700" },
  { href: "/system-design", label: "System Design", Icon: Network, gradient: "from-purple-500 to-fuchsia-400", soft: "bg-purple-50 text-purple-700" },
  { href: "/networks", label: "Computer Networks", Icon: Wifi, gradient: "from-blue-500 to-cyan-400", soft: "bg-blue-50 text-blue-700" },
  { href: "/cheat-sheet", label: "Cheat Sheet", Icon: NotebookText, gradient: "from-teal-500 to-cyan-400", soft: "bg-teal-50 text-teal-700" },
  { href: "/interview", label: "Interview", Icon: MessageSquare, gradient: "from-pink-500 to-rose-400", soft: "bg-pink-50 text-pink-700" },
];

export function Sidebar() {
  const { user, logout } = useAuth();
  const pathname = usePathname();

  if (!user) return null;

  return (
    <aside data-print-hide className="fixed inset-y-0 left-0 hidden w-60 flex-col border-r border-neutral-200 bg-white md:flex">
      <Link href="/dashboard" className="flex items-center px-5 py-5 text-lg font-extrabold tracking-tight text-neutral-900">
        ALGOMIND{" "}
        <span className="ml-1 bg-gradient-to-r from-emerald-500 to-teal-500 bg-clip-text text-transparent">AI</span>
      </Link>

      <nav className="flex flex-1 flex-col gap-1 px-3">
        {LINKS.map((l) => {
          const active = pathname?.startsWith(l.href);
          return (
            <Link
              key={l.href} href={l.href}
              className={`flex items-center gap-2.5 rounded-xl px-2.5 py-2 text-sm font-medium transition-all ${
                active ? l.soft : "text-neutral-500 hover:bg-neutral-50 hover:text-neutral-900"
              }`}
            >
              <span
                className={`flex h-7 w-7 shrink-0 items-center justify-center rounded-lg ${
                  active ? `bg-gradient-to-br ${l.gradient} text-white shadow-sm` : "bg-neutral-100 text-neutral-400"
                }`}
              >
                <l.Icon size={15} strokeWidth={2.25} />
              </span>
              {l.label}
            </Link>
          );
        })}
      </nav>

      <div className="border-t border-neutral-200 px-5 py-4">
        <p className="truncate text-sm font-semibold text-neutral-700">{user.name}</p>
        <p className="truncate text-xs text-neutral-400">{user.email}</p>
        <button onClick={logout} className="mt-2 flex items-center gap-1.5 text-xs font-medium text-neutral-400 hover:text-red-600">
          <LogOut size={13} /> Log out
        </button>
      </div>
    </aside>
  );
}
