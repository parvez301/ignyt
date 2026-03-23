import { Moon, Sun } from "./Icons";
import api from "@/api/client";
import { useAuthStore } from "@/stores/authStore";
import { useThemeStore } from "@/stores/themeStore";

export function ThemeToggle() {
  const { theme, setTheme, applyDom } = useThemeStore();
  const token = useAuthStore((s) => s.token);

  async function toggle() {
    const next = theme === "dark" ? "light" : "dark";
    setTheme(next);
    applyDom();
    if (token) {
      try {
        const { data } = await api.patch("/auth/me", { theme: next });
        useAuthStore.setState({ user: data });
      } catch {
        /* ignore */
      }
    }
  }

  return (
    <button
      type="button"
      aria-label="Toggle theme"
      className="rounded-lg p-2 text-[var(--text-secondary)] hover:bg-[var(--bg-surface)]"
      onClick={toggle}
    >
      {theme === "dark" ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
    </button>
  );
}
