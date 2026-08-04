import api from "./api";

export const guardarCita = (cita) => api.post("/patients/me/appointments", cita);
export const actualizarEstadoCita = (id, estado) => api.patch(`/appointments/${id}/status`, { estado });
