import { useMemo } from "react";
import { renderMathHtml } from "@/utils/katex";

export function MathBlock({ html }: { html: string }) {
  const inner = useMemo(() => ({ __html: renderMathHtml(html) }), [html]);
  return <div className="prose prose-invert max-w-none text-[var(--text-primary)]" dangerouslySetInnerHTML={inner} />;
}
