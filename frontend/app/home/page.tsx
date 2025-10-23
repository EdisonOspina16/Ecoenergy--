'use client';

import { useState } from 'react';
import styles from "../../styles/home.module.css";

export default function Home() {
  const [timeRange, setTimeRange] = useState('day');

  return (
    <div className={styles.container}>
      {/* Header */}
      <header className={styles.header}>
        <div className={styles.headerContent}>
          <div className={styles.logo}>
            <span className={`material-icons ${styles.logoIcon}`}>lightbulb</span>
            <span className={styles.logoText}>ECOENERGY</span>
          </div>
          <div className={styles.headerActions}>
            <span className={styles.userName}>Hola, Usuario</span>
            <button className={styles.logoutButton}>
              <span className="material-icons">logout</span>
              <span className={styles.logoutText}>Cerrar Sesión</span>
            </button>
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
              <h1 className={styles.cardTitle}>Resumen de Consumo [Mi Hogar]</h1>
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