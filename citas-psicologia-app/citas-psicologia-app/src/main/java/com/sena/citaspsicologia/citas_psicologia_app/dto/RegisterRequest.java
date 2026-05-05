package com.sena.citaspsicologia.citas_psicologia_app.dto;

import com.sena.citaspsicologia.citas_psicologia_app.model.RolUsuario;

import lombok.Data;

@Data
public class RegisterRequest {
    private String nombre;
    private String apellido;
    private String email;
    private String password;
    private String telefono;
    private RolUsuario rol;
    private String especialidad;
}
