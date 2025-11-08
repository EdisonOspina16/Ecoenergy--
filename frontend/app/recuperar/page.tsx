"use client";

import React, { useState } from "react";
import Head from "next/head";
import styles from "../../styles/login.module.css";
import { API_URL } from "../../config";

export default function Recuperar() {
  const [correo, setCorreo] = useState("");
  const [nuevaContraseña, setNuevaContraseña] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/recuperar`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          credentials: "include",
        },
        body: JSON.stringify({
          correo: correo,
          nueva_contraseña: nuevaContraseña,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setSuccess(data.message);
        setTimeout(() => {
          window.location.href = data.redirect;
        }, 2000);
      } else {
        setError(data.error || "Error al recuperar contraseña");
      }
    } catch (error) {
      console.error("Error en la petición:", error);
      setError("Error al conectar con el servidor");
    } finally {
      setLoading(false);
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
            style={{ color: "#FFD700", fontSize: "42px" }}
          ></i>
        </div>

        <h1>RECUPERAR CONTRASEÑA</h1>
        <p>Ingresa tu correo y nueva contraseña</p>

        {error && (
          <div style={{ 
            color: "#ff4444", 
            backgroundColor: "#ffe6e6", 
            padding: "10px", 
            borderRadius: "5px", 
            marginBottom: "20px",
            textAlign: "center"
          }}>
            {error}
          </div>
        )}

        {success && (
          <div style={{ 
            color: "#00aa00", 
            backgroundColor: "#e6ffe6", 
            padding: "10px", 
            borderRadius: "5px", 
            marginBottom: "20px",
            textAlign: "center"
          }}>
            {success}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className={styles.inputGroup}>
            <i className={`fas fa-envelope ${styles.inputIcon}`}></i>
            <input
              type="email"
              placeholder="Tu correo electrónico"
              required
              className={styles.iconInput}
              value={correo}
              onChange={(e) => setCorreo(e.target.value)}
            />
          </div>

          <div className={styles.inputGroup}>
            <i className={`fas fa-lock ${styles.inputIcon}`}></i>
            <input
              type="password"
              placeholder="Nueva contraseña"
              required
              className={styles.iconInput}
              value={nuevaContraseña}
              onChange={(e) => setNuevaContraseña(e.target.value)}
            />
          </div>

          <button type="submit" disabled={loading}>
            <i className="fas fa-save" style={{ marginRight: "8px" }}></i>
            {loading ? "ACTUALIZANDO..." : "ACTUALIZAR CONTRASEÑA"}
          </button>
        </form>

        <div className={styles.linksContainer}>
          <a href="/login">
            <i className="fas fa-sign-in-alt" style={{ marginRight: "5px" }}></i>
            Volver al inicio de sesión
          </a>
        </div>
      </div>
    </>
  );
}