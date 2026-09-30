"use client";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

/**
 * @tailwindcss/typography's `prose` classes give real book-like typography
 * (heading hierarchy, paragraph/list spacing, styled code blocks) -- without
 * the plugin installed and registered, `prose` is a no-op and every heading,
 * paragraph, and list renders as flat, unspaced browser-default text. The
 * extra prose-* overrides below layer a chapter-like feel on top: a rule
 * under h2s, relaxed line-height, and code blocks that read as diagrams
 * (used for the ASCII architecture sketches in system design lessons) rather
 * than plain text dumps.
 */
export function Markdown({ children, size = "base" }: { children: string; size?: "base" | "lg" }) {
  return (
    <div
      className={`prose prose-neutral max-w-none ${size === "lg" ? "prose-lg" : ""}
        prose-headings:font-bold prose-headings:tracking-tight
        prose-h1:mb-4
        prose-h2:mt-9 prose-h2:mb-3 prose-h2:border-b prose-h2:border-neutral-200 prose-h2:pb-2
        prose-h3:mt-6
        prose-p:leading-relaxed prose-li:leading-relaxed prose-li:my-1
        prose-ul:my-4 prose-ol:my-4
        prose-strong:font-semibold prose-strong:text-neutral-900
        prose-pre:rounded-xl prose-pre:bg-neutral-900 prose-pre:text-neutral-100 prose-pre:shadow-sm prose-pre:leading-normal
        prose-code:rounded prose-code:bg-neutral-100 prose-code:px-1.5 prose-code:py-0.5 prose-code:text-[0.85em] prose-code:font-normal prose-code:before:content-none prose-code:after:content-none
        prose-pre:prose-code:bg-transparent prose-pre:prose-code:p-0
        prose-blockquote:border-l-4 prose-blockquote:border-emerald-300 prose-blockquote:font-normal prose-blockquote:not-italic prose-blockquote:text-neutral-600
        prose-table:my-4 prose-th:bg-neutral-50 prose-th:text-left prose-td:align-top`}
    >
      <ReactMarkdown remarkPlugins={[remarkGfm]}>{children}</ReactMarkdown>
    </div>
  );
}
