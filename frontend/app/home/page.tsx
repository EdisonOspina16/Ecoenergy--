'use client';

import { useState, useEffect } from 'react';
import styles from "../../styles/home.module.css";

export default function Home() {
  const [timeRange, setTimeRange] = useState('day');
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [homeName, setHomeName] = useState('Mi Hogar');
  const [address, setAddress] = useState('Sin dirección');
  const [totalConsumo, setTotalConsumo] = useState(0);
  const [lastUpdate, setLastUpdate] = useState('');
  const [loading, setLoading] = useState(true);
  const [chartData, setChartData] = useState<any[]>([]);
  const [chartLoading, setChartLoading] = useState(false);
  const [devices, setDevices] = useState<any[]>([]);
  const [loadingDevices, setLoadingDevices] = useState(true);

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

  // Cargar datos de consumo total
  useEffect(() => {
    const cargarConsumo = async () => {
      try {
        setLoading(true);
        const response = await fetch('http://localhost:5000/home', {
          credentials: 'include',
        });

        if (!response.ok) {
          throw new Error('Error al obtener datos de consumo');
        }

        const data = await response.json();

        if (data.total_consumo_kwh !== undefined) {
          setTotalConsumo(data.total_consumo_kwh);
          setLastUpdate(new Date().toLocaleString('es-ES'));
        }
      } catch (error) {
        console.error('Error al cargar consumo:', error);
      } finally {
        setLoading(false);
      }
    };

    cargarConsumo();
    const interval = setInterval(cargarConsumo, 30000);
    return () => clearInterval(interval);
  }, []);

  // Cargar datos históricos para gráfico
  useEffect(() => {
    const cargarDatosHistoricos = async () => {
      try {
        setChartLoading(true);
        const response = await fetch(
          `http://localhost:5000/consumo-historico?rango=${timeRange}`,
          { credentials: 'include' }
        );

        if (!response.ok) {
          throw new Error('Error al obtener datos históricos');
        }

        const data = await response.json();

        if (data.success && data.datos) {
          setChartData(data.datos);
        }
      } catch (error) {
        console.error('Error al cargar datos históricos:', error);
      } finally {
        setChartLoading(false);
      }
    };

    cargarDatosHistoricos();
  }, [timeRange]);

  // Cargar dispositivos desde backend
  useEffect(() => {
    const cargarDispositivos = async () => {
      try {
        const response = await fetch('http://localhost:5000/dispositivos');
        const data = await response.json();

        if (data.success) {
          // Mapear dispositivos a la estructura que espera el frontend
          const dispositivosMapeados = data.dispositivos.map((d: any) => ({
            nombre: d.nombre,
            consumo: d.consumo,
            estado: d.estado,
          }));

          setDevices(dispositivosMapeados);
        } else {
          setDevices([]);
        }
      } catch (error) {
        console.error('Error al cargar dispositivos:', error);
        setDevices([]);
      } finally {
        setLoadingDevices(false);
      }
    };

    cargarDispositivos();
  }, []);

  // Render del gráfico SVG
  const renderChart = () => {
    if (chartLoading) {
      return (
        <div className={styles.centered}>
          <p>Cargando datos...</p>
        </div>
      );
    }

    if (!chartData || chartData.length === 0) {
      return (
        <div className={styles.centered}>
          <p>No hay datos disponibles para este período</p>
        </div>
      );
    }

    const maxConsumo = Math.max(...chartData.map((d: any) => d.consumo));
    const minConsumo = Math.min(...chartData.map((d: any) => d.consumo));
    const range = maxConsumo - minConsumo || 1;

    return (
      <div style={{ padding: '1rem', height: '300px' }}>
        <svg width="100%" height="100%" viewBox="0 0 800 250">
          {[0, 1, 2, 3, 4].map((i) => (
            <g key={i}>
              <line
                x1="50"
                y1={50 + i * 50}
                x2="750"
                y2={50 + i * 50}
                stroke="#E5E7EB"
                strokeWidth="1"
              />
              <text
                x="35"
                y={55 + i * 50}
                fill="#6B7280"
                fontSize="12"
                textAnchor="end"
              >
                {(maxConsumo - (i * range) / 4).toFixed(1)}
              </text>
            </g>
          ))}

          <polyline
            fill="none"
            stroke="#10B981"
            strokeWidth="3"
            points={chartData
              .map((d: any, i: number) => {
                const x = 50 + (i * (700 / (chartData.length - 1 || 1)));
                const y = 250 - ((d.consumo - minConsumo) / range) * 200;
                return `${x},${y}`;
              })
              .join(' ')}
          />

          {chartData.map((d: any, i: number) => {
            const x = 50 + (i * (700 / (chartData.length - 1 || 1)));
            const y = 250 - ((d.consumo - minConsumo) / range) * 200;
            return (
              <g key={i}>
                <circle cx={x} cy={y} r="4" fill="#10B981" />
                {(chartData.length <= 12 || i % Math.ceil(chartData.length / 12) === 0) && (
                  <text
                    x={x}
                    y="270"
                    fill="#6B7280"
                    fontSize="11"
                    textAnchor="middle"
                  >
                    {d.periodo}
                  </text>
                )}
              </g>
            );
          })}

          <text
            x="400"
            y="295"
            fill="#6B7280"
            fontSize="14"
            textAnchor="middle"
            fontWeight="600"
          >
            {timeRange === 'day'
              ? 'Hora del día'
              : timeRange === 'week'
              ? 'Día de la semana'
              : 'Día del mes'}
          </text>
          <text
            x="15"
            y="150"
            fill="#6B7280"
            fontSize="14"
            textAnchor="middle"
            fontWeight="600"
            transform="rotate(-90, 15, 150)"
          >
            Consumo (W)
          </text>
        </svg>
      </div>
    );
  };

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
            <a href="/home" className={styles.navActive}>Dashboard</a>
            <a href="/reportes" className={styles.navLink}>Reports</a>
            <a href="/perfil" className={styles.navLink}>Profile</a>
          </nav>

          <div className={styles.headerActions}>
            <button title="Notificaciones" className={styles.notificationButton}>
              🔔
            </button>
            <div className="user-menu-container" style={{ position: 'relative' }}>
              <button
                onClick={() => setShowUserMenu(!showUserMenu)}
                className={styles.profileButton}
              />
              {showUserMenu && (
                <div className={styles.userMenu}>
                  <div className={styles.userMenuHeader}>
                    <p className={styles.userMenuTitle}>{homeName}</p>
                    <p className={styles.userMenuSubtitle}>{address}</p>
                  </div>
                  <div className={styles.userMenuBody}>
                    <a href="/home">📊 Dashboard</a>
                    <a href="/reportes">📈 Reportes</a>
                    <a href="/perfil">⚙️ Mi Perfil</a>
                  </div>
                  <div className={styles.userMenuFooter}>
                    <button onClick={() => (window.location.href = '/login')}>
                      🚪 Cerrar Sesión
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Main */}
      <main className={styles.main}>
        <div className={styles.grid}>
          {/* Left Column */}
          <div className={styles.leftColumn}>
            {/* Resumen de Consumo */}
            <div className={styles.card}>
              <h1 className={styles.cardTitle}>Resumen de Consumo [{homeName}]</h1>
              {loading ? (
                <p className={styles.summaryValue}>Cargando...</p>
              ) : (
                <p className={styles.summaryValue}>
                  {totalConsumo.toFixed(2)} <span className={styles.summaryUnit}>kWh</span>
                </p>
              )}
              <p className={styles.updateTime}>
                {lastUpdate ? `Última actualización: ${lastUpdate}` : 'Actualizando...'}
              </p>
            </div>

            {/* Tendencia */}
            <div className={styles.card}>
              <div className={styles.cardHeader}>
                <h2 className={styles.cardTitle}>Tendencia de Consumo</h2>
                <div className={styles.timeRangeButtons}>
                  {['day', 'week', 'month'].map((range) => (
                    <button
                      key={range}
                      onClick={() => setTimeRange(range)}
                      className={`${styles.timeButton} ${
                        timeRange === range ? styles.timeButtonActive : ''
                      }`}
                    >
                      {range === 'day' ? 'Día' : range === 'week' ? 'Semana' : 'Mes'}
                    </button>
                  ))}
                </div>
              </div>
              <div className={styles.chartPlaceholder}>{renderChart()}</div>
            </div>

            {/* Consumo por Dispositivo */}
            <div className={styles.card}>
              <div className={styles.cardHeader}>
                <h2 className={styles.cardTitle}>Consumo por Dispositivo</h2>
                <button className={styles.exportButton}>
                  <span className="material-icons">download</span>
                  Exportar a Hojas de cálculo
                </button>
              </div>

              <div className={styles.deviceList}>
                {loadingDevices ? (
                  <p>Cargando dispositivos...</p>
                ) : devices.length === 0 ? (
                  <p>No hay dispositivos registrados.</p>
                ) : (
                  devices.map((device, index) => (
                    <div key={index} className={styles.deviceItem}>
                      <div className={styles.deviceInfo}>
                        <span className={`material-icons ${styles.deviceIcon}`}>
                          {device.nombre.toLowerCase().includes('tv')
                            ? 'tv'
                            : device.nombre.toLowerCase().includes('nevera')
                            ? 'kitchen'
                            : device.nombre.toLowerCase().includes('aire')
                            ? 'air'
                            : 'devices'}
                        </span>
                        <div>
                          <p className={styles.deviceName}>{device.nombre}</p>
                          <p className={styles.deviceConsumption}>
                            {device.consumo.toFixed(2)} kWh
                          </p>
                        </div>
                      </div>
                      <div className={styles.deviceActions}>
                        <div className={styles.deviceStatus}>
                          <div
                            className={`${styles.statusDot} ${
                              device.estado === 'Encendido'
                                ? styles.statusDotOn
                                : styles.statusDotOff
                            }`}
                          ></div>
                          <span>{device.estado}</span>
                        </div>
                        <button
                          className={`${styles.powerButton} ${
                            device.estado === 'Encendido'
                              ? styles.powerButtonOff
                              : styles.powerButtonDisabled
                          }`}
                          disabled={device.estado !== 'Encendido'}
                        >
                          Apagar
                        </button>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>

          {/* Right Column */}
          <div className={styles.rightColumn}>
            {/* Recomendaciones */}
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

            {/* Ahorro */}
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
