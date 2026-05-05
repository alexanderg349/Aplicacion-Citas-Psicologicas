package com.sena.citaspsicologia.citas_psicologia_app.service;

import java.util.List;

import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import com.sena.citaspsicologia.citas_psicologia_app.dto.CitaRequestDTO;
import com.sena.citaspsicologia.citas_psicologia_app.model.Cita;
import com.sena.citaspsicologia.citas_psicologia_app.model.EstadoCita;
import com.sena.citaspsicologia.citas_psicologia_app.model.RolUsuario;
import com.sena.citaspsicologia.citas_psicologia_app.model.Usuario;
import com.sena.citaspsicologia.citas_psicologia_app.repository.CitaRepository;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class CitaService {

    private final CitaRepository citaRepository;
    private final UsuarioService usuarioService;
    private final WhatsappService whatsappService;

    public List<Cita> listarTodas() {
        return citaRepository.findAll();
    }

    public List<Cita> listarPorPaciente(Long pacienteId) {
        return citaRepository.findByPacienteIdOrderByFechaHoraAsc(pacienteId);
    }

    public List<Cita> listarPorPsicologo(Long psicologoId) {
        return citaRepository.findByPsicologoIdOrderByFechaHoraAsc(psicologoId);
    }

    public Cita crear(CitaRequestDTO request) {
        Usuario paciente = usuarioService.obtenerPorId(request.getPacienteId());
        Usuario psicologo = usuarioService.obtenerPorId(request.getPsicologoId());
        validarRoles(paciente, psicologo);

        Cita cita = citaRepository.save(Cita.builder()
                .paciente(paciente)
                .psicologo(psicologo)
                .fechaHora(request.getFechaHora())
                .motivo(request.getMotivo())
                .observaciones(request.getObservaciones())
                .estado(request.getEstado() == null ? EstadoCita.PROGRAMADA : request.getEstado())
                .build());

        whatsappService.registrarEvento(cita, "CITA_CREADA");
        return cita;
    }

    public Cita actualizarEstado(Long citaId, EstadoCita estado) {
        Cita cita = citaRepository.findById(citaId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Cita no encontrada."));
        cita.setEstado(estado);
        Cita actualizada = citaRepository.save(cita);
        whatsappService.registrarEvento(actualizada, "CAMBIO_ESTADO");
        return actualizada;
    }

    private void validarRoles(Usuario paciente, Usuario psicologo) {
        if (paciente.getRol() != RolUsuario.PACIENTE) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "El usuario asignado como paciente no tiene rol PACIENTE.");
        }
        if (psicologo.getRol() != RolUsuario.PSICOLOGO) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "El usuario asignado como psicologo no tiene rol PSICOLOGO.");
        }
    }
}
