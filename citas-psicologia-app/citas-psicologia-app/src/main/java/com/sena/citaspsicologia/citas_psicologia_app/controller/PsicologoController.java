package com.sena.citaspsicologia.citas_psicologia_app.controller;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.sena.citaspsicologia.citas_psicologia_app.dto.EvolucionClinicaRequest;
import com.sena.citaspsicologia.citas_psicologia_app.dto.HistoriaClinicaRequest;
import com.sena.citaspsicologia.citas_psicologia_app.model.Cita;
import com.sena.citaspsicologia.citas_psicologia_app.model.Usuario;
import com.sena.citaspsicologia.citas_psicologia_app.service.CitaService;
import com.sena.citaspsicologia.citas_psicologia_app.service.HistoriaClinicaService;

import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping("/api/psicologos")
@CrossOrigin(origins = "http://localhost:5173")
@RequiredArgsConstructor
public class PsicologoController {

    private final CitaService citaService;
    private final HistoriaClinicaService historiaClinicaService;

    @GetMapping("/{psicologoId}/agenda")
    public List<Cita> agenda(@PathVariable Long psicologoId) {
        return citaService.listarPorPsicologo(psicologoId);
    }

    @GetMapping("/{psicologoId}/pacientes")
    public List<Usuario> pacientes(@PathVariable Long psicologoId) {
        return citaService.listarPorPsicologo(psicologoId).stream()
                .map(Cita::getPaciente)
                .collect(Collectors.toMap(Usuario::getId, paciente -> paciente, (actual, ignorado) -> actual, LinkedHashMap::new))
                .values()
                .stream()
                .toList();
    }

    @GetMapping("/{psicologoId}/pacientes/{pacienteId}/historia")
    public Map<String, Object> historiaCompleta(@PathVariable Long psicologoId, @PathVariable Long pacienteId) {
        Map<String, Object> respuesta = new LinkedHashMap<>();
        respuesta.put("agenda", citaService.listarPorPsicologo(psicologoId).stream()
                .filter(cita -> cita.getPaciente().getId().equals(pacienteId))
                .toList());
        respuesta.putAll(historiaClinicaService.obtenerHistoriaCompleta(pacienteId));
        return respuesta;
    }

    @PostMapping("/{psicologoId}/pacientes/{pacienteId}/historia")
    public Object guardarHistoria(@PathVariable Long psicologoId, @PathVariable Long pacienteId, @RequestBody HistoriaClinicaRequest request) {
        return historiaClinicaService.guardarHistoria(pacienteId, request);
    }

    @PostMapping("/{psicologoId}/pacientes/{pacienteId}/evoluciones")
    public Object agregarEvolucion(@PathVariable Long psicologoId, @PathVariable Long pacienteId, @RequestBody EvolucionClinicaRequest request) {
        return historiaClinicaService.agregarEvolucion(pacienteId, psicologoId, request);
    }
}
