import api from "./api";

export const loginUsuario = (credenciales) => api.post("/auth/login", credenciales);
export const registrarUsuario = (datosUsuario) => api.post("/auth/registro", datosUsuario);
export const listarUsuarios = () => api.get("/auth/usuarios");
