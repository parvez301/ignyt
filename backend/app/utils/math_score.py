from decimal import ROUND_HALF_UP, Decimal


def score_percent(correct: int, total: int) -> int:
    """score = correct/total * 100, half-up (ties round up)."""
    if total <= 0:
        return 0
    q = (Decimal(correct) * Decimal(100) / Decimal(total)).quantize(
        Decimal("1"), rounding=ROUND_HALF_UP
    )
    return int(q)


def stars_for_phase(phase: str, score: int) -> int:
    """Server-side star count for a single phase completion (not cumulative max)."""
    if phase == "practice":
        if score >= 80:
            return 2
        return 1
    if phase == "master":
        if score >= 90:
            return 3
        if score >= 80:
            return 2
        return 1
    return 0
