import { useEffect } from "react";
import { useAuthStore } from "@/stores/authStore";
import api from "@/api/client";
import { useThemeStore } from "@/stores/themeStore";

export function useThemeBootstrap() {
  const user = useAuthStore((s) => s.user);
  const { theme, setTheme, applyDom } = useThemeStore();

  useEffect(() => {
    if (user?.theme === "light" || user?.theme === "dark") {
      setTheme(user.theme);
    }
    applyDom();
  }, [user?.theme, setTheme, applyDom]);

  async function persistTheme(next: "light" | "dark") {
    setTheme(next);
    try {
      await api.patch("/auth/me", { theme: next });
    } catch {
      /* offline */
    }
  }

  return { theme, persistTheme };
}
