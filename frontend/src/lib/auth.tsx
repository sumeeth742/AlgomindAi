"use client";

import { createContext, useContext, useEffect, useState, ReactNode } from "react";
import { useRouter } from "next/navigation";
import { api, clearToken, getToken, setToken } from "./api";
import { UserOut } from "./types";

interface AuthContextValue {
  user: UserOut | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, name: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<UserOut | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  async function loadMe() {
    try {
      const res = await api.get<UserOut>("/auth/me");
      setUser(res.data);
    } catch {
      setUser(null);
      clearToken();
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    // Session bootstrap on mount: check for a stored token and validate it against
    // the API. This is a one-time async fetch-on-mount, not a render-time state sync.
    if (getToken()) {
      // eslint-disable-next-line react-hooks/set-state-in-effect
      loadMe();
    } else {
      setLoading(false);
    }
  }, []);

  async function login(email: string, password: string) {
    const form = new URLSearchParams();
    form.set("username", email);
    form.set("password", password);
    const res = await api.post<{ access_token: string }>("/auth/login", form, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });
    setToken(res.data.access_token);
    await loadMe();
    router.push("/dashboard");
  }

  async function register(email: string, password: string, name: string) {
    const res = await api.post<{ access_token: string }>("/auth/register", {
      email, password, name, interface_mode: "beginner",
    });
    setToken(res.data.access_token);
    await loadMe();
    router.push("/dashboard");
  }

  function logout() {
    clearToken();
    setUser(null);
    router.push("/login");
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used inside AuthProvider");
  return ctx;
}
