import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { ThemeToggle } from "@/components/common/ThemeToggle";
import { QuestionScreen } from "@/components/practice/QuestionScreen";
import api from "@/api/client";
import { useQuestionStore } from "@/stores/questionStore";
import { scorePercent } from "@/utils/score";

export default function MasterPage() {
  const { topicId } = useParams();
  const nav = useNavigate();
  const { items, index, reset, next, incCorrect } = useQuestionStore();
  const [seconds, setSeconds] = useState(0);

  useEffect(() => {
    if (!topicId) return;
    api.post(`/topics/${topicId}/questions`, { phase: "master", count: 5 }).then((r) => {
      reset(topicId, "master", r.data);
    });
  }, [topicId, reset]);

  useEffect(() => {
    const id = setInterval(() => setSeconds((s) => s + 1), 1000);
    return () => clearInterval(id);
  }, []);

  const current = items[index];
  const total = items.length;

  return (
    <div className="mx-auto max-w-3xl p-6">
      <div className="mb-4 flex justify-between">
        <Link to="/" className="text-[var(--brand)]">
          ← Home
        </Link>
        <div className="flex items-center gap-4">
          <span className="text-sm text-[var(--text-secondary)]">⏱ {seconds}s</span>
          <ThemeToggle />
        </div>
      </div>
      <p className="mb-2 text-sm text-[var(--text-secondary)]">
        Master · Question {total ? Math.min(index + 1, total) : "…"} of {total || "…"}
      </p>
      {current && topicId ? (
        <QuestionScreen
          item={current}
          onHintCount={() => {}}
          onChecked={({ correct }) => {
            if (correct) incCorrect();
          }}
          onNext={() => {
            const st = useQuestionStore.getState();
            if (st.index >= st.items.length - 1) {
              const correct = st.sessionCorrect;
              const t = st.items.length;
              nav(`/results/${topicId}`, {
                state: {
                  phase: "master",
                  correct,
                  total: t,
                  score: scorePercent(correct, t),
                  seconds,
                },
              });
            } else {
              next();
            }
          }}
        />
      ) : (
        <p className="text-[var(--text-secondary)]">Loading questions…</p>
      )}
    </div>
  );
}
