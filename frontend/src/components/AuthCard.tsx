import { ReactNode } from "react";

export function AuthCard({ title, subtitle, children }: { title: string; subtitle: string; children: ReactNode }) {
  return (
    <div className="flex min-h-screen items-center justify-center py-8">
      <div className="w-full max-w-sm">
        <div className="mb-8 text-center">
          <p className="text-2xl font-bold tracking-tight text-neutral-900">
            ALGOMIND <span className="text-emerald-600">AI</span>
          </p>
          <p className="mt-1 text-xs uppercase tracking-widest text-neutral-400">
            Learn to recognize, reason, solve, remember, design, apply
          </p>
        </div>
        <div className="rounded-2xl border border-neutral-200 bg-white p-6 shadow-lg shadow-neutral-900/5 sm:p-8">
          <h1 className="text-xl font-bold text-neutral-900">{title}</h1>
          <p className="mt-1 text-sm text-neutral-500">{subtitle}</p>
          <div className="mt-6">{children}</div>
        </div>
      </div>
    </div>
  );
}

export function TextField({
  label, type = "text", value, onChange, placeholder, required, minLength,
}: {
  label: string;
  type?: string;
  value: string;
  onChange: (v: string) => void;
  placeholder?: string;
  required?: boolean;
  minLength?: number;
}) {
  return (
    <label className="flex flex-col gap-1">
      <span className="text-sm font-medium text-neutral-700">{label}</span>
      <input
        type={type} required={required} minLength={minLength} placeholder={placeholder} value={value}
        onChange={(e) => onChange(e.target.value)}
        className="rounded-lg border border-neutral-300 px-3 py-2 text-sm outline-none transition-shadow focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100"
      />
    </label>
  );
}
