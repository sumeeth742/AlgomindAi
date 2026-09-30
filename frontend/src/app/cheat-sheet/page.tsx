"use client";

import { useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { NotebookText, Printer } from "lucide-react";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import { Card, PageHero, Spinner } from "@/components/ui";
import { api } from "@/lib/api";
import { CheatSheetGroup } from "@/lib/types";

type Curriculum = "dsa" | "system-design" | "networks";

const CURRICULUM_LABEL: Record<Curriculum, string> = {
  dsa: "DSA", "system-design": "System Design", networks: "Computer Networks",
};

function CheatSheetContent() {
  const [curriculum, setCurriculum] = useState<Curriculum>("dsa");

  const sheetQ = useQuery({
    queryKey: ["cheat-sheet", curriculum],
    queryFn: async () => (await api.get<CheatSheetGroup[]>(`/cheat-sheet/${curriculum}`)).data,
  });

  return (
    <div>
      <div data-print-hide className="mb-6 flex flex-wrap items-center justify-between gap-3">
        <div className="flex gap-1 rounded-lg bg-neutral-100 p-1 text-sm font-medium">
          {(Object.keys(CURRICULUM_LABEL) as Curriculum[]).map((c) => (
            <button
              key={c}
              onClick={() => setCurriculum(c)}
              className={`rounded-md px-3.5 py-1.5 transition-colors ${
                curriculum === c ? "bg-white text-teal-700 shadow-sm" : "text-neutral-500 hover:text-neutral-800"
              }`}
            >
              {CURRICULUM_LABEL[c]}
            </button>
          ))}
        </div>
        <button
          onClick={() => window.print()}
          className="flex items-center gap-1.5 rounded-xl bg-gradient-to-br from-teal-500 to-cyan-500 px-4 py-2 text-sm font-semibold text-white shadow-md shadow-teal-500/30 transition-all hover:shadow-lg active:scale-95"
        >
          <Printer size={15} /> Print / Save as PDF
        </button>
      </div>

      {/* A real printed title -- invisible on screen, shown only on paper, since
          the on-screen PageHero above is deliberately hidden when printing. */}
      <h1 className="mb-4 hidden text-2xl font-bold print:block">
        ALGOMIND AI -- {CURRICULUM_LABEL[curriculum]} Study Cheat Sheet
      </h1>

      {sheetQ.isLoading && <Spinner label="Building cheat sheet..." />}

      <div className="flex flex-col gap-6">
        {sheetQ.data?.map((group) => (
          <div key={group.group} className="break-inside-avoid">
            <h2 className="mb-2.5 text-xs font-bold uppercase tracking-wide text-teal-700">{group.group}</h2>
            <div className="flex flex-col gap-2.5">
              {group.items.map((item) => (
                <Card key={item.key} className="break-inside-avoid print:border print:border-neutral-300 print:shadow-none">
                  <h3 className="font-bold text-neutral-900">{item.title}</h3>
                  {item.mnemonic && (
                    <p className="mt-1 text-sm italic text-amber-700">&ldquo;{item.mnemonic}&rdquo;</p>
                  )}
                  <p className="mt-1.5 text-sm leading-relaxed text-neutral-600">{item.key_takeaway}</p>
                </Card>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default function CheatSheetPage() {
  return (
    <ProtectedRoute>
      <div data-print-hide>
        <PageHero
          icon={NotebookText} title="Study Cheat Sheet" gradient="from-teal-500 to-cyan-400"
          subtitle="Every skill's real mnemonic and key takeaway, condensed to one page per curriculum -- pick a tab, then print or save as PDF."
        />
      </div>
      <CheatSheetContent />
    </ProtectedRoute>
  );
}
