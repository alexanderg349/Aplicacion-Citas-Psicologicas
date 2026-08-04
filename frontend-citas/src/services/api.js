import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1",
});

api.interceptors.request.use((config) => {
  const saved = localStorage.getItem("usuario-sesion");
  if (saved) {
    const session = JSON.parse(saved);
    if (session?.access_token) {
      config.headers.Authorization = `Bearer ${session.access_token}`;
    }
  }
  return config;
});

export default api;
