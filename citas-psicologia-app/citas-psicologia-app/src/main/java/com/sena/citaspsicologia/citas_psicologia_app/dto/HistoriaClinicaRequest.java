package com.sena.citaspsicologia.citas_psicologia_app.dto;

import lombok.Data;

@Data
public class HistoriaClinicaRequest {
    private String motivoConsulta;
    private String antecedentes;
    private String diagnosticoInicial;
    private String planTratamiento;
}
