import { useEffect, useState } from "react";
import { Link, useLocation, useNavigate, useParams } from "react-router-dom";
import { motion } from "framer-motion";
import { ThemeToggle } from "@/components/common/ThemeToggle";
import api from "@/api/client";

export default function ResultsPage() {
  const { topicId } = useParams();
  const loc = useLocation();
  const nav = useNavigate();
  const state = loc.state as {
    phase: "practice" | "master";
    correct: number;
    total: number;
    score: number;
    seconds?: number;
  } | null;
  const phase = state?.phase;
  const score = state?.score;
  const [done, setDone] = useState<{
    new_phase: string;
    stars: number;
    xp_earned: number;
  } | null>(null);
  const [phaseErr, setPhaseErr] = useState<string | null>(null);

  useEffect(() => {
    if (!topicId || !phase || score === undefined) {
      nav("/");
      return;
    }
    if ((phase === "practice" || phase === "master") && score < 50) {
      setPhaseErr("You need at least 50% to complete this phase — try another round!");
      return;
    }
    api
      .post(`/topics/${topicId}/complete-phase`, { phase, score })
      .then((r) => setDone(r.data))
      .catch((e: { response?: { data?: { detail?: string } } }) => {
        setPhaseErr(String(e.response?.data?.detail || "Could not update progress."));
      });
  }, [topicId, phase, score, nav]);

  if (!state) return null;

  return (
    <div className="mx-auto max-w-lg p-6 text-center">
      <div className="mb-4 flex justify-end">
        <ThemeToggle />
      </div>
      <motion.h1
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        className="text-2xl font-bold text-[var(--text-primary)]"
      >
        Session complete!
      </motion.h1>
      <p className="mt-2 text-[var(--text-secondary)]">
        You got {state.correct} / {state.total} — that is about {state.score}%.
      </p>
      {done && (
        <p className="mt-4 text-lg text-[var(--text-primary)]">
          ⭐ Stars: {done.stars} · +{done.xp_earned} XP · Phase: {done.new_phase}
        </p>
      )}
      {phaseErr && <p className="mt-4 text-amber-700 dark:text-amber-300">{phaseErr}</p>}
      <Link to="/" className="mt-8 inline-block rounded-xl bg-[var(--brand)] px-6 py-3 font-medium text-white">
        Back home
      </Link>
    </div>
  );
}
