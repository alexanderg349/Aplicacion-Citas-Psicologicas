import api from "./api";

export const listarCitas = () => api.get("/citas");
export const listarCitasPaciente = (pacienteId) => api.get(`/citas/paciente/${pacienteId}`);
export const listarCitasPsicologo = (psicologoId) => api.get(`/citas/psicologo/${psicologoId}`);
export const guardarCita = (cita) => api.post("/citas", cita);
export const actualizarEstadoCita = (id, estado) => api.put(`/citas/${id}/estado`, null, { params: { estado } });
