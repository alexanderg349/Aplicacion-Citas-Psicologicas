package com.sena.citaspsicologia.citas_psicologia_app.controller;

import java.util.LinkedHashMap;
import java.util.Map;

import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.sena.citaspsicologia.citas_psicologia_app.model.RolUsuario;
import com.sena.citaspsicologia.citas_psicologia_app.service.CitaService;
import com.sena.citaspsicologia.citas_psicologia_app.service.UsuarioService;

import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping("/api/admin")
@CrossOrigin(origins = "http://localhost:5173")
@RequiredArgsConstructor
public class AdminController {

    private final UsuarioService usuarioService;
    private final CitaService citaService;

    @GetMapping("/resumen")
    public Map<String, Object> resumen() {
        Map<String, Object> data = new LinkedHashMap<>();
        data.put("usuarios", usuarioService.listarTodos());
        data.put("totalPacientes", usuarioService.listarPorRol(RolUsuario.PACIENTE).size());
        data.put("totalPsicologos", usuarioService.listarPorRol(RolUsuario.PSICOLOGO).size());
        data.put("totalAdministradores", usuarioService.listarPorRol(RolUsuario.ADMINISTRADOR).size());
        data.put("totalCitas", citaService.listarTodas().size());
        return data;
    }
}
