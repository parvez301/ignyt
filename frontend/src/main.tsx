import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import { useThemeStore } from "@/stores/themeStore";
import "./index.css";

useThemeStore.persist.onFinishHydration(() => {
  useThemeStore.getState().applyDom();
});

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
