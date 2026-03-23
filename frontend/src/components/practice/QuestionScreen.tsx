import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { MathBlock } from "@/components/common/MathBlock";
import type { GeneratedQuestionItem } from "@/types";
import api from "@/api/client";

interface Props {
  item: GeneratedQuestionItem;
  onChecked: (payload: { correct: boolean; xp: number; misconception?: string | null }) => void;
  onHintCount: (n: number) => void;
  onNext: () => void;
}

export function QuestionScreen({ item, onChecked, onHintCount, onNext }: Props) {
  const [answer, setAnswer] = useState("");
  const [feedback, setFeedback] = useState<{
    kind: "hint" | "result";
    correct: boolean;
    msg: string;
    xp: number;
  } | null>(null);
  const [loading, setLoading] = useState(false);

  async function submit() {
    setLoading(true);
    try {
      const { data } = await api.post(`/questions/${item.generated_question_id}/check`, {
        user_answer: answer,
      });
      setFeedback({
        kind: "result",
        correct: data.is_correct,
        msg: data.is_correct
          ? "Nice work — you nailed it!"
          : data.misconception_explanation || "Almost! Take another look with the hint below.",
        xp: data.xp_earned,
      });
      onChecked({ correct: data.is_correct, xp: data.xp_earned, misconception: data.misconception_explanation });
    } catch {
      setFeedback({ kind: "result", correct: false, msg: "Something went wrong. Try again.", xp: 0 });
    } finally {
      setLoading(false);
    }
  }

  async function takeHint(n: number) {
    try {
      const { data } = await api.post(`/questions/${item.generated_question_id}/hint`, {
        hint_number: n,
      });
      onHintCount(n);
      setFeedback({
        kind: "hint",
        correct: false,
        msg: data.hint_text,
        xp: 0,
      });
    } catch {
      /* ignore */
    }
  }

  const isMcq = item.type === "mcq" && Array.isArray(item.options);
  const isTf = item.type === "true_false" && Array.isArray(item.options);
  const isDrag = item.type === "drag_drop";

  return (
    <div className="flex min-h-[60vh] flex-col gap-6">
      <motion.div layout className="rounded-2xl bg-[var(--bg-card)] p-6 shadow-md">
        <MathBlock html={item.question_html} />
        {isMcq || isTf ? (
          <div className="mt-4 grid gap-2">
            {(item.options as string[]).map((opt) => (
              <button
                key={opt}
                type="button"
                onClick={() => setAnswer(opt)}
                className={`rounded-xl border px-4 py-3 text-left transition ${
                  answer === opt
                    ? "border-[var(--brand)] bg-[var(--bg-surface)]"
                    : "border-transparent bg-[var(--bg-primary)]"
                }`}
              >
                <MathBlock html={opt} />
              </button>
            ))}
          </div>
        ) : isDrag ? (
          <textarea
            className="mt-4 min-h-[100px] w-full rounded-xl border border-[var(--bg-surface)] bg-[var(--bg-primary)] px-4 py-3 font-mono text-sm text-[var(--text-primary)]"
            placeholder='Paste JSON mapping, e.g. {"3":"N","0":"W"}'
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
          />
        ) : (
          <input
            className="mt-4 w-full rounded-xl border border-[var(--bg-surface)] bg-[var(--bg-primary)] px-4 py-3 text-[var(--text-primary)]"
            placeholder="Your answer"
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
          />
        )}
        <div className="mt-4 flex flex-wrap gap-2">
          <button
            type="button"
            disabled={loading}
            onClick={() => takeHint(1)}
            className="rounded-lg bg-[var(--bg-surface)] px-4 py-2 text-sm text-[var(--text-primary)]"
          >
            Hint 1
          </button>
          <button
            type="button"
            disabled={loading}
            onClick={() => takeHint(2)}
            className="rounded-lg bg-[var(--bg-surface)] px-4 py-2 text-sm text-[var(--text-primary)]"
          >
            Hint 2
          </button>
          <button
            type="button"
            disabled={loading}
            onClick={() => takeHint(3)}
            className="rounded-lg bg-[var(--bg-surface)] px-4 py-2 text-sm text-[var(--text-primary)]"
          >
            Hint 3
          </button>
          <button
            type="button"
            disabled={loading || !answer}
            onClick={submit}
            className="ml-auto rounded-xl bg-[var(--brand)] px-6 py-2 font-medium text-white"
          >
            Check
          </button>
        </div>
      </motion.div>
      <AnimatePresence>
        {feedback && (
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className={`rounded-xl p-4 ${
              feedback.correct ? "bg-emerald-500/10 text-emerald-700 dark:text-emerald-300" : "bg-amber-500/10 text-amber-900 dark:text-amber-100"
            }`}
          >
            <p className="font-medium">{feedback.correct ? "Great job!" : "Keep going!"}</p>
            <p className="mt-1 text-sm">{feedback.msg}</p>
            {feedback.kind === "result" && feedback.correct && feedback.xp > 0 && (
              <p className="mt-2 text-sm text-[var(--text-secondary)]">+{feedback.xp} XP</p>
            )}
            {feedback.kind === "hint" && (
              <button
                type="button"
                className="mt-4 rounded-xl bg-[var(--bg-surface)] px-4 py-2 text-sm font-medium text-[var(--text-primary)]"
                onClick={() => setFeedback(null)}
              >
                Got it
              </button>
            )}
            {feedback.kind === "result" && (
              <button
                type="button"
                className="mt-4 rounded-xl bg-[var(--brand)] px-4 py-2 text-sm font-medium text-white"
                onClick={() => {
                  setFeedback(null);
                  setAnswer("");
                  onNext();
                }}
              >
                Next question
              </button>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
