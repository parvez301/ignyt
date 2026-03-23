import { Link } from "react-router-dom";
import { ThemeToggle } from "@/components/common/ThemeToggle";

export default function ReviewPage() {
  return (
    <div className="mx-auto max-w-lg p-6">
      <div className="mb-4 flex justify-between">
        <Link to="/" className="text-[var(--brand)]">
          ← Home
        </Link>
        <ThemeToggle />
      </div>
      <p className="text-[var(--text-secondary)]">Review queue is part of Phase 2.</p>
    </div>
  );
}
