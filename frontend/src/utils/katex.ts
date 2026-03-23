import katex from "katex";
import "katex/dist/katex.min.css";

export function renderMathHtml(html: string): string {
  if (!html) return "";

  // Seeded/backend content can arrive with one extra escaping layer
  // (e.g. "\\(" and "\\mathbb"), so normalize before rendering.
  const normalized = html.replace(/\\\\/g, "\\");

  const withInline = normalized.replace(/\\\(([\s\S]*?)\\\)/g, (_, expr) => {
    try {
      return katex.renderToString(expr.trim(), { throwOnError: false, displayMode: false });
    } catch {
      return _;
    }
  });

  return withInline.replace(/\\\[([\s\S]*?)\\\]/g, (_, expr) => {
    try {
      return katex.renderToString(expr.trim(), { throwOnError: false, displayMode: true });
    } catch {
      return _;
    }
  });
}
