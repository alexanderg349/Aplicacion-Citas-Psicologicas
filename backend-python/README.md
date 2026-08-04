# Backend Python Seguro

Backend migrado desde Java/Spring Boot hacia Python/FastAPI.

## Que resuelve

- Autenticacion por `JWT`
- Control de acceso por roles
- Registro publico solo para `PACIENTE`
- Creacion de `ADMINISTRADOR` y `PSICOLOGO` solo desde panel admin
- Hash seguro de contrasenas con `Argon2`
- Validacion fuerte de datos con `Pydantic`
- Configuracion por variables de entorno
- Bitacora de notificaciones tipo WhatsApp

## Estructura

- `app/main.py`: punto de entrada
- `app/core`: configuracion, seguridad y rate limiting
- `app/db`: engine y sesiones SQLAlchemy
- `app/models`: tablas ORM
- `app/schemas`: modelos de entrada y salida
- `app/services`: logica de negocio
- `app/api/routes`: endpoints
- `docs/`: documentacion funcional y de aprendizaje

## Arranque rapido

1. Copia `.env.example` a `.env`
2. Ajusta `SECRET_KEY`, `DATABASE_URL` y `CORS_ORIGINS`
3. Instala dependencias:
   - `python -m pip install -r requirements.txt`
4. Inicia el backend:
   - `python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000`

## Usuarios demo

- Administrador: `admin@psicologia.com` / `Admin123*Seguro`
- Psicologo: `psicologo@psicologia.com` / `Psico123*Seguro`
- Paciente: `paciente@psicologia.com` / `Paciente123*Seguro`

## Documentacion adicional

- [Documentacion del sistema](./docs/DOCUMENTACION_DEL_SISTEMA.md)
- [Guia de tecnologias y aprendizaje](./docs/GUIA_TECNOLOGIAS_Y_APRENDIZAJE.md)
- [Despliegue y seguridad](./docs/DESPLIEGUE_HOSTINGER_Y_SEGURIDAD.md)
