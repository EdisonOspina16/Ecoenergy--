'use client';

import { useState } from 'react';
import styles from "../../styles/perfil.module.css";

interface Device {
  id: number;
  name: string;
  icon: string;
  connected: boolean;
}

export default function Profile() {
  const [address, setAddress] = useState('Av. Libertador 456');
  const [city, setCity] = useState('Buenos Aires');
  const [postalCode, setPostalCode] = useState('C1428');
  const [residenceType, setResidenceType] = useState('Apartamento');
  const [newDeviceId, setNewDeviceId] = useState('');
  const [newDeviceNickname, setNewDeviceNickname] = useState('');
  
  const [devices, setDevices] = useState<Device[]>([
    { id: 1, name: 'Lámpara del Salón', icon: 'outlet', connected: true },
    { id: 2, name: 'TV del Cuarto', icon: 'tv', connected: true },
    { id: 3, name: 'Cafetera Cocina', icon: 'coffee_maker', connected: false },
  ]);

  const handleProfileSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Perfil guardado:', { address, city, postalCode, residenceType });
  };

  const handleDeviceRegister = (e: React.FormEvent) => {
    e.preventDefault();
    if (newDeviceId && newDeviceNickname) {
      const newDevice: Device = {
        id: devices.length + 1,
        name: newDeviceNickname,
        icon: 'outlet',
        connected: false,
      };
      setDevices([...devices, newDevice]);
      setNewDeviceId('');
      setNewDeviceNickname('');
    }
  };

  const handleDeleteDevice = (id: number) => {
    setDevices(devices.filter(device => device.id !== id));
  };

  const handleDeviceNameChange = (id: number, newName: string) => {
    setDevices(devices.map(device => 
      device.id === id ? { ...device, name: newName } : device
    ));
  };

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
            <a href="#" className={styles.navLink}>Dashboard</a>
            <a href="#" className={styles.navLink}>Reports</a>
            <a href="#" className={styles.navLinkActive}>Profile</a>
          </nav>
          <div className={styles.headerActions}>
            <button className={styles.notificationButton}>
              <span className="material-symbols-outlined">notifications</span>
            </button>
            <div 
              className={styles.avatar}
              style={{backgroundImage: 'url("https://lh3.googleusercontent.com/aida-public/AB6AXuBqNo8fjfebe_H0I5zh8Fvrbtov-mVmsTd8fa-uhbH9zFVol60RO1YFiXKDnaYuqEvFvzosAfQHITzbl_XnkMOl7Mj6bdHGkiArUnzlzAA-283ck-z-IdS13en693-eVl1R21SdhTnNhGrfR2e4tL8qTaFtvEz782idrxUUqsPXpiFG8AecB3RWIUD8B_4nsKdkyPxIqJPn6Yp8BCLauwRCIpKZU5Iky9mRb27BtIhefRYg6c35py4fXq9x4ctwr81GnuoY51uD47cB")'}}
            />
          </div>
        </div>
      </header>

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
                        <span className={styles.labelText}>Dirección</span>
                        <input
                          type="text"
                          className={styles.formInput}
                          placeholder="Ej: Calle Falsa 123"
                          value={address}
                          onChange={(e) => setAddress(e.target.value)}
                        />
                      </label>
                    </div>
                    <div className={styles.formGroup}>
                      <label className={styles.formLabel}>
                        <span className={styles.labelText}>Ciudad</span>
                        <input
                          type="text"
                          className={styles.formInput}
                          placeholder="Ej: Springfield"
                          value={city}
                          onChange={(e) => setCity(e.target.value)}
                        />
                      </label>
                    </div>
                    <div className={styles.formGroup}>
                      <label className={styles.formLabel}>
                        <span className={styles.labelText}>Código Postal</span>
                        <input
                          type="text"
                          className={styles.formInput}
                          placeholder="Ej: 1425"
                          value={postalCode}
                          onChange={(e) => setPostalCode(e.target.value)}
                        />
                      </label>
                    </div>
                    <div className={styles.formGroupFull}>
                      <label className={styles.formLabel}>
                        <span className={styles.labelText}>Tipo de Residencia</span>
                        <select
                          className={styles.formSelect}
                          value={residenceType}
                          onChange={(e) => setResidenceType(e.target.value)}
                        >
                          <option>Casa</option>
                          <option>Apartamento</option>
                          <option>Oficina</option>
                        </select>
                      </label>
                    </div>
                    <div className={styles.formActions}>
                      <button type="submit" className={styles.primaryButton}>
                        Guardar Cambios
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
                  <ul className={styles.deviceList}>
                    {devices.map((device) => (
                      <li key={device.id} className={styles.deviceItem}>
                        <div className={`${styles.deviceIcon} ${device.connected ? styles.deviceIconConnected : styles.deviceIconDisconnected}`}>
                          <span className="material-symbols-outlined">{device.icon}</span>
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
                        <button
                          className={styles.deleteButton}
                          onClick={() => handleDeleteDevice(device.id)}
                        >
                          <span className="material-symbols-outlined">delete</span>
                        </button>
                      </li>
                    ))}
                  </ul>
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
                      />
                    </label>
                    <button type="submit" className={styles.primaryButton}>
                      Registrar Tomacorriente
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
