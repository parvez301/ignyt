import { useEffect } from "react";
import api from "@/api/client";
import { useProgressStore } from "@/stores/progressStore";

export function useLoadProgress() {
  const { setMe } = useProgressStore();
  useEffect(() => {
    api
      .get("/users/me/progress")
      .then((r) => setMe(r.data))
      .catch(() => setMe(null));
  }, [setMe]);
}
