# Paso a paso del proyecto de citas psicologicas

## 1. Estructura del proyecto
- Backend Spring Boot: `citas-psicologia-app/citas-psicologia-app`
- Frontend React: `frontend-citas`

## 2. Requisitos previos
- MySQL activo en `localhost:3306`
- Base de datos `db_citas_psicologia`
- Node.js instalado
- Java JDK instalado y `JAVA_HOME` configurado

## 3. Configurar base de datos
1. Crear la base de datos en MySQL:
   `CREATE DATABASE db_citas_psicologia;`
2. Revisar el archivo `citas-psicologia-app/citas-psicologia-app/src/main/resources/application.properties`.
3. Si tu usuario o clave de MySQL es diferente, ajustalos alli.
4. Iniciar el backend. Hibernate crea las tablas nuevas automaticamente:
   - `usuarios_app`
   - `citas_app`
   - `historias_clinicas`
   - `evoluciones_clinicas`
   - `whatsapp_log`

## 4. Ejecutar el backend
1. Instala Java si aun no lo tienes disponible en consola.
2. Configura `JAVA_HOME`.
3. Entra a `citas-psicologia-app/citas-psicologia-app`.
4. Ejecuta:
   `mvnw.cmd spring-boot:run`
5. El backend queda en `http://localhost:8090`.

## 5. Ejecutar el frontend
1. Entra a `frontend-citas`.
2. Ejecuta:
   `npm install`
3. Luego:
   `npm run dev`
4. Abre `http://localhost:5173`.

## 6. Usuarios de prueba
- Administrador: `admin@psicologia.com` / `Admin123*`
- Psicologo: `psicologo@psicologia.com` / `Psico123*`
- Paciente: `paciente@psicologia.com` / `Paciente123*`

## 7. Funcionalidades ya implementadas
- Registro de usuario con rol: administrador, psicologo o paciente
- Correo y contrasena por usuario
- Telefono obligatorio para todos los usuarios
- Especialidad obligatoria para psicologos
- Ambiente distinto segun el rol
- Paciente: consulta sus citas y solicita nuevas
- Psicologo: ve agenda, pacientes, historia clinica y evoluciones
- Administrador: ve resumen del sistema y usuarios registrados
- Registro de notificaciones tipo WhatsApp en la tabla `whatsapp_log` cuando se crea o cambia una cita

## 8. Importante sobre WhatsApp real
Por ahora el proyecto deja la trazabilidad y el mensaje generado en base de datos.
Si quieres envio real, el siguiente paso es integrar una API como Twilio o Meta WhatsApp Cloud.

## 9. Siguiente mejora recomendada
- Cifrar contrasenas con BCrypt
- Agregar JWT o sesiones seguras
- Restringir endpoints segun rol
- Conectar WhatsApp real
- Crear modulo de disponibilidad horaria del psicologo
