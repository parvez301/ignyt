import { useEffect } from "react";
import { Link } from "react-router-dom";
import { ThemeToggle } from "@/components/common/ThemeToggle";
import api from "@/api/client";
import { useAuth } from "@/hooks/useAuth";
import { useProgressStore } from "@/stores/progressStore";
import { useThemeStore } from "@/stores/themeStore";

export default function HomePage() {
  const { user, logout } = useAuth();
  const { me, setMe, chapterId, setChapterId } = useProgressStore();
  const { setTheme, applyDom } = useThemeStore();

  useEffect(() => {
    api
      .get("/users/me/progress")
      .then((r) => setMe(r.data))
      .catch(() => {});
  }, [setMe]);

  useEffect(() => {
    async function loadChapter() {
      const sub = await api.get("/subjects", { params: { page: 1, per_page: 5 } });
      const sid = sub.data.items[0]?.id;
      if (!sid) return;
      const grades = await api.get(`/subjects/${sid}/grades`, { params: { page: 1, per_page: 5 } });
      const gid = grades.data.items[0]?.id;
      if (!gid) return;
      const ch = await api.get(`/grades/${gid}/chapters`, { params: { page: 1, per_page: 5 } });
      const cid = ch.data.items[0]?.id;
      if (cid) setChapterId(cid);
    }
    loadChapter();
  }, [setChapterId]);

  useEffect(() => {
    if (user?.theme === "light" || user?.theme === "dark") {
      setTheme(user.theme);
      applyDom();
    }
  }, [user?.theme, setTheme, applyDom]);

  return (
    <div className="mx-auto min-h-screen max-w-5xl p-6">
      <header className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-[var(--text-primary)]">Hi, {user?.display_name}!</h1>
          <p className="text-[var(--text-secondary)]">Ready for your next quest?</p>
        </div>
        <div className="flex items-center gap-2">
          <ThemeToggle />
          <button type="button" className="text-sm text-[var(--text-secondary)] underline" onClick={logout}>
            Log out
          </button>
        </div>
      </header>
      <div className="grid gap-4 md:grid-cols-2">
        <div className="rounded-2xl bg-[var(--bg-card)] p-6 shadow">
          <p className="text-sm text-[var(--text-secondary)]">Total XP</p>
          <p className="text-3xl font-semibold text-[var(--text-primary)]">{me?.total_xp ?? "—"}</p>
          <p className="text-sm text-[var(--text-secondary)]">Level {me?.level ?? "—"}</p>
        </div>
        <div className="rounded-2xl bg-[var(--bg-card)] p-6 shadow">
          <p className="text-sm text-[var(--text-secondary)]">Streak</p>
          <p className="text-3xl font-semibold text-[var(--text-primary)]">{me?.streak_current ?? 0} days</p>
        </div>
        <Link
          to={chapterId ? `/chapter/${chapterId}` : "#"}
          className="block rounded-2xl bg-[var(--brand)] p-6 text-center font-medium text-white shadow hover:opacity-95"
        >
          Continue — Chapter map
        </Link>
        <Link
          to="/leaderboard"
          className="block rounded-2xl border border-[var(--bg-surface)] bg-[var(--bg-card)] p-6 text-center font-medium text-[var(--text-primary)] shadow"
        >
          Leaderboard
        </Link>
        <Link
          to="/profile"
          className="block rounded-2xl border border-[var(--bg-surface)] bg-[var(--bg-card)] p-6 text-center font-medium text-[var(--text-primary)] shadow"
        >
          Profile & badges
        </Link>
      </div>
    </div>
  );
}
