import { useEffect } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { ThemeToggle } from "@/components/common/ThemeToggle";
import { QuestionScreen } from "@/components/practice/QuestionScreen";
import api from "@/api/client";
import { useQuestionStore } from "@/stores/questionStore";
import { scorePercent } from "@/utils/score";

export default function PracticePage() {
  const { topicId } = useParams();
  const nav = useNavigate();
  const { items, index, reset, next, incCorrect } = useQuestionStore();

  useEffect(() => {
    if (!topicId) return;
    api.post(`/topics/${topicId}/questions`, { phase: "practice", count: 5 }).then((r) => {
      reset(topicId, "practice", r.data);
    });
  }, [topicId, reset]);

  const current = items[index];
  const total = items.length;

  return (
    <div className="mx-auto max-w-3xl p-6">
      <div className="mb-4 flex justify-between">
        <Link to="/" className="text-[var(--brand)]">
          ← Home
        </Link>
        <ThemeToggle />
      </div>
      <p className="mb-2 text-sm text-[var(--text-secondary)]">
        Practice · Question {total ? Math.min(index + 1, total) : "…"} of {total || "…"}
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
                state: { phase: "practice", correct, total: t, score: scorePercent(correct, t) },
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
