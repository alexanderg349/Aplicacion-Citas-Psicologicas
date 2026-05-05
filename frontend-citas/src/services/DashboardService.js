import api from "./api";

export const obtenerResumenAdmin = () => api.get("/admin/resumen");
export const obtenerResumenPaciente = (pacienteId) => api.get(`/pacientes/${pacienteId}/resumen`);
export const obtenerAgendaPsicologo = (psicologoId) => api.get(`/psicologos/${psicologoId}/agenda`);
export const obtenerPacientesPsicologo = (psicologoId) => api.get(`/psicologos/${psicologoId}/pacientes`);
export const obtenerHistoriaPaciente = (psicologoId, pacienteId) => api.get(`/psicologos/${psicologoId}/pacientes/${pacienteId}/historia`);
export const guardarHistoriaPaciente = (psicologoId, pacienteId, payload) => api.post(`/psicologos/${psicologoId}/pacientes/${pacienteId}/historia`, payload);
export const agregarEvolucionPaciente = (psicologoId, pacienteId, payload) => api.post(`/psicologos/${psicologoId}/pacientes/${pacienteId}/evoluciones`, payload);
