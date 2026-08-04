import api from "./api";

export const loginUsuario = (credenciales) => api.post("/auth/login", credenciales);
export const registrarUsuario = (datosUsuario) => api.post("/auth/register", datosUsuario);
export const obtenerSesionActual = () => api.get("/auth/me");
export const listarPsicologos = () => api.get("/users/psychologists");
