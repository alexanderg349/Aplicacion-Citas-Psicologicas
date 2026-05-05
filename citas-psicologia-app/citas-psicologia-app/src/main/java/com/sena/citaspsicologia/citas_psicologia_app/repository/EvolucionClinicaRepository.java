package com.sena.citaspsicologia.citas_psicologia_app.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.sena.citaspsicologia.citas_psicologia_app.model.EvolucionClinica;

public interface EvolucionClinicaRepository extends JpaRepository<EvolucionClinica, Long> {
    List<EvolucionClinica> findByHistoriaClinicaIdOrderByFechaRegistroDesc(Long historiaId);
}
