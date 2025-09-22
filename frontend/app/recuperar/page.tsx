"use client";

import { useState } from "react";
import Head from "next/head";
import styles from "../../styles/recuperar.module.css";
import { API_URL } from "../../config";

export default function Recuperar() {
  const [correo, setCorreo] = useState("");
  const [mensaje, setMensaje] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const response = await fetch(`${API_URL}/api/auth/recuperar`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: correo,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setMensaje("Se ha enviado un enlace de recuperación a tu correo electrónico");
      } else {
        setMensaje(data.error || "Error al enviar el correo de recuperación");
      }
    } catch (error) {
      console.error("Error en la petición:", error);
      setMensaje("Error al conectar con el servidor");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <Head>
        <title>Recuperar Contraseña - EcoEnergy</title>
        <link
          href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
          rel="stylesheet"
        />
      </Head>

      <header className={styles.header}>
        ECOENERGY
        <span style={{ color: "#FFD700", marginLeft: "10px" }}>
          <i className="fas fa-lightbulb"></i>
        </span>
      </header>

      <div className={styles.container}>
        <div className={`${styles.decoration} ${styles.decoration1}`}></div>
        <div className={`${styles.decoration} ${styles.decoration2}`}></div>

        <div className={styles.icono}>
          <i
            className="fas fa-key"
            style={{ color: "#00796b", fontSize: "42px" }}
          ></i>
        </div>

        <h1>¿Has olvidado la contraseña?</h1>
        <p>Nueva contraseña</p>
        <p className={styles.descripcion}>
          Ingresa tu correo electrónico y te enviaremos un enlace para restablecer tu contraseña
        </p>

        <form onSubmit={handleSubmit}>
          <div className={styles.inputGroup}>
            <label className={styles.label}>CORREO ELECTRÓNICO</label>
            <input
              type="email"
              placeholder="TU@CORREO.COM"
              required
              className={styles.input}
              value={correo}
              onChange={(e) => setCorreo(e.target.value)}
              disabled={isLoading}
            />
          </div>

          <button type="submit" disabled={isLoading}>
            <i className="fas fa-paper-plane" style={{ marginRight: "8px" }}></i>
            {isLoading ? "ENVIANDO..." : "INGRESAR"}
          </button>
        </form>

        {mensaje && (
          <div className={`${styles.mensaje} ${mensaje.includes("Error") ? styles.error : styles.success}`}>
            <i className={mensaje.includes("Error") ? "fas fa-exclamation-circle" : "fas fa-check-circle"} 
               style={{ marginRight: "8px" }}></i>
            {mensaje}
          </div>
        )}

        <div className={styles.linksContainer}>
          <a href="/login">
            <i className="fas fa-arrow-left" style={{ marginRight: "5px" }}></i>
            Volver al inicio de sesión
          </a>

          <a href="/registro">
            <i className="fas fa-user-plus" style={{ marginRight: "5px" }}></i>
            ¿No tienes cuenta? Regístrate
          </a>
        </div>
      </div>
    </>
  );
}