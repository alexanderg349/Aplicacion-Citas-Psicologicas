# Guia de tecnologias y aprendizaje

## 1. Por que se cambio de Java/Spring Boot a Python

Se migro porque querias una opcion mas simple de mantener y adaptar. Python permite construir una API moderna con menos friccion y una curva de aprendizaje mas amigable para un junior.

## 2. Tecnologias usadas

### FastAPI

Se usa para crear la API.

Por que sirve:

- crea endpoints HTTP rapidamente
- valida datos automaticamente
- genera documentacion interactiva en `/docs`
- es moderna y muy clara para aprender

### SQLAlchemy

Se usa para mapear objetos Python a tablas de base de datos.

Por que sirve:

- evita escribir SQL manual para todo
- reduce riesgo de inyeccion SQL
- facilita cambiar entre SQLite y MySQL

### Pydantic

Se usa para validar y serializar datos.

Por que sirve:

- verifica que los campos tengan el tipo correcto
- ayuda a devolver respuestas limpias
- hace que el backend sea mas estricto y predecible

### JWT

Se usa para autenticacion.

Por que sirve:

- el frontend recibe un token al iniciar sesion
- ese token se envia en cada peticion protegida
- el backend sabe quien hace la accion y con que rol

### Argon2

Se usa para hash de contrasenas.

Por que sirve:

- no guarda contrasenas en texto plano
- es mucho mas fuerte que guardar texto directo o usar hash debil

### React + Axios

Se mantienen en el frontend.

Por que sirven:

- React organiza la interfaz por componentes
- Axios facilita llamadas HTTP

## 3. Que aprende un junior aqui

### Paso 1. Entender cliente y servidor

- `frontend-citas` es el cliente
- `backend-python` es el servidor
- el cliente hace peticiones al servidor

### Paso 2. Entender rutas

Ejemplo:

- frontend llama `POST /api/v1/auth/login`
- backend valida usuario
- backend responde token + perfil

### Paso 3. Entender modelos

Los modelos representan tablas:

- `User`
- `Appointment`
- `ClinicalHistory`
- `ClinicalEvolution`

### Paso 4. Entender schemas

Los `schemas` son contratos.

Ejemplo:

- que campos recibe `login`
- que campos devuelve `summary`

### Paso 5. Entender servicios

Los servicios contienen la logica de negocio.

Ejemplo:

- autenticar usuario
- crear cita
- actualizar historia clinica

### Paso 6. Entender dependencias

FastAPI usa dependencias para:

- abrir y cerrar la sesion de base de datos
- validar el token
- verificar el rol

## 4. Recorrido del login paso a paso

1. El usuario llena correo y contrasena.
2. React envia `POST /api/v1/auth/login`.
3. FastAPI recibe el JSON.
4. Busca el usuario en base de datos.
5. Verifica la contrasena con Argon2.
6. Si todo es correcto, genera JWT.
7. El frontend guarda el token en `localStorage`.
8. Axios envia ese token en futuras peticiones.

## 5. Recorrido de una cita nueva

1. El paciente entra al panel.
2. Escoge psicologo, fecha, hora y motivo.
3. React arma el payload.
4. FastAPI valida el token del paciente.
5. FastAPI crea la cita.
6. El servicio registra una bitacora tipo WhatsApp.
7. El frontend refresca la agenda.

## 6. Como estudiar este proyecto

Orden recomendado:

1. `frontend-citas/src/pages/LoginPage.jsx`
2. `frontend-citas/src/pages/DashboardPage.jsx`
3. `backend-python/app/main.py`
4. `backend-python/app/api/routes/auth.py`
5. `backend-python/app/services/auth_service.py`
6. `backend-python/app/models/user.py`
7. `backend-python/app/services/appointment_service.py`
8. `backend-python/app/services/clinical_service.py`

## 7. Ejercicios para aprender

### Nivel 1

- Cambia el tiempo de expiracion del token
- Cambia el texto de las alertas del login

### Nivel 2

- Agrega un campo `documento`
- Muestra el documento en el panel admin

### Nivel 3

- Reemplaza SQLite por MySQL en desarrollo
- Agrega filtro por fecha en agenda del psicologo

### Nivel 4

- Integra proveedor real de WhatsApp
- Guarda auditoria de cambios de historia clinica
