package com.sena.citaspsicologia.citas_psicologia_app.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.sena.citaspsicologia.citas_psicologia_app.model.Cita;

public interface CitaRepository extends JpaRepository<Cita, Long> {
    List<Cita> findByPacienteIdOrderByFechaHoraAsc(Long pacienteId);
    List<Cita> findByPsicologoIdOrderByFechaHoraAsc(Long psicologoId);
}
