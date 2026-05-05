package com.sena.citaspsicologia.citas_psicologia_app.service;

import org.springframework.stereotype.Service;

import com.sena.citaspsicologia.citas_psicologia_app.model.Cita;
import com.sena.citaspsicologia.citas_psicologia_app.model.NotificacionWhatsapp;
import com.sena.citaspsicologia.citas_psicologia_app.repository.NotificacionWhatsappRepository;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class WhatsappService {

    private final NotificacionWhatsappRepository notificacionWhatsappRepository;

    public NotificacionWhatsapp registrarEvento(Cita cita, String evento) {
        String mensaje = "Hola " + cita.getPaciente().getNombre()
                + ", tu cita con el psicologo " + cita.getPsicologo().getNombre()
                + " quedo " + cita.getEstado().name().toLowerCase()
                + " para " + cita.getFechaHora() + ".";

        return notificacionWhatsappRepository.save(NotificacionWhatsapp.builder()
                .cita(cita)
                .telefonoDestino(cita.getPaciente().getTelefono())
                .evento(evento)
                .mensaje(mensaje)
                .build());
    }
}
