import axios from "axios";
import { useAuthStore } from "@/stores/authStore";

const api = axios.create({
  // Local dev can continue using Vite proxy (/api).
  // Vercel/production should set VITE_API_BASE_URL to the deployed backend URL.
  baseURL: import.meta.env.VITE_API_BASE_URL || "/api",
});

api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
