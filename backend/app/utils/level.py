THRESHOLDS = [0, 100, 250, 500, 1000, 2000, 3500, 5500, 8000, 12000]


def level_from_xp(total_xp: int) -> int:
    for lvl in range(len(THRESHOLDS) - 1, -1, -1):
        if total_xp >= THRESHOLDS[lvl]:
            return lvl + 1
    return 1
