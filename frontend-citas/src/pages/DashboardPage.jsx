import { useEffect, useMemo, useState } from 'react';
import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  Container,
  Divider,
  FormControl,
  InputLabel,
  MenuItem,
  Paper,
  Select,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from '@mui/material';
import Swal from 'sweetalert2';
import { guardarCita, actualizarEstadoCita } from '../services/CitaService';
import {
  agregarEvolucionPaciente,
  crearUsuarioDesdeAdmin,
  guardarHistoriaPaciente,
  obtenerAgendaPsicologo,
  obtenerHistoriaPaciente,
  obtenerPacientesPsicologo,
  obtenerResumenAdmin,
  obtenerResumenPaciente,
} from '../services/DashboardService';
import { listarPsicologos } from '../services/AuthService';

const formatearFecha = (valor) => {
  if (!valor) return 'Sin fecha';
  return new Date(valor).toLocaleString('es-CO', {
    dateStyle: 'medium',
    timeStyle: 'short',
  });
};

const estadoColor = {
  PROGRAMADA: 'primary',
  REPROGRAMADA: 'warning',
  COMPLETADA: 'success',
  CANCELADA: 'error',
};

function SectionCard({ title, subtitle, children }) {
  return (
    <Card sx={{ borderRadius: 4, boxShadow: '0 24px 60px rgba(15, 23, 42, 0.08)' }}>
      <CardContent sx={{ p: 3 }}>
        <Typography variant="h6" fontWeight={700}>{title}</Typography>
        {subtitle ? <Typography color="text.secondary" sx={{ mb: 2 }}>{subtitle}</Typography> : null}
        {children}
      </CardContent>
    </Card>
  );
}

function AdminDashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [formData, setFormData] = useState({
    nombre: '',
    apellido: '',
    telefono: '',
    rol: 'PACIENTE',
    especialidad: '',
    email: '',
    password: '',
  });

  const cargar = async () => {
    const response = await obtenerResumenAdmin();
    setData(response.data);
  };

  useEffect(() => {
    cargar()
      .catch(() => Swal.fire('Error', 'No fue posible cargar el resumen administrativo.', 'error'))
      .finally(() => setLoading(false));
  }, []);

  const handleCreateUser = async (event) => {
    event.preventDefault();
    try {
      await crearUsuarioDesdeAdmin({
        ...formData,
        especialidad: formData.rol === 'PSICOLOGO' ? formData.especialidad : null,
      });
      Swal.fire('Usuario creado', 'El usuario fue creado desde administracion con control de roles.', 'success');
      setFormData({ nombre: '', apellido: '', telefono: '', rol: 'PACIENTE', especialidad: '', email: '', password: '' });
      await cargar();
    } catch (error) {
      const detail = error.response?.data?.detail;
      Swal.fire('Error', Array.isArray(detail) ? detail[0] : detail || 'No se pudo crear el usuario.', 'error');
    }
  };

  if (loading) return <Alert severity="info">Cargando panel administrativo...</Alert>;

  return (
    <Stack spacing={3}>
      <Stack direction={{ xs: 'column', md: 'row' }} spacing={2}>
        {[
          ['Pacientes', data.totalPacientes],
          ['Psicologos', data.totalPsicologos],
          ['Administradores', data.totalAdministradores],
          ['Citas', data.totalCitas],
        ].map(([label, value]) => (
          <Paper key={label} sx={{ flex: 1, p: 2.5, borderRadius: 4, background: 'linear-gradient(135deg, #0f172a, #1d4ed8)', color: 'white' }}>
            <Typography variant="body2">{label}</Typography>
            <Typography variant="h3" fontWeight={800}>{value}</Typography>
          </Paper>
        ))}
      </Stack>

      <SectionCard title="Crear usuarios internos" subtitle="Solo administracion puede crear psicologos y administradores. Esto evita escalamiento de privilegios desde el registro publico.">
        <Box component="form" onSubmit={handleCreateUser}>
          <Stack spacing={2}>
            <Stack direction={{ xs: 'column', md: 'row' }} spacing={2}>
              <TextField label="Nombre" required fullWidth value={formData.nombre} onChange={(event) => setFormData((current) => ({ ...current, nombre: event.target.value }))} />
              <TextField label="Apellido" required fullWidth value={formData.apellido} onChange={(event) => setFormData((current) => ({ ...current, apellido: event.target.value }))} />
            </Stack>
            <Stack direction={{ xs: 'column', md: 'row' }} spacing={2}>
              <TextField label="Telefono" required fullWidth value={formData.telefono} onChange={(event) => setFormData((current) => ({ ...current, telefono: event.target.value }))} />
              <TextField label="Correo electronico" type="email" required fullWidth value={formData.email} onChange={(event) => setFormData((current) => ({ ...current, email: event.target.value }))} />
            </Stack>
            <Stack direction={{ xs: 'column', md: 'row' }} spacing={2}>
              <FormControl fullWidth>
                <InputLabel>Rol</InputLabel>
                <Select label="Rol" value={formData.rol} onChange={(event) => setFormData((current) => ({ ...current, rol: event.target.value }))}>
                  <MenuItem value="ADMINISTRADOR">Administrador</MenuItem>
                  <MenuItem value="PSICOLOGO">Psicologo</MenuItem>
                  <MenuItem value="PACIENTE">Paciente</MenuItem>
                </Select>
              </FormControl>
              <TextField label="Contrasena" type="password" required fullWidth value={formData.password} onChange={(event) => setFormData((current) => ({ ...current, password: event.target.value }))} helperText="Minimo 12 caracteres con mayuscula, minuscula, numero y simbolo." />
            </Stack>
            {formData.rol === 'PSICOLOGO' ? <TextField label="Especialidad" required fullWidth value={formData.especialidad} onChange={(event) => setFormData((current) => ({ ...current, especialidad: event.target.value }))} /> : null}
            <Button type="submit" variant="contained" sx={{ alignSelf: 'start', px: 4 }}>Crear usuario</Button>
          </Stack>
        </Box>
      </SectionCard>

      <SectionCard title="Usuarios registrados" subtitle="Resumen de cuentas y perfiles disponibles en el sistema.">
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Nombre</TableCell>
              <TableCell>Rol</TableCell>
              <TableCell>Correo</TableCell>
              <TableCell>Telefono</TableCell>
              <TableCell>Especialidad</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {data.usuarios.map((usuario) => (
              <TableRow key={usuario.id}>
                <TableCell>{usuario.nombre} {usuario.apellido}</TableCell>
                <TableCell>{usuario.rol}</TableCell>
                <TableCell>{usuario.email}</TableCell>
                <TableCell>{usuario.telefono}</TableCell>
                <TableCell>{usuario.especialidad || 'No aplica'}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </SectionCard>
    </Stack>
  );
}

function PatientDashboard() {
  const [resumen, setResumen] = useState(null);
  const [psicologos, setPsicologos] = useState([]);
  const [formData, setFormData] = useState({
    psicologo_id: '',
    fecha: '',
    hora: '',
    motivo: '',
    observaciones: '',
  });

  const cargar = async () => {
    const [resumenResp, psicologosResp] = await Promise.all([
      obtenerResumenPaciente(),
      listarPsicologos(),
    ]);
    setResumen(resumenResp.data);
    setPsicologos(psicologosResp.data);
  };

  useEffect(() => {
    cargar().catch(() => Swal.fire('Error', 'No fue posible cargar el panel del paciente.', 'error'));
  }, []);

  const handleCrearCita = async (event) => {
    event.preventDefault();
    try {
      await guardarCita({
        psicologo_id: Number(formData.psicologo_id),
        fecha_hora: `${formData.fecha}T${formData.hora}:00`,
        motivo: formData.motivo,
        observaciones: formData.observaciones,
      });
      Swal.fire('Cita creada', 'La cita fue registrada y quedo lista para notificacion por WhatsApp.', 'success');
      setFormData({ psicologo_id: '', fecha: '', hora: '', motivo: '', observaciones: '' });
      await cargar();
    } catch (error) {
      const detail = error.response?.data?.detail;
      Swal.fire('Error', Array.isArray(detail) ? detail[0] : detail || 'No se pudo crear la cita.', 'error');
    }
  };

  if (!resumen) return <Alert severity="info">Cargando tus citas y tu historia clinica...</Alert>;

  const citas = resumen.citas || [];
  const historia = resumen.historia?.historia;

  return (
    <Stack spacing={3}>
      <SectionCard title="Agenda del paciente" subtitle="Aqui puedes consultar tus citas programadas y pedir nuevas sesiones.">
        <Stack spacing={2}>
          {citas.length === 0 ? <Alert severity="warning">Aun no tienes citas registradas.</Alert> : null}
          {citas.map((cita) => (
            <Paper key={cita.id} sx={{ p: 2, borderRadius: 3, border: '1px solid #e2e8f0' }}>
              <Stack direction={{ xs: 'column', md: 'row' }} justifyContent="space-between" spacing={1}>
                <Box>
                  <Typography fontWeight={700}>{cita.motivo}</Typography>
                  <Typography color="text.secondary">{formatearFecha(cita.fecha_hora)}</Typography>
                  <Typography color="text.secondary">Psicologo: {cita.psicologo?.nombre} {cita.psicologo?.apellido}</Typography>
                </Box>
                <Chip label={cita.estado} color={estadoColor[cita.estado] || 'default'} />
              </Stack>
            </Paper>
          ))}
        </Stack>
      </SectionCard>

      <SectionCard title="Solicitar nueva cita" subtitle="Cada cita queda enlazada con tu telefono para aviso de cambios por WhatsApp.">
        <Box component="form" onSubmit={handleCrearCita}>
          <Stack spacing={2}>
            <FormControl fullWidth required>
              <InputLabel>Psicologo</InputLabel>
              <Select label="Psicologo" value={formData.psicologo_id} onChange={(event) => setFormData((current) => ({ ...current, psicologo_id: event.target.value }))}>
                {psicologos.map((item) => (
                  <MenuItem key={item.id} value={item.id}>{item.nombre} {item.apellido}</MenuItem>
                ))}
              </Select>
            </FormControl>
            <Stack direction={{ xs: 'column', md: 'row' }} spacing={2}>
              <TextField type="date" label="Fecha" InputLabelProps={{ shrink: true }} fullWidth required value={formData.fecha} onChange={(event) => setFormData((current) => ({ ...current, fecha: event.target.value }))} />
              <TextField type="time" label="Hora" InputLabelProps={{ shrink: true }} fullWidth required value={formData.hora} onChange={(event) => setFormData((current) => ({ ...current, hora: event.target.value }))} />
            </Stack>
            <TextField label="Motivo" fullWidth required value={formData.motivo} onChange={(event) => setFormData((current) => ({ ...current, motivo: event.target.value }))} />
            <TextField label="Observaciones" fullWidth multiline minRows={3} value={formData.observaciones} onChange={(event) => setFormData((current) => ({ ...current, observaciones: event.target.value }))} />
            <Button type="submit" variant="contained" sx={{ alignSelf: 'start', px: 4 }}>Agendar cita</Button>
          </Stack>
        </Box>
      </SectionCard>

      <SectionCard title="Historia clinica" subtitle="El paciente puede revisar un resumen general de su proceso.">
        {historia ? (
          <Stack spacing={1.5}>
            <Typography><strong>Motivo de consulta:</strong> {historia.motivo_consulta}</Typography>
            <Typography><strong>Antecedentes:</strong> {historia.antecedentes}</Typography>
            <Typography><strong>Diagnostico inicial:</strong> {historia.diagnostico_inicial}</Typography>
            <Typography><strong>Plan de tratamiento:</strong> {historia.plan_tratamiento}</Typography>
          </Stack>
        ) : (
          <Alert severity="info">Tu historia clinica aun no ha sido diligenciada por el terapeuta.</Alert>
        )}
      </SectionCard>
    </Stack>
  );
}

function PsychologistDashboard() {
  const [agenda, setAgenda] = useState([]);
  const [pacientes, setPacientes] = useState([]);
  const [pacienteSeleccionado, setPacienteSeleccionado] = useState('');
  const [detalle, setDetalle] = useState(null);
  const [historiaForm, setHistoriaForm] = useState({ motivo_consulta: '', antecedentes: '', diagnostico_inicial: '', plan_tratamiento: '' });
  const [evolucionForm, setEvolucionForm] = useState({ cita_id: '', resumen_sesion: '', observaciones: '', recomendaciones: '' });

  const cargarBase = async () => {
    const [agendaResp, pacientesResp] = await Promise.all([
      obtenerAgendaPsicologo(),
      obtenerPacientesPsicologo(),
    ]);
    setAgenda(agendaResp.data);
    setPacientes(pacientesResp.data);
  };

  const cargarDetalle = async (pacienteId) => {
    const response = await obtenerHistoriaPaciente(pacienteId);
    setDetalle(response.data);
    const historia = response.data.historia;
    setHistoriaForm({
      motivo_consulta: historia?.motivo_consulta || '',
      antecedentes: historia?.antecedentes || '',
      diagnostico_inicial: historia?.diagnostico_inicial || '',
      plan_tratamiento: historia?.plan_tratamiento || '',
    });
  };

  useEffect(() => {
    cargarBase().catch(() => Swal.fire('Error', 'No se pudo cargar el panel del psicologo.', 'error'));
  }, []);

  useEffect(() => {
    if (!pacienteSeleccionado) return;
    cargarDetalle(pacienteSeleccionado).catch(() => {
      setDetalle(null);
      setHistoriaForm({ motivo_consulta: '', antecedentes: '', diagnostico_inicial: '', plan_tratamiento: '' });
    });
  }, [pacienteSeleccionado]);

  const citasPaciente = useMemo(() => detalle?.agenda || [], [detalle]);

  const guardarHistoria = async (event) => {
    event.preventDefault();
    try {
      await guardarHistoriaPaciente(Number(pacienteSeleccionado), historiaForm);
      Swal.fire('Historia guardada', 'La historia clinica fue actualizada.', 'success');
      await cargarDetalle(pacienteSeleccionado);
    } catch (error) {
      const detail = error.response?.data?.detail;
      Swal.fire('Error', Array.isArray(detail) ? detail[0] : detail || 'No se pudo guardar la historia clinica.', 'error');
    }
  };

  const guardarEvolucion = async (event) => {
    event.preventDefault();
    try {
      await agregarEvolucionPaciente(Number(pacienteSeleccionado), {
        ...evolucionForm,
        cita_id: evolucionForm.cita_id ? Number(evolucionForm.cita_id) : null,
      });
      Swal.fire('Registro agregado', 'La evolucion clinica fue almacenada.', 'success');
      setEvolucionForm({ cita_id: '', resumen_sesion: '', observaciones: '', recomendaciones: '' });
      await cargarDetalle(pacienteSeleccionado);
    } catch (error) {
      const detail = error.response?.data?.detail;
      Swal.fire('Error', Array.isArray(detail) ? detail[0] : detail || 'No se pudo guardar la evolucion clinica.', 'error');
    }
  };

  const cambiarEstado = async (citaId, estado) => {
    try {
      await actualizarEstadoCita(citaId, estado);
      Swal.fire('Cita actualizada', `La cita quedo ${estado.toLowerCase()}.`, 'success');
      await cargarBase();
      if (pacienteSeleccionado) await cargarDetalle(pacienteSeleccionado);
    } catch (error) {
      const detail = error.response?.data?.detail;
      Swal.fire('Error', Array.isArray(detail) ? detail[0] : detail || 'No se pudo actualizar el estado de la cita.', 'error');
    }
  };

  return (
    <Stack spacing={3}>
      <SectionCard title="Agenda del psicologo" subtitle="Controla citas programadas, reprogramadas, completadas o canceladas.">
        <Stack spacing={2}>
          {agenda.map((cita) => (
            <Paper key={cita.id} sx={{ p: 2, borderRadius: 3, border: '1px solid #e2e8f0' }}>
              <Stack direction={{ xs: 'column', lg: 'row' }} justifyContent="space-between" spacing={2}>
                <Box>
                  <Typography fontWeight={700}>{cita.paciente?.nombre} {cita.paciente?.apellido}</Typography>
                  <Typography>{cita.motivo}</Typography>
                  <Typography color="text.secondary">{formatearFecha(cita.fecha_hora)}</Typography>
                </Box>
                <Stack direction={{ xs: 'column', md: 'row' }} spacing={1} alignItems="center">
                  <Chip label={cita.estado} color={estadoColor[cita.estado] || 'default'} />
                  {['REPROGRAMADA', 'COMPLETADA', 'CANCELADA'].map((estado) => (
                    <Button key={estado} size="small" variant="outlined" onClick={() => cambiarEstado(cita.id, estado)}>{estado}</Button>
                  ))}
                </Stack>
              </Stack>
            </Paper>
          ))}
        </Stack>
      </SectionCard>

      <SectionCard title="Pacientes y seguimiento" subtitle="Selecciona un paciente para consultar su historial completo y registrar evoluciones.">
        <Stack spacing={2}>
          <FormControl fullWidth>
            <InputLabel>Paciente</InputLabel>
            <Select label="Paciente" value={pacienteSeleccionado} onChange={(event) => setPacienteSeleccionado(event.target.value)}>
              {pacientes.map((paciente) => (
                <MenuItem key={paciente.id} value={paciente.id}>{paciente.nombre} {paciente.apellido}</MenuItem>
              ))}
            </Select>
          </FormControl>

          {pacienteSeleccionado ? (
            <Stack spacing={3}>
              <Box component="form" onSubmit={guardarHistoria}>
                <Typography variant="subtitle1" fontWeight={700} sx={{ mb: 1 }}>Historia clinica</Typography>
                <Stack spacing={2}>
                  <TextField label="Motivo de consulta" fullWidth multiline minRows={2} value={historiaForm.motivo_consulta} onChange={(event) => setHistoriaForm((current) => ({ ...current, motivo_consulta: event.target.value }))} />
                  <TextField label="Antecedentes" fullWidth multiline minRows={2} value={historiaForm.antecedentes} onChange={(event) => setHistoriaForm((current) => ({ ...current, antecedentes: event.target.value }))} />
                  <TextField label="Diagnostico inicial" fullWidth multiline minRows={2} value={historiaForm.diagnostico_inicial} onChange={(event) => setHistoriaForm((current) => ({ ...current, diagnostico_inicial: event.target.value }))} />
                  <TextField label="Plan de tratamiento" fullWidth multiline minRows={2} value={historiaForm.plan_tratamiento} onChange={(event) => setHistoriaForm((current) => ({ ...current, plan_tratamiento: event.target.value }))} />
                  <Button type="submit" variant="contained" sx={{ alignSelf: 'start' }}>Guardar historia</Button>
                </Stack>
              </Box>

              <Divider />

              <Box component="form" onSubmit={guardarEvolucion}>
                <Typography variant="subtitle1" fontWeight={700} sx={{ mb: 1 }}>Nueva evolucion clinica</Typography>
                <Stack spacing={2}>
                  <FormControl fullWidth>
                    <InputLabel>Cita asociada</InputLabel>
                    <Select label="Cita asociada" value={evolucionForm.cita_id} onChange={(event) => setEvolucionForm((current) => ({ ...current, cita_id: event.target.value }))}>
                      <MenuItem value="">Sin cita</MenuItem>
                      {citasPaciente.map((cita) => (
                        <MenuItem key={cita.id} value={cita.id}>{formatearFecha(cita.fecha_hora)} - {cita.estado}</MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                  <TextField label="Resumen de sesion" fullWidth multiline minRows={2} required value={evolucionForm.resumen_sesion} onChange={(event) => setEvolucionForm((current) => ({ ...current, resumen_sesion: event.target.value }))} />
                  <TextField label="Observaciones" fullWidth multiline minRows={2} value={evolucionForm.observaciones} onChange={(event) => setEvolucionForm((current) => ({ ...current, observaciones: event.target.value }))} />
                  <TextField label="Recomendaciones" fullWidth multiline minRows={2} value={evolucionForm.recomendaciones} onChange={(event) => setEvolucionForm((current) => ({ ...current, recomendaciones: event.target.value }))} />
                  <Button type="submit" variant="contained" sx={{ alignSelf: 'start' }}>Agregar evolucion</Button>
                </Stack>
              </Box>

              <Divider />

              <Box>
                <Typography variant="subtitle1" fontWeight={700} sx={{ mb: 1 }}>Historial del paciente</Typography>
                {!detalle?.evoluciones?.length ? <Alert severity="info">Aun no hay evoluciones registradas.</Alert> : null}
                <Stack spacing={1.5}>
                  {detalle?.evoluciones?.map((item) => (
                    <Paper key={item.id} sx={{ p: 2, borderRadius: 3, border: '1px solid #e2e8f0' }}>
                      <Typography fontWeight={700}>{formatearFecha(item.created_at)}</Typography>
                      <Typography>{item.resumen_sesion}</Typography>
                      <Typography color="text.secondary">Observaciones: {item.observaciones || 'Sin observaciones'}</Typography>
                      <Typography color="text.secondary">Recomendaciones: {item.recomendaciones || 'Sin recomendaciones'}</Typography>
                    </Paper>
                  ))}
                </Stack>
              </Box>
            </Stack>
          ) : (
            <Alert severity="info">Selecciona un paciente para abrir la historia clinica.</Alert>
          )}
        </Stack>
      </SectionCard>
    </Stack>
  );
}

export function DashboardPage({ usuario, onLogout }) {
  const titulo = {
    ADMINISTRADOR: 'Panel administrativo',
    PSICOLOGO: 'Panel del psicologo',
    PACIENTE: 'Panel del paciente',
  }[usuario.rol];

  const subtitulo = {
    ADMINISTRADOR: 'Control general de usuarios, agendas y trazabilidad del sistema.',
    PSICOLOGO: 'Gestion de pacientes, historia clinica, agenda y seguimiento terapeutico.',
    PACIENTE: 'Consulta tus citas y solicita nuevas sesiones desde tu propio ambiente.',
  }[usuario.rol];

  return (
    <Box sx={{ minHeight: '100vh', background: 'radial-gradient(circle at top, #dbeafe 0%, #f8fafc 45%, #e2e8f0 100%)' }}>
      <Container maxWidth="lg" sx={{ py: 5 }}>
        <Paper sx={{ p: 3, mb: 3, borderRadius: 6, background: 'linear-gradient(135deg, #0f172a 0%, #1e3a8a 45%, #0f766e 100%)', color: 'white' }}>
          <Stack direction={{ xs: 'column', md: 'row' }} justifyContent="space-between" spacing={2} alignItems={{ md: 'center' }}>
            <Box>
              <Typography variant="overline" sx={{ letterSpacing: 2 }}>Consultorio psicologico</Typography>
              <Typography variant="h3" fontWeight={800}>{titulo}</Typography>
              <Typography sx={{ opacity: 0.85, maxWidth: 720 }}>{subtitulo}</Typography>
            </Box>
            <Stack alignItems={{ xs: 'start', md: 'end' }} spacing={1}>
              <Chip label={usuario.rol} sx={{ color: 'white', borderColor: 'rgba(255,255,255,0.4)' }} variant="outlined" />
              <Typography fontWeight={700}>{usuario.nombreCompleto}</Typography>
              <Typography>{usuario.email}</Typography>
              <Button variant="contained" color="error" onClick={onLogout}>Cerrar sesion</Button>
            </Stack>
          </Stack>
        </Paper>

        {usuario.rol === 'ADMINISTRADOR' ? <AdminDashboard /> : null}
        {usuario.rol === 'PACIENTE' ? <PatientDashboard /> : null}
        {usuario.rol === 'PSICOLOGO' ? <PsychologistDashboard /> : null}
      </Container>
    </Box>
  );
}
