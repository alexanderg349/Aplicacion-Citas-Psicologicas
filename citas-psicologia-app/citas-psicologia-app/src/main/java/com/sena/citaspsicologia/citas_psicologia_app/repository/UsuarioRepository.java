package com.sena.citaspsicologia.citas_psicologia_app.repository;

import java.util.List;
import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

import com.sena.citaspsicologia.citas_psicologia_app.model.RolUsuario;
import com.sena.citaspsicologia.citas_psicologia_app.model.Usuario;

public interface UsuarioRepository extends JpaRepository<Usuario, Long> {
    Optional<Usuario> findByEmail(String email);
    List<Usuario> findByRolOrderByNombreAsc(RolUsuario rol);
}
