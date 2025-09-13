"use client";

import { useState } from "react";
import Head from "next/head";
import styles from "../../styles/login.module.css";


export default function Login() {
  const [correo, setCorreo] = useState("");
  const [contraseña, setContraseña] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log("Correo:", correo);
    console.log("Contraseña:", contraseña);
    // conectar el backend en Node.js
  };

  return (
    <>
      <Head>
        <title>Iniciar Sesión - EcoEnergy</title>
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
            className="fas fa-lightbulb"
            style={{ color: "#FFD700", fontSize: "42px" }}
          ></i>
        </div>

        <h1>INICIAR SESIÓN</h1>
        <p>Inicia sesión para continuar con tu experiencia sostenible</p>

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
              placeholder="Tu contraseña"
              required
              className={styles.iconInput}
              value={contraseña}
              onChange={(e) => setContraseña(e.target.value)}
            />
          </div>

          <button type="submit">
            <i className="fas fa-sign-in-alt" style={{ marginRight: "8px" }}></i>
            INGRESAR
          </button>
        </form>

        <div className={styles.linksContainer}>
          <a href="/registro">
            <i className="fas fa-user-plus" style={{ marginRight: "5px" }}></i>
            ¿No tienes cuenta? Regístrate
          </a>

          <a href="/recuperar">
            <i className="fas fa-key" style={{ marginRight: "5px" }}></i>
            ¿Olvidaste tu contraseña?
          </a>
        </div>
      </div>
    </>
  );
}
