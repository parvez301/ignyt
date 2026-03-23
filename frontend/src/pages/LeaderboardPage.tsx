import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { ThemeToggle } from "@/components/common/ThemeToggle";
import api from "@/api/client";

interface Row {
  rank: number;
  display_name: string;
  total_xp: number;
  level: number;
}

export default function LeaderboardPage() {
  const [rows, setRows] = useState<Row[]>([]);

  useEffect(() => {
    api.get("/leaderboard", { params: { page: 1, per_page: 20 } }).then((r) => setRows(r.data.items));
  }, []);

  return (
    <div className="mx-auto max-w-2xl p-6">
      <div className="mb-4 flex justify-between">
        <Link to="/" className="text-[var(--brand)]">
          ← Home
        </Link>
        <ThemeToggle />
      </div>
      <h1 className="mb-4 text-2xl font-bold text-[var(--text-primary)]">Leaderboard</h1>
      <table className="w-full text-left text-sm">
        <thead>
          <tr className="text-[var(--text-secondary)]">
            <th className="pb-2">#</th>
            <th className="pb-2">Learner</th>
            <th className="pb-2">XP</th>
            <th className="pb-2">Level</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r) => (
            <tr key={r.rank} className="border-t border-[var(--bg-surface)] text-[var(--text-primary)]">
              <td className="py-2">{r.rank}</td>
              <td className="py-2">{r.display_name}</td>
              <td className="py-2">{r.total_xp}</td>
              <td className="py-2">{r.level}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
