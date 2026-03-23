import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { motion } from "framer-motion";
import { ThemeToggle } from "@/components/common/ThemeToggle";
import api from "@/api/client";

interface SectionNode {
  id: string;
  name: string;
  section_number: string | null;
  order: number;
  status: string;
  stars_earned: number;
  stars_possible: number;
}

export default function ChapterMapPage() {
  const { chapterId } = useParams();
  const [sections, setSections] = useState<SectionNode[]>([]);
  const [topicsBySection, setTopicsBySection] = useState<Record<string, { id: string; name: string; phase: string; stars: number }[]>>({});

  useEffect(() => {
    if (!chapterId) return;
    api.get(`/chapters/${chapterId}/map`).then((r) => setSections(r.data.sections));
  }, [chapterId]);

  useEffect(() => {
    async function loadTopics() {
      const map: Record<string, { id: string; name: string; phase: string; stars: number }[]> = {};
      for (const s of sections) {
        const res = await api.get(`/sections/${s.id}/topics`, { params: { per_page: 50 } });
        const tlist = res.data.items.map((t: { id: string; name: string }) => ({
          id: t.id,
          name: t.name,
          phase: "…",
          stars: 0,
        }));
        map[s.id] = tlist;
      }
      if (chapterId) {
        const prog = await api.get(`/users/me/progress/chapter/${chapterId}`);
        for (const sec of prog.data.sections) {
          map[sec.section_id] = sec.topics.map(
            (t: { topic_id: string; name: string; phase: string; stars: number }) => ({
              id: t.topic_id,
              name: t.name,
              phase: t.phase,
              stars: t.stars,
            }),
          );
        }
      }
      setTopicsBySection(map);
    }
    if (sections.length) loadTopics();
  }, [sections, chapterId]);

  return (
    <div className="mx-auto max-w-3xl p-6">
      <div className="mb-6 flex justify-between">
        <Link to="/" className="text-[var(--brand)]">
          ← Home
        </Link>
        <ThemeToggle />
      </div>
      <h1 className="mb-8 text-2xl font-bold text-[var(--text-primary)]">Chapter quest path</h1>
      <div className="flex flex-col gap-6">
        {sections.map((s, i) => (
          <motion.div
            key={s.id}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.05 }}
            className={`rounded-2xl border p-4 ${
              s.status === "completed"
                ? "border-emerald-500/40 bg-emerald-500/5"
                : s.status === "in_progress"
                  ? "border-[var(--brand)] shadow-[0_0_20px_rgba(99,102,241,0.25)]"
                  : "border-[var(--bg-surface)] opacity-60"
            }`}
          >
            <div className="mb-2 flex justify-between">
              <h2 className="font-semibold text-[var(--text-primary)]">
                {s.section_number} {s.name}
              </h2>
              <span className="text-sm text-[var(--text-secondary)]">
                ⭐ {s.stars_earned}/{s.stars_possible}
              </span>
            </div>
            <ul className="space-y-2">
              {(topicsBySection[s.id] || []).map((t) => (
                <li key={t.id} className="grid grid-cols-[minmax(0,1fr)_auto] items-start gap-x-3 gap-y-1 text-sm">
                  <span className="text-[var(--text-primary)]">{t.name}</span>
                  <div className="flex flex-col items-end gap-1">
                    <span className="whitespace-nowrap text-[var(--text-secondary)]">
                      {t.phase} · {t.stars}★
                    </span>
                    <div className="flex flex-col items-end gap-1">
                      <Link className="text-[var(--brand)]" to={`/learn/${t.id}`}>
                        Learn
                      </Link>
                      <Link className="text-[var(--brand)]" to={`/practice/${t.id}`}>
                        Practice
                      </Link>
                      <Link className="text-[var(--brand)]" to={`/master/${t.id}`}>
                        Master
                      </Link>
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
