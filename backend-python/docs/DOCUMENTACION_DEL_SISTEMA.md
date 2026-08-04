# Documentacion del sistema

## 1. Objetivo

El sistema permite administrar citas psicologicas con tres perfiles:

- `ADMINISTRADOR`
- `PSICOLOGO`
- `PACIENTE`

## 2. Arquitectura actual

- Frontend: `React + Vite + MUI`
- Backend: `FastAPI + SQLAlchemy`
- Base de datos: `SQLite` por defecto para desarrollo
- Produccion: `MySQL` o `MariaDB` mediante `DATABASE_URL`

## 3. Flujo funcional

### Registro

- El registro publico solo crea pacientes.
- Psicologos y administradores se crean desde el panel administrativo.

### Login

- El usuario envia correo y contrasena.
- El backend valida credenciales.
- Si son correctas, responde con un `JWT` y los datos del usuario.

### Panel administrador

- Ve resumen global del sistema.
- Crea usuarios con cualquier rol.
- Consulta usuarios registrados.

### Panel psicologo

- Consulta agenda.
- Cambia estado de citas.
- Ve pacientes atendidos.
- Crea o actualiza historia clinica.
- Agrega evoluciones clinicas.

### Panel paciente

- Consulta sus citas.
- Solicita nuevas citas.
- Consulta resumen de historia clinica.

## 4. Endpoints principales

### Autenticacion

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`

### Administracion

- `GET /api/v1/admin/summary`
- `POST /api/v1/admin/users`

### Usuarios

- `GET /api/v1/users/psychologists`

### Pacientes

- `GET /api/v1/patients/me/summary`
- `POST /api/v1/patients/me/appointments`

### Psicologos

- `GET /api/v1/psychologists/me/agenda`
- `GET /api/v1/psychologists/me/patients`
- `GET /api/v1/psychologists/me/patients/{patient_id}/history`
- `PUT /api/v1/psychologists/me/patients/{patient_id}/history`
- `POST /api/v1/psychologists/me/patients/{patient_id}/evolutions`

### Citas

- `PATCH /api/v1/appointments/{appointment_id}/status`

## 5. Modelos de negocio

### User

- datos personales
- correo unico
- contrasena cifrada
- rol
- especialidad opcional
- bloqueo temporal por intentos fallidos

### Appointment

- paciente
- psicologo
- fecha y hora
- motivo
- observaciones
- estado

### ClinicalHistory

- motivo de consulta
- antecedentes
- diagnostico inicial
- plan de tratamiento

### ClinicalEvolution

- cita asociada opcional
- resumen de sesion
- observaciones
- recomendaciones

### WhatsAppLog

- cita relacionada
- telefono destino
- evento
- mensaje generado

## 6. Variables de entorno importantes

- `SECRET_KEY`
- `DATABASE_URL`
- `CORS_ORIGINS`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `SEED_DEMO_DATA`
- `MAX_LOGIN_FAILURES`
- `LOCK_MINUTES_AFTER_FAILURES`

## 7. Cambio importante de seguridad

En el backend anterior cualquier persona podia intentar crear usuarios con rol de administrador o psicologo desde el formulario publico. Eso ya no es posible.

## 8. Estado del backend Java

El backend Spring Boot queda en el repositorio solo como referencia historica. Ya no debe ser la opcion principal de despliegue.
