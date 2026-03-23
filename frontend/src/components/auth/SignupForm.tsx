import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "@/api/client";
import { useAuthStore } from "@/stores/authStore";

export function SignupForm() {
  const nav = useNavigate();
  const setAuth = useAuthStore((s) => s.setAuth);
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [displayName, setDisplayName] = useState("");
  const [err, setErr] = useState("");

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setErr("");
    try {
      const { data } = await api.post("/auth/signup", {
        username,
        email,
        password,
        display_name: displayName,
      });
      setAuth(data.token, data.user);
      nav("/");
    } catch (ex: unknown) {
      const msg =
        (ex as { response?: { data?: { detail?: string } } })?.response?.data?.detail ||
        "Could not create account.";
      setErr(String(msg));
    }
  }

  return (
    <form onSubmit={onSubmit} className="mx-auto flex max-w-md flex-col gap-4 rounded-2xl bg-[var(--bg-card)] p-8 shadow-lg">
      <h1 className="text-2xl font-semibold text-[var(--text-primary)]">Join Ignyt</h1>
      {err && <p className="text-sm text-amber-600 dark:text-amber-400">{err}</p>}
      <label className="flex flex-col gap-1 text-sm text-[var(--text-secondary)]">
        Display name
        <input
          className="rounded-lg border border-[var(--bg-surface)] bg-[var(--bg-primary)] px-3 py-2 text-[var(--text-primary)]"
          value={displayName}
          onChange={(e) => setDisplayName(e.target.value)}
        />
      </label>
      <label className="flex flex-col gap-1 text-sm text-[var(--text-secondary)]">
        Username
        <input
          className="rounded-lg border border-[var(--bg-surface)] bg-[var(--bg-primary)] px-3 py-2 text-[var(--text-primary)]"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          autoComplete="username"
        />
      </label>
      <label className="flex flex-col gap-1 text-sm text-[var(--text-secondary)]">
        Email
        <input
          type="email"
          className="rounded-lg border border-[var(--bg-surface)] bg-[var(--bg-primary)] px-3 py-2 text-[var(--text-primary)]"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          autoComplete="email"
        />
      </label>
      <label className="flex flex-col gap-1 text-sm text-[var(--text-secondary)]">
        Password
        <input
          type="password"
          className="rounded-lg border border-[var(--bg-surface)] bg-[var(--bg-primary)] px-3 py-2 text-[var(--text-primary)]"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          autoComplete="new-password"
        />
      </label>
      <button type="submit" className="rounded-xl bg-[var(--brand)] py-3 font-medium text-white">
        Sign up
      </button>
      <p className="text-center text-sm text-[var(--text-secondary)]">
        Already have an account?{" "}
        <Link to="/login" className="text-[var(--brand)]">
          Log in
        </Link>
      </p>
    </form>
  );
}
