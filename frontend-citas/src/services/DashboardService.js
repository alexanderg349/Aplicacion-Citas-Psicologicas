import api from "./api";

export const obtenerResumenAdmin = () => api.get("/admin/summary");
export const crearUsuarioDesdeAdmin = (payload) => api.post("/admin/users", payload);
export const obtenerResumenPaciente = () => api.get("/patients/me/summary");
export const obtenerAgendaPsicologo = () => api.get("/psychologists/me/agenda");
export const obtenerPacientesPsicologo = () => api.get("/psychologists/me/patients");
export const obtenerHistoriaPaciente = (pacienteId) => api.get(`/psychologists/me/patients/${pacienteId}/history`);
export const guardarHistoriaPaciente = (pacienteId, payload) => api.put(`/psychologists/me/patients/${pacienteId}/history`, payload);
export const agregarEvolucionPaciente = (pacienteId, payload) => api.post(`/psychologists/me/patients/${pacienteId}/evolutions`, payload);
