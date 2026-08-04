from sqlalchemy.orm import Session

from app.models import Appointment, WhatsAppLog


def log_whatsapp_event(db: Session, appointment: Appointment, event: str) -> None:
    message = (
        f"Hola {appointment.paciente.nombre}, tu cita con {appointment.psicologo.nombre} "
        f"quedo {appointment.estado.value.lower()} para {appointment.fecha_hora.isoformat()}."
    )
    db.add(
        WhatsAppLog(
            appointment_id=appointment.id,
            telefono_destino=appointment.paciente.telefono,
            evento=event,
            mensaje=message,
        )
    )
    db.commit()
