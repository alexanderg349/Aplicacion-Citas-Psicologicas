package com.sena.citaspsicologia.citas_psicologia_app.service;

import java.util.List;

import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import com.sena.citaspsicologia.citas_psicologia_app.dto.LoginRequest;
import com.sena.citaspsicologia.citas_psicologia_app.dto.RegisterRequest;
import com.sena.citaspsicologia.citas_psicologia_app.model.RolUsuario;
import com.sena.citaspsicologia.citas_psicologia_app.model.Usuario;
import com.sena.citaspsicologia.citas_psicologia_app.repository.UsuarioRepository;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class UsuarioService {

    private final UsuarioRepository usuarioRepository;

    public Usuario registrar(RegisterRequest request) {
        usuarioRepository.findByEmail(request.getEmail()).ifPresent(usuario -> {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "El correo ya esta registrado.");
        });

        if (request.getRol() == RolUsuario.PSICOLOGO && (request.getEspecialidad() == null || request.getEspecialidad().isBlank())) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "El psicologo debe tener especialidad.");
        }

        Usuario usuario = Usuario.builder()
                .nombre(request.getNombre())
                .apellido(request.getApellido())
                .email(request.getEmail())
                .password(request.getPassword())
                .telefono(request.getTelefono())
                .rol(request.getRol())
                .especialidad(request.getRol() == RolUsuario.PSICOLOGO ? request.getEspecialidad() : null)
                .build();

        return usuarioRepository.save(usuario);
    }

    public Usuario autenticar(LoginRequest request) {
        Usuario usuario = usuarioRepository.findByEmail(request.getEmail())
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.UNAUTHORIZED, "Credenciales incorrectas."));

        if (!usuario.getPassword().equals(request.getPassword())) {
            throw new ResponseStatusException(HttpStatus.UNAUTHORIZED, "Credenciales incorrectas.");
        }

        return usuario;
    }

    public Usuario obtenerPorId(Long id) {
        return usuarioRepository.findById(id)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Usuario no encontrado."));
    }

    public List<Usuario> listarPorRol(RolUsuario rol) {
        return usuarioRepository.findByRolOrderByNombreAsc(rol);
    }

    public List<Usuario> listarTodos() {
        return usuarioRepository.findAll();
    }
}
