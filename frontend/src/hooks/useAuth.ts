import { useAuthStore } from "@/stores/authStore";

export function useAuth() {
  const { token, user, logout } = useAuthStore();
  return { isAuthed: !!token, user, logout };
}
