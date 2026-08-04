import { useEffect, useState } from 'react';
import { Alert, Box, Button, Container, Link, Paper, Stack, TextField, Typography } from '@mui/material';
import Swal from 'sweetalert2';
import { loginUsuario, registrarUsuario } from '../services/AuthService';

const initialState = {
  nombre: '',
  apellido: '',
  email: '',
  password: '',
  telefono: '',
};

export function LoginPage({ onLoginSuccess }) {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState(initialState);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setFormData(initialState);
  }, [isLogin]);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((current) => ({ ...current, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    try {
      if (isLogin) {
        const response = await loginUsuario({ email: formData.email, password: formData.password });
        Swal.fire('Ingreso correcto', `Bienvenido ${response.data.user.nombreCompleto}`, 'success');
        onLoginSuccess(response.data);
      } else {
        const response = await registrarUsuario({
          nombre: formData.nombre,
          apellido: formData.apellido,
          email: formData.email,
          password: formData.password,
          telefono: formData.telefono,
          rol: 'PACIENTE',
        });
        Swal.fire('Paciente registrado', 'La cuenta fue creada correctamente y ya quedaste autenticado.', 'success');
        onLoginSuccess(response.data);
      }
    } catch (error) {
      const detail = error.response?.data?.detail;
      const message = Array.isArray(detail) ? detail[0] : detail || 'No fue posible completar la solicitud.';
      Swal.fire('Error', message, 'error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ minHeight: '100vh', background: 'linear-gradient(135deg, #082f49 0%, #0f766e 45%, #f8fafc 100%)', display: 'grid', placeItems: 'center', px: 2 }}>
      <Container maxWidth="md">
        <Paper sx={{ borderRadius: 8, overflow: 'hidden', boxShadow: '0 30px 80px rgba(8, 47, 73, 0.30)' }}>
          <Stack direction={{ xs: 'column', md: 'row' }}>
            <Box sx={{ flex: 1, p: { xs: 4, md: 5 }, background: 'linear-gradient(160deg, #082f49, #0f172a)', color: 'white' }}>
              <Typography variant="overline" sx={{ letterSpacing: 3 }}>SENA · Proyecto formativo</Typography>
              <Typography variant="h3" fontWeight={800} sx={{ mt: 1, mb: 2 }}>
                Sistema de agendamiento para psicologia
              </Typography>
              <Typography sx={{ opacity: 0.86, maxWidth: 420 }}>
                Frontend React con backend Python seguro, autenticacion por token, control por roles e historial clinico protegido.
              </Typography>
              <Stack spacing={1.5} sx={{ mt: 4 }}>
                <Alert severity="info" sx={{ borderRadius: 3 }}>Administrador: crea usuarios internos y supervisa la operacion.</Alert>
                <Alert severity="success" sx={{ borderRadius: 3 }}>Psicologo: gestiona agenda, pacientes e historia clinica.</Alert>
                <Alert severity="warning" sx={{ borderRadius: 3 }}>Paciente: se registra publicamente y consulta sus citas.</Alert>
              </Stack>
            </Box>

            <Box sx={{ flex: 1, p: { xs: 4, md: 5 }, backgroundColor: 'rgba(255,255,255,0.95)' }}>
              <Typography variant="h4" fontWeight={800}>{isLogin ? 'Iniciar sesion' : 'Crear cuenta de paciente'}</Typography>
              <Typography color="text.secondary" sx={{ mb: 3 }}>
                {isLogin ? 'Accede con tu correo y contrasena.' : 'Por seguridad, el registro publico solo crea cuentas de paciente.'}
              </Typography>

              <Box component="form" onSubmit={handleSubmit}>
                <Stack spacing={2}>
                  {!isLogin ? (
                    <>
                      <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2}>
                        <TextField name="nombre" label="Nombre" required fullWidth value={formData.nombre} onChange={handleChange} />
                        <TextField name="apellido" label="Apellido" required fullWidth value={formData.apellido} onChange={handleChange} />
                      </Stack>
                      <TextField name="telefono" label="Telefono" required fullWidth value={formData.telefono} onChange={handleChange} />
                      <Alert severity="info" sx={{ borderRadius: 3 }}>
                        Los usuarios administradores y psicologos solo pueden ser creados desde el panel del administrador.
                      </Alert>
                    </>
                  ) : null}

                  <TextField name="email" label="Correo electronico" type="email" required fullWidth value={formData.email} onChange={handleChange} />
                  <TextField name="password" label="Contrasena" type="password" required fullWidth value={formData.password} onChange={handleChange} helperText={!isLogin ? 'Usa al menos 12 caracteres, mayuscula, minuscula, numero y simbolo.' : ' '} />

                  <Button type="submit" variant="contained" size="large" disabled={loading} sx={{ py: 1.6, borderRadius: 3 }}>
                    {loading ? 'Procesando...' : isLogin ? 'Ingresar' : 'Registrar y entrar'}
                  </Button>

                  <Typography textAlign="center" color="text.secondary">
                    {isLogin ? 'Si aun no tienes cuenta' : 'Si ya tienes cuenta'}{' '}
                    <Link component="button" type="button" onClick={() => setIsLogin((current) => !current)} underline="hover">
                      {isLogin ? 'registrate aqui' : 'inicia sesion aqui'}
                    </Link>
                  </Typography>
                </Stack>
              </Box>
            </Box>
          </Stack>
        </Paper>
      </Container>
    </Box>
  );
}
