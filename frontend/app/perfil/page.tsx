'use client';

import { useState, useEffect } from 'react';
import styles from "../../styles/perfil.module.css";

interface Device {
  id: number;
  name: string;
  icon: string;
  connected: boolean;
}

export default function Profile() {
  const [address, setAddress] = useState('');
  const [homeName, setHomeName] = useState('');
  const [newDeviceId, setNewDeviceId] = useState('');
  const [newDeviceNickname, setNewDeviceNickname] = useState('');
  const [devices, setDevices] = useState<Device[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<{type: 'success' | 'error', text: string} | null>(null);
  const [showUserMenu, setShowUserMenu] = useState(false);


  // Cargar datos del perfil y dispositivos al montar el componente
  useEffect(() => {
    cargarDatos();
  }, []);

  // Cerrar menú de usuario al hacer clic fuera
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      const target = event.target as HTMLElement;
      if (!target.closest('.user-menu-container')) {
        setShowUserMenu(false);
      }
    };

    if (showUserMenu) {
      document.addEventListener('click', handleClickOutside);
    }

    return () => {
      document.removeEventListener('click', handleClickOutside);
    };
  }, [showUserMenu]);

  const cargarDatos = async () => {
    try {
      setLoading(true);

      // Una sola llamada GET para obtener perfil y dispositivos
      const response = await fetch('http://localhost:5000/perfil', {
        credentials: 'include',
      });
      
      if (response.status === 401) {
        window.location.href = '/login';
        return;
      }
      
      const data = await response.json();
      
      if (data.success) {
        // Cargar datos del hogar
        if (data.hogar) {
          setAddress(data.hogar.direccion || '');
          setHomeName(data.hogar.nombre_hogar || '');
        }
        
        // Cargar dispositivos
        setDevices(data.dispositivos || []);
      }
      
    } catch (error) {
      console.error('Error al cargar datos:', error);
      mostrarMensaje('error', 'Error al cargar los datos');
    } finally {
      setLoading(false);
    }
  };

  const mostrarMensaje = (type: 'success' | 'error', text: string) => {
    setMessage({ type, text });
    setTimeout(() => setMessage(null), 5000);
  };

  const handleProfileSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!address || !homeName) {
      mostrarMensaje('error', 'La dirección y el nombre del hogar son requeridos');
      return;
    }

    try {
      setSaving(true);
      
      const response = await fetch('http://localhost:5000/perfil', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          
        },
        credentials: 'include',
        body: JSON.stringify({
          address,
          nombre_hogar: homeName
        })
      });

      const data = await response.json();
      
      if (data.success) {
        mostrarMensaje('success', data.message);
      } else {
        mostrarMensaje('error', data.error || 'Error al guardar el perfil');
      }
    } catch (error) {
      console.error('Error al guardar perfil:', error);
      mostrarMensaje('error', 'Error al conectar con el servidor');
    } finally {
      setSaving(false);
    }
  };

  const handleDeviceRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!newDeviceId || !newDeviceNickname) {
      mostrarMensaje('error', 'Ingresa el ID y el apodo del dispositivo');
      return;
    }

    try {
      setSaving(true);
      
      const response = await fetch('http://localhost:5000/perfil', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({
          deviceId: newDeviceId,
          nickname: newDeviceNickname
        })
      });

      const data = await response.json();
      
      if (data.success) {
        setDevices([...devices, data.dispositivo]);
        setNewDeviceId('');
        setNewDeviceNickname('');
        mostrarMensaje('success', 'Dispositivo registrado exitosamente');
      } else {
        mostrarMensaje('error', data.error || 'Error al registrar el dispositivo');
      }
    } catch (error) {
      console.error('Error al registrar dispositivo:', error);
      mostrarMensaje('error', 'Error al conectar con el servidor');
    } finally {
      setSaving(false);
    }
  };

  const handleDeleteDevice = async (id: number) => {
    if (!confirm('¿Estás seguro de que deseas eliminar este dispositivo?')) {
      return;
    }

    try {
      const response = await fetch(`http://localhost:5000/perfil/dispositivo/${id}`, {
        method: 'DELETE',
        credentials: 'include',
      });

      const data = await response.json();
      
      if (data.success) {
        setDevices(devices.filter(device => device.id !== id));
        mostrarMensaje('success', 'Dispositivo eliminado exitosamente');
      } else {
        mostrarMensaje('error', data.error || 'Error al eliminar el dispositivo');
      }
    } catch (error) {
      console.error('Error al eliminar dispositivo:', error);
      mostrarMensaje('error', 'Error al conectar con el servidor');
    }
  };

  const handleToggleConnection = async (id: number) => {
    try {
      // Encontrar el dispositivo actual
      const device = devices.find((d) => d.id === id);
      if (!device) return;

      // Cambiar el estado localmente primero
      const updatedDevices = devices.map((d) =>
        d.id === id ? { ...d, connected: !d.connected } : d
      );
      setDevices(updatedDevices);

      // Enviar la actualización al backend
      const response = await fetch(`http://localhost:5000/perfil/dispositivo/${id}/estado`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({ estado_activo: !device.connected }),
      });

      const data = await response.json();

      if (!data.success) {
        // Si falla, revertir el cambio
        setDevices(devices);
        mostrarMensaje("error", data.error || "No se pudo actualizar el estado");
      } else {
        mostrarMensaje("success", `Dispositivo ${!device.connected ? "conectado" : "desconectado"}`);
      }
    } catch (error) {
      console.error("Error al cambiar estado:", error);
      mostrarMensaje("error", "Error al conectar con el servidor");
    }
  };

  const handleDeviceNameChange = async (id: number, newName: string) => {
    // Actualizar localmente de inmediato para mejor UX
    setDevices(devices.map(device => 
      device.id === id ? { ...device, name: newName } : device
    ));

    try {
      const response = await fetch(`http://localhost:5000/perfil/dispositivo/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          credentials: 'include',
        },
        body: JSON.stringify({ name: newName })
      });

      const data = await response.json();
      
      if (!data.success) {
        // Si falla, revertir el cambio
        cargarDatos();
        mostrarMensaje('error', data.error || 'Error al actualizar el dispositivo');
      }
    } catch (error) {
      console.error('Error al actualizar dispositivo:', error);
      cargarDatos();
    }
  };

  if (loading) {
    return (
      <div className={styles.container}>
        <div style={{ 
          display: 'flex', 
          justifyContent: 'center', 
          alignItems: 'center', 
          height: '100vh',
          fontSize: '1.25rem',
          color: '#6B7280'
        }}>
          Cargando...
        </div>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      {/* Header */}
      <header className={styles.header}>
        <div className={styles.headerContent}>
          <div className={styles.logo}>
            <div className={styles.logoIcon}>
              <svg fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1h-2v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"></path>
              </svg>
            </div>
            <h1 className={styles.logoText}>EcoEnergy</h1>
          </div>
          <nav className={styles.nav}>
            <a href="/home" className={styles.navLink}>Dashboard</a>
            <a href="/reportes" className={styles.navLink}>Reports</a>
            <a href="/perfil" className={styles.navLinkActive}>Profile</a>
          </nav>
          <div className={styles.headerActions}>
            <button className={styles.notificationButton} title="Notificaciones">
              🔔
            </button>
            <div className="user-menu-container" style={{ position: 'relative' }}>
              <button 
                className={styles.avatar}
                onClick={() => setShowUserMenu(!showUserMenu)}
                style={{
                  backgroundImage: 'url("https://lh3.googleusercontent.com/aida-public/AB6AXuBqNo8fjfebe_H0I5zh8Fvrbtov-mVmsTd8fa-uhbH9zFVol60RO1YFiXKDnaYuqEvFvzosAfQHITzbl_XnkMOl7Mj6bdHGkiArUnzlzAA-283ck-z-IdS13en693-eVl1R21SdhTnNhGrfR2e4tL8qTaFtvEz782idrxUUqsPXpiFG8AecB3RWIUD8B_4nsKdkyPxIqJPn6Yp8BCLauwRCIpKZU5Iky9mRb27BtIhefRYg6c35py4fXq9x4ctwr81GnuoY51uD47cB")',
                  border: 'none',
                  cursor: 'pointer'
                }}
              />
              
              {/* Menú desplegable del usuario */}
              {showUserMenu && (
                <div style={{
                  position: 'absolute',
                  top: '3rem',
                  right: '0',
                  backgroundColor: 'white',
                  borderRadius: '0.5rem',
                  boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
                  border: '1px solid #E5E7EB',
                  minWidth: '200px',
                  zIndex: 50
                }}>
                  <div style={{ padding: '0.75rem 1rem', borderBottom: '1px solid #E5E7EB' }}>
                    <p style={{ fontWeight: '600', color: '#1F2937', marginBottom: '0.25rem' }}>
                      {homeName || 'Mi Hogar'}
                    </p>
                    <p style={{ fontSize: '0.875rem', color: '#6B7280' }}>
                      {address || 'Sin dirección'}
                    </p>
                  </div>
                  <div style={{ padding: '0.5rem 0' }}>
                    <a 
                      href="/perfil" 
                      style={{ 
                        display: 'block',
                        padding: '0.75rem 1rem',
                        color: '#10B981',
                        fontSize: '0.875rem',
                        fontWeight: '500',
                        textDecoration: 'none',
                        backgroundColor: '#F0FDF4'
                      }}
                    >
                      ⚙️ Mi Perfil
                    </a>
                    <a 
                      href="/home" 
                      style={{ 
                        display: 'block',
                        padding: '0.75rem 1rem',
                        color: '#6B7280',
                        fontSize: '0.875rem',
                        textDecoration: 'none'
                      }}
                      onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#F9FAFB'}
                      onMouseLeave={(e) => e.currentTarget.style.backgroundColor = 'transparent'}
                    >
                      📊 Dashboard
                    </a>
                    <a 
                      href="/reportes" 
                      style={{ 
                        display: 'block',
                        padding: '0.75rem 1rem',
                        color: '#6B7280',
                        fontSize: '0.875rem',
                        textDecoration: 'none'
                      }}
                      onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#F9FAFB'}
                      onMouseLeave={(e) => e.currentTarget.style.backgroundColor = 'transparent'}
                    >
                      📈 Reportes
                    </a>
                  </div>
                  <div style={{ borderTop: '1px solid #E5E7EB', padding: '0.5rem 0' }}>
                    <button 
                      onClick={() => {
                        // Aquí puedes agregar la lógica de logout
                        window.location.href = '/login';
                      }}
                      style={{ 
                        display: 'block',
                        width: '100%',
                        padding: '0.75rem 1rem',
                        color: '#EF4444',
                        fontSize: '0.875rem',
                        fontWeight: '500',
                        textAlign: 'left',
                        border: 'none',
                        backgroundColor: 'transparent',
                        cursor: 'pointer'
                      }}
                      onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#FEF2F2'}
                      onMouseLeave={(e) => e.currentTarget.style.backgroundColor = 'transparent'}
                    >
                      🚪 Cerrar Sesión
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Mensaje de notificación */}
      {message && (
        <div style={{
          position: 'fixed',
          top: '5rem',
          right: '1rem',
          padding: '1rem 1.5rem',
          borderRadius: '0.5rem',
          backgroundColor: message.type === 'success' ? '#10B981' : '#EF4444',
          color: 'white',
          fontWeight: '600',
          zIndex: 50,
          boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)'
        }}>
          {message.text}
        </div>
      )}

      {/* Main Content */}
      <main className={styles.main}>
        <div className={styles.mainContent}>
          {/* Page Heading */}
          <div className={styles.pageHeading}>
            <h1 className={styles.pageTitle}>Mi Perfil y Dispositivos</h1>
            <p className={styles.pageDescription}>
              Gestiona la información de tu hogar y monitorea tus dispositivos conectados.
            </p>
          </div>

          <div className={styles.grid}>
            {/* Left Column */}
            <div className={styles.leftColumn}>
              {/* Profile Section */}
              <section className={styles.card}>
                <div className={styles.cardHeader}>
                  <h2 className={styles.cardTitle}>Perfil del Hogar</h2>
                </div>
                <div className={styles.cardBody}>
                  <form onSubmit={handleProfileSubmit} className={styles.profileForm}>
                    <div className={styles.formGroupFull}>
                      <label className={styles.formLabel}>
                        <span className={styles.labelText}>Nombre del Hogar</span>
                        <input
                          type="text"
                          className={styles.formInput}
                          placeholder="Ej: Mi Casa"
                          value={homeName}
                          onChange={(e) => setHomeName(e.target.value)}
                          required
                        />
                      </label>
                    </div>
                    <div className={styles.formGroupFull}>
                      <label className={styles.formLabel}>
                        <span className={styles.labelText}>Dirección Completa</span>
                        <input
                          type="text"
                          className={styles.formInput}
                          placeholder="Ej: Calle 50 #45-32, Medellín, Antioquia"
                          value={address}
                          onChange={(e) => setAddress(e.target.value)}
                          required
                        />
                      </label>
                    </div>
                    <div className={styles.formActions}>
                      <button 
                        type="submit" 
                        className={styles.primaryButton}
                        disabled={saving}
                      >
                        {saving ? 'Guardando...' : 'Guardar Cambios'}
                      </button>
                    </div>
                  </form>
                </div>
              </section>

              {/* Devices Section */}
              <section className={styles.card}>
                <div className={styles.cardHeader}>
                  <h2 className={styles.cardTitle}>Mis Dispositivos</h2>
                </div>
                <div className={styles.cardBody}>
                  {devices.length === 0 ? (
                    <p style={{ color: '#6B7280', textAlign: 'center', padding: '2rem' }}>
                      No tienes dispositivos registrados. Registra uno usando el formulario de la derecha.
                    </p>
                  ) : (
                    <ul className={styles.deviceList}>
                      {devices.map((device) => (
                        <li key={device.id} className={styles.deviceItem}>
                          <div className={`${styles.deviceIcon} ${device.connected ? styles.deviceIconConnected : styles.deviceIconDisconnected}`}>
                            <span style={{ fontSize: '1.5rem' }}>
                              {device.icon === 'lightbulb' ? '💡' : 
                               device.icon === 'tv' ? '📺' : 
                               device.icon === 'coffee_maker' ? '☕' : 
                               device.icon === 'air' ? '🌀' : '🔌'}
                            </span>
                          </div>
                          <div className={styles.deviceInfo}>
                            <input
                              type="text"
                              className={styles.deviceNameInput}
                              value={device.name}
                              onChange={(e) => handleDeviceNameChange(device.id, e.target.value)}
                            />
                          </div>
                          <div className={`${styles.deviceStatus} ${device.connected ? styles.deviceStatusConnected : styles.deviceStatusDisconnected}`}>
                            <div className={styles.statusDot}></div>
                            <span>{device.connected ? 'Conectado' : 'Desconectado'}</span>
                          </div>

                          {/* 🔘 Botón para cambiar estado */}
                          <button
                            onClick={() => handleToggleConnection(device.id)}
                            className={styles.toggleButton}
                            title={device.connected ? "Desconectar" : "Conectar"}
                            style={{
                              backgroundColor: device.connected ? "#EF4444" : "#10B981",
                              color: "white",
                              border: "none",
                              borderRadius: "0.5rem",
                              padding: "0.5rem 1rem",
                              cursor: "pointer",
                              fontSize: "0.875rem",
                              fontWeight: 600,
                            }}
                          >
                            {device.connected ? "Desconectar" : "Conectar"}
                          </button>
                          <button
                            className={styles.deleteButton}
                            onClick={() => handleDeleteDevice(device.id)}
                            title="Eliminar dispositivo"
                          >
                            🗑️
                          </button>

                        </li>
                      ))}
                    </ul>
                  )}
                </div>
              </section>
            </div>

            {/* Right Column - Register Device */}
            <aside className={styles.rightColumn}>
              <div className={styles.card}>
                <div className={styles.cardHeader}>
                  <h2 className={styles.cardTitle}>Registrar Nuevo Tomacorriente</h2>
                </div>
                <div className={styles.cardBody}>
                  <form onSubmit={handleDeviceRegister} className={styles.registerForm}>
                    <label className={styles.formLabel}>
                      <span className={styles.labelText}>ID del Dispositivo</span>
                      <input
                        type="text"
                        className={styles.formInput}
                        placeholder="Ingresa el código del dispositivo"
                        value={newDeviceId}
                        onChange={(e) => setNewDeviceId(e.target.value)}
                        required
                      />
                    </label>
                    <label className={styles.formLabel}>
                      <span className={styles.labelText}>Apodo</span>
                      <input
                        type="text"
                        className={styles.formInput}
                        placeholder="Ej: Cargador del móvil"
                        value={newDeviceNickname}
                        onChange={(e) => setNewDeviceNickname(e.target.value)}
                        required
                      />
                    </label>
                    <button 
                      type="submit" 
                      className={styles.primaryButton}
                      disabled={saving}
                    >
                      {saving ? 'Registrando...' : 'Registrar Tomacorriente'}
                    </button>
                  </form>
                </div>
              </div>
            </aside>
          </div>
        </div>
      </main>
    </div>
  );
}