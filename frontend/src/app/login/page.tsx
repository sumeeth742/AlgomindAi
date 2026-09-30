"use client";

import { useState } from "react";
import Link from "next/link";
import { useAuth } from "@/lib/auth";
import { AuthCard, TextField } from "@/components/AuthCard";
import { Button } from "@/components/ui";

export default function LoginPage() {
  const { login } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setBusy(true);
    try {
      await login(email, password);
    } catch {
      setError("Incorrect email or password.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <AuthCard title="Welcome back" subtitle="Log in to continue your learning path.">
      <form onSubmit={onSubmit} className="flex flex-col gap-4">
        <TextField label="Email" type="email" required value={email} onChange={setEmail} placeholder="you@example.com" />
        <TextField label="Password" type="password" required value={password} onChange={setPassword} placeholder="••••••••" />
        {error && <p className="text-sm text-red-600">{error}</p>}
        <Button type="submit" disabled={busy} className="w-full">
          {busy ? "Logging in..." : "Log in"}
        </Button>
      </form>
      <p className="mt-5 text-center text-sm text-neutral-600">
        No account? <Link href="/register" className="font-medium text-emerald-700 underline">Register</Link>
      </p>
    </AuthCard>
  );
}
