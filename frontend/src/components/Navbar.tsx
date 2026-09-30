"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { useAuth } from "@/lib/auth";

const LINKS = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/skills", label: "DSA Concepts" },
  { href: "/problems", label: "Problems" },
  { href: "/contests", label: "Contests" },
  { href: "/retention", label: "Retention" },
  { href: "/system-design", label: "System Design" },
  { href: "/networks", label: "Computer Networks" },
  { href: "/cheat-sheet", label: "Cheat Sheet" },
  { href: "/interview", label: "Interview" },
];

/** Mobile-only top bar. On desktop, the Sidebar component provides navigation instead. */
export function Navbar() {
  const { user, logout } = useAuth();
  const pathname = usePathname();
  const [open, setOpen] = useState(false);

  if (!user) return null;

  return (
    <nav data-print-hide className="sticky top-0 z-20 border-b border-neutral-200 bg-white/90 backdrop-blur md:hidden">
      <div className="flex items-center justify-between px-4 py-3">
        <Link href="/dashboard" className="font-bold tracking-tight text-neutral-900" onClick={() => setOpen(false)}>
          ALGOMIND <span className="text-emerald-600">AI</span>
        </Link>

        <button
          onClick={() => setOpen((v) => !v)}
          aria-label="Toggle menu"
          className="flex h-9 w-9 items-center justify-center rounded-lg border border-neutral-200 text-neutral-700"
        >
          {open ? "×" : "☰"}
        </button>
      </div>

      {open && (
        <div className="flex flex-col gap-1 border-t border-neutral-200 px-4 py-3 text-sm">
          {LINKS.map((l) => (
            <Link
              key={l.href} href={l.href} onClick={() => setOpen(false)}
              className={`rounded-lg px-2 py-2 ${pathname?.startsWith(l.href) ? "bg-emerald-50 font-medium text-emerald-700" : "text-neutral-600"}`}
            >
              {l.label}
            </Link>
          ))}
          <div className="mt-2 flex items-center justify-between border-t border-neutral-200 px-2 pt-3">
            <span className="text-neutral-400">{user.name}</span>
            <button onClick={logout} className="text-neutral-500 hover:text-red-600">
              Log out
            </button>
          </div>
        </div>
      )}
    </nav>
  );
}
