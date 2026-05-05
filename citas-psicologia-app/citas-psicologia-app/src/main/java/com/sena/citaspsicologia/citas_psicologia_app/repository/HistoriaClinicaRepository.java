package com.sena.citaspsicologia.citas_psicologia_app.repository;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

import com.sena.citaspsicologia.citas_psicologia_app.model.HistoriaClinica;

public interface HistoriaClinicaRepository extends JpaRepository<HistoriaClinica, Long> {
    Optional<HistoriaClinica> findByPacienteId(Long pacienteId);
}
