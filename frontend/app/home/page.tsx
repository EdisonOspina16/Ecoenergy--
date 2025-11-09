'use client';

import { useState, useEffect } from 'react';
import styles from "../../styles/home.module.css";

export default function Home() {
  const [timeRange, setTimeRange] = useState('day');
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [homeName, setHomeName] = useState('Mi Hogar');
  const [address, setAddress] = useState('Sin dirección');

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

  // Cargar datos del perfil
  useEffect(() => {
    const cargarPerfil = async () => {
      try {
        const response = await fetch('http://localhost:5000/perfil', {
          credentials: 'include',
        });
        
        if (response.status === 401) {
          window.location.href = '/login';
          return;
        }
        
        const data = await response.json();
        
        if (data.success && data.hogar) {
          setHomeName(data.hogar.nombre_hogar || 'Mi Hogar');
          setAddress(data.hogar.direccion || 'Sin dirección');
        }
      } catch (error) {
        console.error('Error al cargar perfil:', error);
      }
    };

    cargarPerfil();
  }, []);

  return (
    <div className={styles.container}>
      {/* Header */}
      <header className={styles.header}>
        <div className={styles.headerContent}>
          <div className={styles.logo}>
            <span className={`material-icons ${styles.logoIcon}`}>lightbulb</span>
            <span className={styles.logoText}>ECOENERGY</span>
          </div>
          <nav style={{ display: 'flex', gap: '2rem' }}>
            <a 
              href="/dashboard" 
              style={{ 
                color: '#10B981', 
                textDecoration: 'none', 
                fontWeight: '600',
                borderBottom: '2px solid #10B981',
                paddingBottom: '0.25rem'
              }}
            >
              Dashboard
            </a>
            <a 
              href="/reportes" 
              style={{ 
                color: '#6B7280', 
                textDecoration: 'none', 
                fontWeight: '500'
              }}
            >
              Reports
            </a>
            <a 
              href="/perfil" 
              style={{ 
                color: '#6B7280', 
                textDecoration: 'none', 
                fontWeight: '500'
              }}
            >
              Profile
            </a>
          </nav>
          <div className={styles.headerActions}>
            <button 
              style={{
                background: 'none',
                border: 'none',
                fontSize: '1.5rem',
                cursor: 'pointer',
                padding: '0.5rem'
              }}
              title="Notificaciones"
            >
              🔔
            </button>
            <div className="user-menu-container" style={{ position: 'relative' }}>
              <button 
                onClick={() => setShowUserMenu(!showUserMenu)}
                style={{
                  width: '2.5rem',
                  height: '2.5rem',
                  borderRadius: '50%',
                  backgroundImage: 'url("https://lh3.googleusercontent.com/aida-public/AB6AXuBqNo8fjfebe_H0I5zh8Fvrbtov-mVmsTd8fa-uhbH9zFVol60RO1YFiXKDnaYuqEvFvzosAfQHITzbl_XnkMOl7Mj6bdHGkiArUnzlzAA-283ck-z-IdS13en693-eVl1R21SdhTnNhGrfR2e4tL8qTaFtvEz782idrxUUqsPXpiFG8AecB3RWIUD8B_4nsKdkyPxIqJPn6Yp8BCLauwRCIpKZU5Iky9mRb27BtIhefRYg6c35py4fXq9x4ctwr81GnuoY51uD47cB")',
                  backgroundSize: 'cover',
                  backgroundPosition: 'center',
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
                      {homeName}
                    </p>
                    <p style={{ fontSize: '0.875rem', color: '#6B7280' }}>
                      {address}
                    </p>
                  </div>
                  <div style={{ padding: '0.5rem 0' }}>
                    <a 
                      href="/dashboard" 
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
                    <a 
                      href="/perfil" 
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
                      ⚙️ Mi Perfil
                    </a>
                  </div>
                  <div style={{ borderTop: '1px solid #E5E7EB', padding: '0.5rem 0' }}>
                    <button 
                      onClick={() => {
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

      {/* Main Content */}
      <main className={styles.main}>
        <div className={styles.grid}>
          {/* Left Column */}
          <div className={styles.leftColumn}>
            {/* Consumption Summary */}
            <div className={styles.card}>
              <h1 className={styles.cardTitle}>Resumen de Consumo [{homeName}]</h1>
              <p className={styles.summaryValue}>
                1.25 <span className={styles.summaryUnit}>kWh</span>
              </p>
              <p className={styles.updateTime}>Última actualización: hace 3 segundos</p>
            </div>

            {/* Consumption Trend */}
            <div className={styles.card}>
              <div className={styles.cardHeader}>
                <h2 className={styles.cardTitle}>Tendencia de Consumo</h2>
                <div className={styles.timeRangeButtons}>
                  <button
                    onClick={() => setTimeRange('day')}
                    className={`${styles.timeButton} ${
                      timeRange === 'day' ? styles.timeButtonActive : ''
                    }`}
                  >
                    Día
                  </button>
                  <button
                    onClick={() => setTimeRange('week')}
                    className={`${styles.timeButton} ${
                      timeRange === 'week' ? styles.timeButtonActive : ''
                    }`}
                  >
                    Semana
                  </button>
                  <button
                    onClick={() => setTimeRange('month')}
                    className={`${styles.timeButton} ${
                      timeRange === 'month' ? styles.timeButtonActive : ''
                    }`}
                  >
                    Mes
                  </button>
                </div>
              </div>
              <div className={styles.chartPlaceholder}>
                <p>Gráfico de consumo histórico</p>
              </div>
            </div>

            {/* Device Consumption */}
            <div className={styles.card}>
              <div className={styles.cardHeader}>
                <h2 className={styles.cardTitle}>Consumo por Dispositivo</h2>
                <button className={styles.exportButton}>
                  <span className="material-icons">download</span>
                  Exportar a Hojas de cálculo
                </button>
              </div>
              <div className={styles.deviceList}>
                {/* TV */}
                <div className={styles.deviceItem}>
                  <div className={styles.deviceInfo}>
                    <span className={`material-icons ${styles.deviceIcon}`}>tv</span>
                    <div>
                      <p className={styles.deviceName}>Televisor Sala</p>
                      <p className={styles.deviceConsumption}>0.15 kWh</p>
                    </div>
                  </div>
                  <div className={styles.deviceActions}>
                    <div className={styles.deviceStatus}>
                      <div className={`${styles.statusDot} ${styles.statusDotOn}`}></div>
                      <span>Encendido</span>
                    </div>
                    <button className={`${styles.powerButton} ${styles.powerButtonOff}`}>
                      Apagar
                    </button>
                  </div>
                </div>

                {/* Fridge */}
                <div className={styles.deviceItem}>
                  <div className={styles.deviceInfo}>
                    <span className={`material-icons ${styles.deviceIcon}`}>kitchen</span>
                    <div>
                      <p className={styles.deviceName}>Nevera</p>
                      <p className={styles.deviceConsumption}>0.80 kWh</p>
                    </div>
                  </div>
                  <div className={styles.deviceActions}>
                    <div className={styles.deviceStatus}>
                      <div className={`${styles.statusDot} ${styles.statusDotOn}`}></div>
                      <span>Encendido</span>
                    </div>
                    <button
                      className={`${styles.powerButton} ${styles.powerButtonOff}`}
                      disabled
                    >
                      Apagar
                    </button>
                  </div>
                </div>

                {/* AC */}
                <div className={styles.deviceItem}>
                  <div className={styles.deviceInfo}>
                    <span className={`material-icons ${styles.deviceIcon}`}>air</span>
                    <div>
                      <p className={styles.deviceName}>Aire Acondicionado</p>
                      <p className={styles.deviceConsumption}>0.00 kWh</p>
                    </div>
                  </div>
                  <div className={styles.deviceActions}>
                    <div className={styles.deviceStatus}>
                      <div className={`${styles.statusDot} ${styles.statusDotOff}`}></div>
                      <span>Apagado</span>
                    </div>
                    <button className={`${styles.powerButton} ${styles.powerButtonDisabled}`} disabled>
                      Apagar
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Right Column */}
          <div className={styles.rightColumn}>
            {/* Recommendations */}
            <div className={styles.card}>
              <h2 className={styles.cardTitle}>Recomendaciones</h2>
              <div className={styles.recommendations}>
                <div className={`${styles.alert} ${styles.alertDanger}`}>
                  <p className={styles.alertDangerText}>Pico Inusual Detectado</p>
                  <p className={styles.alertDangerDesc}>
                    Se detectó un consumo anómalo a las 3:00 AM.
                  </p>
                </div>
                <div className={`${styles.alert} ${styles.alertSuccess}`}>
                  <p className={styles.alertSuccessText}>
                    Tu <span className={styles.bold}>Nevera</span> está consumiendo 15% más de lo
                    esperado. Revisa la temperatura o el sellado de las puertas.
                  </p>
                </div>
              </div>
            </div>

            {/* Savings */}
            <div className={styles.card}>
              <div className={styles.cardHeader}>
                <h2 className={styles.cardTitle}>Tu Ahorro</h2>
                <button className={styles.exportButton}>
                  <span className="material-icons">download</span>
                  Exportar
                </button>
              </div>
              <div className={styles.savingsGrid}>
                <div className={`${styles.savingsCard} ${styles.savingsCardBlue}`}>
                  <p className={`${styles.savingsLabel} ${styles.savingsLabelBlue}`}>
                    Ahorro Financiero Proyectado
                  </p>
                  <p className={`${styles.savingsValue} ${styles.savingsValueBlue}`}>
                    25.000 COP/mes
                  </p>
                </div>
                <div className={`${styles.savingsCard} ${styles.savingsCardGreen}`}>
                  <p className={`${styles.savingsLabel} ${styles.savingsLabelGreen}`}>
                    Impacto Ambiental
                  </p>
                  <p className={`${styles.savingsValue} ${styles.savingsValueGreen}`}>
                    10 kg CO₂ menos
                  </p>
                </div>
                <div className={`${styles.savingsCard} ${styles.savingsCardAmber}`}>
                  <p className={`${styles.savingsLabel} ${styles.savingsLabelAmber}`}>
                    Indicador Didáctico
                  </p>
                  <p className={`${styles.savingsValue} ${styles.savingsValueAmber}`}>
                    Equivalente a 5 horas menos de AC
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}