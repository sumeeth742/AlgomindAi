import axios from "axios";

export const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export const api = axios.create({ baseURL: API_URL });

api.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = window.localStorage.getItem("algomind_token");
    if (token) {
      config.headers = config.headers ?? {};
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

export function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return window.localStorage.getItem("algomind_token");
}

export function setToken(token: string) {
  window.localStorage.setItem("algomind_token", token);
}

export function clearToken() {
  window.localStorage.removeItem("algomind_token");
}
