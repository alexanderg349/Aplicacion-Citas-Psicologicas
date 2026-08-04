import { useEffect, useState } from 'react';
import { DashboardPage } from './pages/DashboardPage';
import { LoginPage } from './pages/LoginPage';

function App() {
  const [usuario, setUsuario] = useState(() => {
    const saved = localStorage.getItem('usuario-sesion');
    return saved ? JSON.parse(saved) : null;
  });

  useEffect(() => {
    if (usuario) {
      localStorage.setItem('usuario-sesion', JSON.stringify(usuario));
    } else {
      localStorage.removeItem('usuario-sesion');
    }
  }, [usuario]);

  return usuario ? (
    <DashboardPage usuario={usuario.user || usuario} onLogout={() => setUsuario(null)} />
  ) : (
    <LoginPage onLoginSuccess={setUsuario} />
  );
}

export default App;
