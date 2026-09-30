"use client";

import { ReactNode } from "react";
import { useAuth } from "@/lib/auth";
import { Navbar } from "@/components/Navbar";
import { Sidebar } from "@/components/Sidebar";

export function AppShell({ children }: { children: ReactNode }) {
  const { user } = useAuth();

  if (!user) {
    // Logged-out pages (login/register) own their own centered layout -- no
    // sidebar gutter to reserve space for.
    return <main className="mx-auto w-full max-w-5xl flex-1 px-4 sm:px-6 lg:px-8">{children}</main>;
  }

  return (
    <>
      <Sidebar />
      <div data-print-content className="flex min-h-full flex-col md:pl-60">
        <Navbar />
        <main className="mx-auto w-full max-w-5xl flex-1 px-4 py-6 sm:px-6 lg:px-8">{children}</main>
      </div>
    </>
  );
}
