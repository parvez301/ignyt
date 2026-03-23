import { Link } from "react-router-dom";
import { ThemeToggle } from "@/components/common/ThemeToggle";

export default function DailyChallengePage() {
  return (
    <div className="mx-auto max-w-lg p-6">
      <div className="mb-4 flex justify-between">
        <Link to="/" className="text-[var(--brand)]">
          ← Home
        </Link>
        <ThemeToggle />
      </div>
      <p className="text-[var(--text-secondary)]">Daily challenge arrives in Phase 2 — stay tuned!</p>
    </div>
  );
}
