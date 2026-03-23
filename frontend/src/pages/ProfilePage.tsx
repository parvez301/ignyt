import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { ThemeToggle } from "@/components/common/ThemeToggle";
import api from "@/api/client";
import { useAuthStore } from "@/stores/authStore";

interface Badge {
  id: string;
  name: string;
  description: string | null;
}

export default function ProfilePage() {
  const user = useAuthStore((s) => s.user);
  const [badges, setBadges] = useState<Badge[]>([]);

  useEffect(() => {
    api.get("/users/me/badges").then((r) => setBadges(r.data));
  }, []);

  return (
    <div className="mx-auto max-w-2xl p-6">
      <div className="mb-4 flex justify-between">
        <Link to="/" className="text-[var(--brand)]">
          ← Home
        </Link>
        <ThemeToggle />
      </div>
      <h1 className="text-2xl font-bold text-[var(--text-primary)]">{user?.display_name}</h1>
      <p className="text-[var(--text-secondary)]">
        @{user?.username} · Level {user?.level} · {user?.total_xp} XP
      </p>
      <h2 className="mt-8 font-semibold text-[var(--text-primary)]">Badges</h2>
      <ul className="mt-2 space-y-2">
        {badges.map((b) => (
          <li key={b.id} className="rounded-xl bg-[var(--bg-card)] p-3 text-[var(--text-primary)] shadow">
            <strong>{b.name}</strong>
            {b.description && <p className="text-sm text-[var(--text-secondary)]">{b.description}</p>}
          </li>
        ))}
        {badges.length === 0 && <li className="text-[var(--text-secondary)]">No badges yet — keep learning!</li>}
      </ul>
    </div>
  );
}
