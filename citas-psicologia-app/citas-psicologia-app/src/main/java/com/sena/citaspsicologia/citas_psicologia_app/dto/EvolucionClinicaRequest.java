package com.sena.citaspsicologia.citas_psicologia_app.dto;

import lombok.Data;

@Data
public class EvolucionClinicaRequest {
    private Long citaId;
    private String resumenSesion;
    private String observaciones;
    private String recomendaciones;
}
