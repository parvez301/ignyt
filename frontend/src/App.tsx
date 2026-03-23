import { useEffect } from "react";
import { BrowserRouter } from "react-router-dom";
import { AppRouter } from "@/router";
import { useThemeStore } from "@/stores/themeStore";

export default function App() {
  const applyDom = useThemeStore((s) => s.applyDom);

  useEffect(() => {
    applyDom();
  }, [applyDom]);

  return (
    <BrowserRouter>
      <AppRouter />
    </BrowserRouter>
  );
}
