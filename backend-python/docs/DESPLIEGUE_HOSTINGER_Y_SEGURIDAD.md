# Despliegue en Hostinger y seguridad

## 1. Realidad importante sobre Hostinger

Si tu plan es `Web Hosting` o `Cloud Hosting`, Hostinger no te deja ejecutar Python ni Java del lado del servidor porque no tienes acceso root.

Eso significa que este backend Python necesita una de estas opciones:

- `Hostinger VPS`
- otro proveedor para el backend, por ejemplo Render, Railway o un VPS externo

Si quieres quedarte en Hostinger sin VPS, la salida mas realista es:

- desplegar el frontend estatico en Hostinger
- desplegar el backend Python en un servicio aparte

## 2. Opcion recomendada

### Opcion A. Hostinger VPS

- frontend y backend pueden vivir bajo el mismo dominio
- tienes control del sistema
- puedes instalar Python, dependencias, proxy reverso y SSL

### Opcion B. Frontend en Hostinger + backend externo

- frontend React compilado en Hostinger
- backend FastAPI en Render/Railway/VPS
- el frontend apunta a la URL publica del backend con `VITE_API_URL`

## 3. Mejoras de seguridad implementadas

### Secretos fuera del repositorio

- se eliminaron credenciales hardcodeadas
- se usan variables de entorno

### Contrasenas seguras

- se usa `Argon2`
- no se guardan contrasenas en texto plano

### JWT con expiracion

- el token expira
- el backend valida rol y usuario en cada peticion

### RBAC

- `PACIENTE` no puede crear administradores
- `PSICOLOGO` no puede abrir resumen admin
- `ADMINISTRADOR` es el unico que crea usuarios internos

### Rate limiting en autenticacion

- se limita el numero de intentos por IP y ruta

### Bloqueo temporal por fuerza bruta

- tras varios intentos fallidos la cuenta se bloquea temporalmente

### CORS restringido

- solo se permiten orígenes definidos en configuracion

### Encabezados de seguridad

- `X-Frame-Options`
- `X-Content-Type-Options`
- `Referrer-Policy`
- `Permissions-Policy`
- `Strict-Transport-Security` en produccion

### ORM en lugar de SQL concatenado

- reduce superficie de inyeccion SQL

### Serializacion controlada

- el backend devuelve solo campos autorizados

## 4. Recomendaciones extra para subir aun mas la seguridad

- mover el token desde `localStorage` a cookies `HttpOnly` si luego unificas dominio y backend
- usar `HTTPS` obligatorio en produccion
- poner Nginx como proxy reverso
- activar `fail2ban` en VPS
- usar rotacion de logs
- hacer backups automaticos cifrados
- agregar auditoria de cambios clinicos
- integrar 2FA para administradores

## 5. Pasos de despliegue en VPS

1. Crear VPS Linux en Hostinger.
2. Instalar Python 3.
3. Clonar el proyecto.
4. Crear entorno virtual.
5. Instalar dependencias con `pip install -r requirements.txt`.
6. Crear archivo `.env`.
7. Configurar `DATABASE_URL`.
8. Levantar FastAPI con `uvicorn` o `gunicorn` + `uvicorn workers`.
9. Configurar Nginx como proxy reverso.
10. Instalar SSL con Certbot.
11. Compilar React.
12. Servir el frontend estatico con Nginx o publicarlo aparte.
