"use client";

import { useQuery } from "@tanstack/react-query";
import Link from "next/link";
import { Link2 } from "lucide-react";
import { api } from "@/lib/api";
import { ConceptBridgeItem, ConceptBridgeResponse } from "@/lib/types";

const DOMAIN_LABEL: Record<string, string> = { dsa: "DSA", system_design: "System Design", networks: "Networks" };
const DOMAIN_TONE: Record<string, string> = {
  dsa: "bg-sky-50 text-sky-800 ring-sky-200",
  system_design: "bg-emerald-50 text-emerald-800 ring-emerald-200",
  networks: "bg-amber-50 text-amber-800 ring-amber-200",
};

function hrefFor(item: ConceptBridgeItem): string {
  if (item.domain === "dsa") return `/skills?skill=${item.key}`;
  if (item.domain === "system_design") return `/system-design?lesson=${item.key}`;
  return `/networks?lesson=${item.key}`;
}

/** Real, computed cross-curriculum links (TF-IDF cosine similarity over actual
 * lesson text, local scikit-learn, no API key) -- shown only for lessons where
 * a genuine lexical bridge to one of the OTHER two curricula was found above a
 * noise floor. `domain`/`itemKey` identify the current lesson exactly as the
 * backend corpus indexes it. */
export function ConceptBridgePanel({ domain, itemKey }: { domain: "dsa" | "system_design" | "networks"; itemKey: string }) {
  const bridgesQ = useQuery({
    queryKey: ["concept-bridges", domain, itemKey],
    queryFn: async () => (await api.get<ConceptBridgeResponse>(`/concept-bridges/${domain}/${itemKey}`)).data,
    enabled: !!itemKey,
  });

  const bridges = bridgesQ.data?.bridges ?? [];
  if (bridgesQ.isLoading || bridges.length === 0) return null;

  return (
    <div className="mt-6 border-t border-neutral-200 pt-5">
      <p className="mb-2 flex items-center gap-1.5 text-xs font-bold uppercase tracking-wide text-indigo-700">
        <Link2 size={14} /> Same idea, different curriculum
      </p>
      <div className="flex flex-col gap-2">
        {bridges.map((b) => (
          <Link
            key={`${b.domain}:${b.key}`}
            href={hrefFor(b)}
            className="flex items-center justify-between gap-3 rounded-lg border border-indigo-100 bg-indigo-50/60 px-3 py-2 text-sm hover:border-indigo-300"
          >
            <span className="flex items-center gap-2">
              <span className={`rounded px-1.5 py-0.5 text-[10px] font-bold uppercase ring-1 ${DOMAIN_TONE[b.domain]}`}>
                {DOMAIN_LABEL[b.domain]}
              </span>
              <span className="font-medium text-indigo-900">{b.title}</span>
            </span>
            <span className="text-xs text-indigo-500">{Math.round(b.similarity * 100)}% overlap</span>
          </Link>
        ))}
      </div>
    </div>
  );
}
