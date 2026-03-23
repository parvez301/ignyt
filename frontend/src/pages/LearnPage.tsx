import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { ThemeToggle } from "@/components/common/ThemeToggle";
import { MathBlock } from "@/components/common/MathBlock";
import { renderMathHtml } from "@/utils/katex";
import api from "@/api/client";

export default function LearnPage() {
  const { topicId } = useParams();
  const nav = useNavigate();
  const [bundle, setBundle] = useState<{
    concept_cards: { id: string; title: string; content_html: string }[];
    worked_examples: { id: string; title: string; completed: boolean; steps_json: { step: number; content: string; explanation: string }[] }[];
    real_world_hook: string | null;
  } | null>(null);
  const [openStep, setOpenStep] = useState<Record<string, number>>({});

  async function loadLearnBundle(id: string) {
    const r = await api.get(`/topics/${id}/learn`);
    setBundle(r.data);
  }

  useEffect(() => {
    if (!topicId) return;
    loadLearnBundle(topicId);
  }, [topicId]);

  async function markWe(weId: string) {
    if (!topicId) return;
    await api.post(`/topics/${topicId}/worked-examples/${weId}/complete`);
    // Re-fetch from server to keep UI in sync with persisted state.
    await loadLearnBundle(topicId);
  }

  async function completeLearn() {
    if (!topicId) return;
    try {
      await api.post(`/topics/${topicId}/complete-phase`, { phase: "learn" });
      nav(`/practice/${topicId}`);
    } catch (e: unknown) {
      const d = (e as { response?: { data?: { detail?: string } } })?.response?.data?.detail;
      alert(d || "Finish all worked examples first.");
    }
  }

  if (!bundle) return <p className="p-6 text-[var(--text-secondary)]">Loading…</p>;

  return (
    <div className="mx-auto max-w-3xl p-6">
      <div className="mb-4 flex justify-between">
        <Link to="/" className="text-[var(--brand)]">
          ← Home
        </Link>
        <ThemeToggle />
      </div>
      {bundle.real_world_hook && (
        <div className="mb-6 rounded-2xl bg-[var(--brand)]/10 p-4 text-[var(--text-primary)]">
          <MathBlock html={bundle.real_world_hook} />
        </div>
      )}
      <h1 className="mb-4 text-xl font-bold text-[var(--text-primary)]">Learn</h1>
      {bundle.concept_cards.map((c) => (
        <section key={c.id} className="mb-6 rounded-2xl bg-[var(--bg-card)] p-4 shadow">
          <h2
            className="font-semibold text-[var(--text-primary)]"
            dangerouslySetInnerHTML={{ __html: renderMathHtml(c.title) }}
          />
          <MathBlock html={c.content_html} />
        </section>
      ))}
      {bundle.worked_examples.map((we) => (
        <section key={we.id} className="mb-6 rounded-2xl bg-[var(--bg-card)] p-4 shadow">
          <div className="flex items-center justify-between gap-3">
            <h2
              className="font-semibold text-[var(--text-primary)]"
              dangerouslySetInnerHTML={{ __html: renderMathHtml(we.title) }}
            />
            {we.completed && (
              <span className="rounded-full bg-emerald-500/20 px-2 py-1 text-xs font-semibold text-emerald-300">
                Done
              </span>
            )}
          </div>
          <ol className="mt-2 space-y-3">
            {we.steps_json.map((st) => (
              <li key={st.step}>
                <button
                  type="button"
                  className="text-left text-sm text-[var(--brand)]"
                  onClick={() =>
                    setOpenStep((o) => ({
                      ...o,
                      [we.id]: Math.max(o[we.id] || 0, st.step),
                    }))
                  }
                >
                  <span className="font-medium">Step {st.step}: </span>
                  <span dangerouslySetInnerHTML={{ __html: renderMathHtml(st.content) }} />
                </button>
                {(openStep[we.id] || 0) >= st.step && (
                  <div className="mt-1 text-sm text-[var(--text-secondary)]">
                    <span dangerouslySetInnerHTML={{ __html: renderMathHtml(st.explanation) }} />
                  </div>
                )}
              </li>
            ))}
          </ol>
          <button
            type="button"
            disabled={we.completed}
            className={`mt-3 rounded-lg px-4 py-2 text-sm text-white ${
              we.completed ? "cursor-not-allowed bg-slate-500/70" : "bg-[var(--success)]"
            }`}
            onClick={() => markWe(we.id)}
          >
            {we.completed ? "Completed" : "Mark example done"}
          </button>
        </section>
      ))}
      <button
        type="button"
        onClick={completeLearn}
        className="inline-block rounded-xl bg-[var(--brand)] px-6 py-3 font-medium text-white"
      >
        Complete learn &amp; unlock practice
      </button>
    </div>
  );
}
