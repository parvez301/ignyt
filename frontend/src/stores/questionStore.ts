import { create } from "zustand";
import type { GeneratedQuestionItem } from "@/types";

interface QuestionState {
  topicId: string | null;
  phase: "practice" | "master";
  items: GeneratedQuestionItem[];
  index: number;
  sessionCorrect: number;
  hintsUsedThisQuestion: number;
  reset: (topicId: string, phase: "practice" | "master", items: GeneratedQuestionItem[]) => void;
  next: () => void;
  incCorrect: () => void;
  setHintsUsed: (n: number) => void;
}

export const useQuestionStore = create<QuestionState>((set, get) => ({
  topicId: null,
  phase: "practice",
  items: [],
  index: 0,
  sessionCorrect: 0,
  hintsUsedThisQuestion: 0,
  reset: (topicId, phase, items) =>
    set({
      topicId,
      phase,
      items,
      index: 0,
      sessionCorrect: 0,
      hintsUsedThisQuestion: 0,
    }),
  next: () => set({ index: get().index + 1, hintsUsedThisQuestion: 0 }),
  incCorrect: () => set({ sessionCorrect: get().sessionCorrect + 1 }),
  setHintsUsed: (n) => set({ hintsUsedThisQuestion: n }),
}));
