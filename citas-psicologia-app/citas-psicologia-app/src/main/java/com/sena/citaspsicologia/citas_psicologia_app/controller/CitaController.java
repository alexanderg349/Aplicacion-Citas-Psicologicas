package com.sena.citaspsicologia.citas_psicologia_app.controller;

import java.util.List;

import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.sena.citaspsicologia.citas_psicologia_app.dto.CitaRequestDTO;
import com.sena.citaspsicologia.citas_psicologia_app.model.Cita;
import com.sena.citaspsicologia.citas_psicologia_app.model.EstadoCita;
import com.sena.citaspsicologia.citas_psicologia_app.service.CitaService;

import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping("/api/citas")
@CrossOrigin(origins = "http://localhost:5173")
@RequiredArgsConstructor
public class CitaController {

    private final CitaService citaService;

    @GetMapping
    public List<Cita> listarTodas() {
        return citaService.listarTodas();
    }

    @GetMapping("/paciente/{id}")
    public List<Cita> listarPorPaciente(@PathVariable Long id) {
        return citaService.listarPorPaciente(id);
    }

    @GetMapping("/psicologo/{id}")
    public List<Cita> listarPorPsicologo(@PathVariable Long id) {
        return citaService.listarPorPsicologo(id);
    }

    @PostMapping
    public Cita crear(@RequestBody CitaRequestDTO request) {
        return citaService.crear(request);
    }

    @PutMapping("/{id}/estado")
    public Cita actualizarEstado(@PathVariable Long id, @RequestParam EstadoCita estado) {
        return citaService.actualizarEstado(id, estado);
    }
}
