/** Half-up rounding, matches backend score_percent. */
export function scorePercent(correct: number, total: number): number {
  if (total <= 0) return 0;
  return Math.floor((correct * 100) / total + 0.5);
}
