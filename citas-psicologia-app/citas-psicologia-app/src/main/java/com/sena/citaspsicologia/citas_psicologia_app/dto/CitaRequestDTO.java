package com.sena.citaspsicologia.citas_psicologia_app.dto;

import java.time.LocalDateTime;

import com.sena.citaspsicologia.citas_psicologia_app.model.EstadoCita;

import lombok.Data;

@Data
public class CitaRequestDTO {
    private Long pacienteId;
    private Long psicologoId;
    private LocalDateTime fechaHora;
    private String motivo;
    private String observaciones;
    private EstadoCita estado;
}
