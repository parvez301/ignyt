import { create } from "zustand";

export interface MeProgress {
  total_xp: number;
  level: number;
  streak_current: number;
  streak_longest: number;
  total_stars: number;
}

interface ProgressState {
  me: MeProgress | null;
  chapterId: string | null;
  setMe: (m: MeProgress | null) => void;
  setChapterId: (id: string | null) => void;
}

export const useProgressStore = create<ProgressState>((set) => ({
  me: null,
  chapterId: null,
  setMe: (me) => set({ me }),
  setChapterId: (chapterId) => set({ chapterId }),
}));
