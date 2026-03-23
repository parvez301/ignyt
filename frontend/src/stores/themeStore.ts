import { create } from "zustand";
import { persist } from "zustand/middleware";

type Theme = "light" | "dark";

interface ThemeState {
  theme: Theme;
  setTheme: (t: Theme) => void;
  applyDom: () => void;
}

export const useThemeStore = create<ThemeState>()(
  persist(
    (set, get) => ({
      theme: "dark",
      setTheme: (theme) => {
        set({ theme });
        get().applyDom();
      },
      applyDom: () => {
        const root = document.documentElement;
        if (get().theme === "dark") root.classList.add("dark");
        else root.classList.remove("dark");
      },
    }),
    { name: "ignyt-theme", partialize: (s) => ({ theme: s.theme }) },
  ),
);
