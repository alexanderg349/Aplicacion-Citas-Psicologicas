package com.sena.citaspsicologia.citas_psicologia_app.service;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import com.sena.citaspsicologia.citas_psicologia_app.dto.EvolucionClinicaRequest;
import com.sena.citaspsicologia.citas_psicologia_app.dto.HistoriaClinicaRequest;
import com.sena.citaspsicologia.citas_psicologia_app.model.Cita;
import com.sena.citaspsicologia.citas_psicologia_app.model.EvolucionClinica;
import com.sena.citaspsicologia.citas_psicologia_app.model.HistoriaClinica;
import com.sena.citaspsicologia.citas_psicologia_app.model.RolUsuario;
import com.sena.citaspsicologia.citas_psicologia_app.model.Usuario;
import com.sena.citaspsicologia.citas_psicologia_app.repository.CitaRepository;
import com.sena.citaspsicologia.citas_psicologia_app.repository.EvolucionClinicaRepository;
import com.sena.citaspsicologia.citas_psicologia_app.repository.HistoriaClinicaRepository;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class HistoriaClinicaService {

    private final HistoriaClinicaRepository historiaClinicaRepository;
    private final EvolucionClinicaRepository evolucionClinicaRepository;
    private final CitaRepository citaRepository;
    private final UsuarioService usuarioService;

    public HistoriaClinica guardarHistoria(Long pacienteId, HistoriaClinicaRequest request) {
        Usuario paciente = usuarioService.obtenerPorId(pacienteId);
        if (paciente.getRol() != RolUsuario.PACIENTE) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Solo se puede abrir historia clinica a pacientes.");
        }

        HistoriaClinica historia = historiaClinicaRepository.findByPacienteId(pacienteId)
                .orElse(HistoriaClinica.builder().paciente(paciente).build());

        historia.setMotivoConsulta(request.getMotivoConsulta());
        historia.setAntecedentes(request.getAntecedentes());
        historia.setDiagnosticoInicial(request.getDiagnosticoInicial());
        historia.setPlanTratamiento(request.getPlanTratamiento());

        return historiaClinicaRepository.save(historia);
    }

    public Map<String, Object> obtenerHistoriaCompleta(Long pacienteId) {
        HistoriaClinica historia = historiaClinicaRepository.findByPacienteId(pacienteId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "El paciente aun no tiene historia clinica."));

        List<EvolucionClinica> evoluciones = evolucionClinicaRepository.findByHistoriaClinicaIdOrderByFechaRegistroDesc(historia.getId());

        Map<String, Object> respuesta = new LinkedHashMap<>();
        respuesta.put("historia", historia);
        respuesta.put("evoluciones", evoluciones);
        return respuesta;
    }

    public EvolucionClinica agregarEvolucion(Long pacienteId, Long psicologoId, EvolucionClinicaRequest request) {
        HistoriaClinica historia = historiaClinicaRepository.findByPacienteId(pacienteId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Primero debes crear la historia clinica."));
        Usuario psicologo = usuarioService.obtenerPorId(psicologoId);
        if (psicologo.getRol() != RolUsuario.PSICOLOGO) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "El profesional debe tener rol PSICOLOGO.");
        }

        Cita cita = null;
        if (request.getCitaId() != null) {
            cita = citaRepository.findById(request.getCitaId())
                    .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Cita no encontrada."));
        }

        return evolucionClinicaRepository.save(EvolucionClinica.builder()
                .historiaClinica(historia)
                .psicologo(psicologo)
                .cita(cita)
                .resumenSesion(request.getResumenSesion())
                .observaciones(request.getObservaciones())
                .recomendaciones(request.getRecomendaciones())
                .build());
    }
}
