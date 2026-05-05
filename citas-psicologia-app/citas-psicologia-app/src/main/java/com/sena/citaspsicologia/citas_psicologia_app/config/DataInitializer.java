package com.sena.citaspsicologia.citas_psicologia_app.config;

import java.time.LocalDateTime;

import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import com.sena.citaspsicologia.citas_psicologia_app.model.Cita;
import com.sena.citaspsicologia.citas_psicologia_app.model.EstadoCita;
import com.sena.citaspsicologia.citas_psicologia_app.model.HistoriaClinica;
import com.sena.citaspsicologia.citas_psicologia_app.model.RolUsuario;
import com.sena.citaspsicologia.citas_psicologia_app.model.Usuario;
import com.sena.citaspsicologia.citas_psicologia_app.repository.CitaRepository;
import com.sena.citaspsicologia.citas_psicologia_app.repository.HistoriaClinicaRepository;
import com.sena.citaspsicologia.citas_psicologia_app.repository.UsuarioRepository;
import com.sena.citaspsicologia.citas_psicologia_app.service.WhatsappService;

@Configuration
public class DataInitializer {

    @Bean
    CommandLineRunner initData(UsuarioRepository usuarioRepository,
                               CitaRepository citaRepository,
                               HistoriaClinicaRepository historiaClinicaRepository,
                               WhatsappService whatsappService) {
        return args -> {
            if (usuarioRepository.count() > 0) {
                return;
            }

            usuarioRepository.save(Usuario.builder()
                    .nombre("Administrador")
                    .apellido("Principal")
                    .email("admin@psicologia.com")
                    .password("Admin123*")
                    .telefono("3000000001")
                    .rol(RolUsuario.ADMINISTRADOR)
                    .build());

            Usuario psicologo = usuarioRepository.save(Usuario.builder()
                    .nombre("Laura")
                    .apellido("Ramirez")
                    .email("psicologo@psicologia.com")
                    .password("Psico123*")
                    .telefono("3000000002")
                    .rol(RolUsuario.PSICOLOGO)
                    .especialidad("Terapia cognitivo conductual")
                    .build());

            Usuario paciente = usuarioRepository.save(Usuario.builder()
                    .nombre("Carlos")
                    .apellido("Gomez")
                    .email("paciente@psicologia.com")
                    .password("Paciente123*")
                    .telefono("3000000003")
                    .rol(RolUsuario.PACIENTE)
                    .build());

            historiaClinicaRepository.save(HistoriaClinica.builder()
                    .paciente(paciente)
                    .motivoConsulta("Ansiedad laboral y dificultades para dormir.")
                    .antecedentes("No registra hospitalizaciones. Reporta episodios previos de estres.")
                    .diagnosticoInicial("Sintomas compatibles con ansiedad moderada.")
                    .planTratamiento("Sesiones semanales, diario emocional y tecnicas de respiracion.")
                    .build());

            Cita proximaCita = citaRepository.save(Cita.builder()
                    .paciente(paciente)
                    .psicologo(psicologo)
                    .fechaHora(LocalDateTime.now().plusDays(2).withHour(16).withMinute(0).withSecond(0).withNano(0))
                    .motivo("Seguimiento terapeutico")
                    .estado(EstadoCita.PROGRAMADA)
                    .observaciones("Paciente solicita modalidad virtual.")
                    .build());

            citaRepository.save(Cita.builder()
                    .paciente(paciente)
                    .psicologo(psicologo)
                    .fechaHora(LocalDateTime.now().minusDays(7).withHour(15).withMinute(0).withSecond(0).withNano(0))
                    .motivo("Valoracion inicial")
                    .estado(EstadoCita.COMPLETADA)
                    .observaciones("Se levanto informacion inicial para historia clinica.")
                    .build());

            whatsappService.registrarEvento(proximaCita, "SEMILLA_CITA");
        };
    }
}
