"use client";

import React, { useState } from "react";
import Head from "next/head";
import styles from "../../styles/login.module.css";

export default function Registro() {
  const [nombre, setNombre] = useState("");
  const [apellidos, setApellidos] = useState("");
  const [correo, setCorreo] = useState("");
  const [contraseña, setContraseña] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    console.log("Intentando registro con:", { nombre, apellidos, correo, contraseña: "***" });

    try {
      const response = await fetch("http://localhost:5000/registro", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          credentials: "include",
        },
        body: JSON.stringify({
          nombre: nombre,
          apellidos: apellidos,
          correo: correo,
          contraseña: contraseña,
        }),
      });

      console.log("Response status:", response.status);
      console.log("Response headers:", response.headers);

      if (!response.ok) {
        console.error("Error response:", response.status, response.statusText);
      }

      const data = await response.json();
      console.log("Response data:", data);

      if (response.ok) {
        console.log("Registro exitoso, redirigiendo a:", data.redirect);
        // Redirigir al login
        window.location.href = data.redirect;
      } else {
        console.error("Error en registro:", data.error);
        setError(data.error || "Error al procesar el registro");
      }
    } catch (error) {
      console.error("Error en la petición:", error);
      
      if (error instanceof Error) {
        console.error("Tipo de error:", error.name);
        console.error("Mensaje:", error.message);
        
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
          setError("No se puede conectar con el servidor. Verifica que el backend esté corriendo en http://localhost:5000");
        } else {
          setError("Error al conectar con el servidor: " + error.message);
        }
      } else {
        setError("Error desconocido al conectar con el servidor");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Head>
        <title>Registro - EcoEnergy</title>
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
            className="fas fa-user-plus"
            style={{ color: "#FFD700", fontSize: "42px" }}
          ></i>
        </div>

        <h1>REGISTRO</h1>
        <p>Completa tus datos básicos para crear tu cuenta</p>

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

        <form onSubmit={handleSubmit}>
          <div className={styles.inputGroup}>
            <i className={`fas fa-user ${styles.inputIcon}`}></i>
            <input
              type="text"
              placeholder="Tu nombre"
              required
              className={styles.iconInput}
              value={nombre}
              onChange={(e) => setNombre(e.target.value)}
            />
          </div>

          <div className={styles.inputGroup}>
            <i className={`fas fa-user ${styles.inputIcon}`}></i>
            <input
              type="text"
              placeholder="Tus apellidos"
              required
              className={styles.iconInput}
              value={apellidos}
              onChange={(e) => setApellidos(e.target.value)}
            />
          </div>

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
              placeholder="Tu contraseña"
              required
              className={styles.iconInput}
              value={contraseña}
              onChange={(e) => setContraseña(e.target.value)}
            />
          </div>

          <button type="submit" disabled={loading}>
            <i className="fas fa-check" style={{ marginRight: "8px" }}></i>
            {loading ? "REGISTRANDO..." : "COMPLETAR REGISTRO"}
          </button>
        </form>

        <div className={styles.linksContainer}>
          <a href="/login">
            <i className="fas fa-sign-in-alt" style={{ marginRight: "5px" }}></i>
            ¿Ya tienes cuenta? Inicia sesión
          </a>
        </div>
      </div>
    </>
  );
}