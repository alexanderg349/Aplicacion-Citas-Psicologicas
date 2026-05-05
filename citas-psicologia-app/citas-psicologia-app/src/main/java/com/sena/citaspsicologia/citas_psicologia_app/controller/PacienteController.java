package com.sena.citaspsicologia.citas_psicologia_app.controller;

import java.util.LinkedHashMap;
import java.util.Map;

import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.sena.citaspsicologia.citas_psicologia_app.service.CitaService;
import com.sena.citaspsicologia.citas_psicologia_app.service.HistoriaClinicaService;

import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping("/api/pacientes")
@CrossOrigin(origins = "http://localhost:5173")
@RequiredArgsConstructor
public class PacienteController {

    private final CitaService citaService;
    private final HistoriaClinicaService historiaClinicaService;

    @GetMapping("/{pacienteId}/resumen")
    public Map<String, Object> resumen(@PathVariable Long pacienteId) {
        Map<String, Object> data = new LinkedHashMap<>();
        data.put("citas", citaService.listarPorPaciente(pacienteId));
        try {
            data.put("historia", historiaClinicaService.obtenerHistoriaCompleta(pacienteId));
        } catch (Exception ex) {
            data.put("historia", null);
        }
        return data;
    }
}
