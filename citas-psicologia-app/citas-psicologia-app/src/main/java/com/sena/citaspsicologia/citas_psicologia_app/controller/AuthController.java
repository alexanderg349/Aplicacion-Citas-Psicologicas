package com.sena.citaspsicologia.citas_psicologia_app.controller;

import java.util.LinkedHashMap;
import java.util.Map;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

import com.sena.citaspsicologia.citas_psicologia_app.dto.LoginRequest;
import com.sena.citaspsicologia.citas_psicologia_app.dto.RegisterRequest;
import com.sena.citaspsicologia.citas_psicologia_app.model.Usuario;
import com.sena.citaspsicologia.citas_psicologia_app.service.UsuarioService;

import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping("/api/auth")
@CrossOrigin(origins = "http://localhost:5173")
@RequiredArgsConstructor
public class AuthController {

    private final UsuarioService usuarioService;

    @PostMapping("/registro")
    @ResponseStatus(HttpStatus.CREATED)
    public Map<String, Object> registrar(@RequestBody RegisterRequest request) {
        Usuario usuario = usuarioService.registrar(request);
        return construirRespuesta(usuario);
    }

    @PostMapping("/login")
    public Map<String, Object> login(@RequestBody LoginRequest request) {
        Usuario usuario = usuarioService.autenticar(request);
        return construirRespuesta(usuario);
    }

    @GetMapping("/usuarios")
    public Iterable<Usuario> listarUsuarios() {
        return usuarioService.listarTodos();
    }

    private Map<String, Object> construirRespuesta(Usuario usuario) {
        Map<String, Object> response = new LinkedHashMap<>();
        response.put("id", usuario.getId());
        response.put("nombreCompleto", usuario.getNombre() + " " + usuario.getApellido());
        response.put("email", usuario.getEmail());
        response.put("telefono", usuario.getTelefono());
        response.put("rol", usuario.getRol());
        response.put("especialidad", usuario.getEspecialidad());
        return response;
    }
}
