"use client";

import { useState } from "react";
import axios from "axios";
import Link from "next/link";
import { useAuth } from "@/lib/auth";
import { AuthCard, TextField } from "@/components/AuthCard";
import { Button } from "@/components/ui";

// FastAPI returns either a plain string `detail` (e.g. "Email already
// registered") or, for a Pydantic field validation failure, a list of
// {msg, loc, ...} objects -- surface the real reason either way instead of
// guessing.
function extractErrorMessage(err: unknown): string {
  if (axios.isAxiosError(err)) {
    const detail = err.response?.data?.detail;
    if (typeof detail === "string") return detail;
    if (Array.isArray(detail) && typeof detail[0]?.msg === "string") {
      return detail[0].msg.replace(/^Value error,\s*/, "");
    }
  }
  return "Could not create your account -- please check your details and try again.";
}

export default function RegisterPage() {
  const { register } = useAuth();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setBusy(true);
    try {
      await register(email, password, name);
    } catch (err) {
      setError(extractErrorMessage(err));
    } finally {
      setBusy(false);
    }
  }

  return (
    <AuthCard title="Create your account" subtitle="Start with a quick check of what you already know, then follow a study plan built around it.">
      <form onSubmit={onSubmit} className="flex flex-col gap-4">
        <div>
          <TextField label="Name" required value={name} onChange={setName} placeholder="Ada Lovelace" />
          <p className="mt-1 text-xs text-neutral-400">Letters only -- no numbers or symbols.</p>
        </div>
        <TextField label="Email" type="email" required value={email} onChange={setEmail} placeholder="you@example.com" />
        <div>
          <TextField label="Password" type="password" required minLength={8} value={password} onChange={setPassword} placeholder="min. 8 characters" />
          <p className="mt-1 text-xs text-neutral-400">At least 8 characters, with at least one letter and one number.</p>
        </div>
        {error && <p className="text-sm text-red-600">{error}</p>}
        <Button type="submit" disabled={busy} className="w-full">
          {busy ? "Creating account..." : "Create account"}
        </Button>
      </form>
      <p className="mt-5 text-center text-sm text-neutral-600">
        Already have an account? <Link href="/login" className="font-medium text-emerald-700 underline">Log in</Link>
      </p>
    </AuthCard>
  );
}
