"use client";

import React, { useState, useEffect } from "react";
import Head from "next/head";
import styles from "../styles/login.module.css";
import { API_URL } from "../config";

interface Usuario {
  nombre?: string;
  correo?: string;
  fecha_registro?: string;
  [key: string]: any;
}

export default function Home() {
  const [mensaje, setMensaje] = useState("");
  const [usuario, setUsuario] = useState<Usuario | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    // Obtener mensaje del backend
    fetch(`${API_URL}/`)
      .then(response => response.json())
      .then(data => {
        setMensaje(data.message);
        setLoading(false);
      })
      .catch(error => {
        console.error("Error al obtener mensaje:", error);
        setError("Error al conectar con el servidor");
        setLoading(false);
      });

    // Verificar si hay usuario logueado
    fetch(`${API_URL}/perfil`, {
      credentials: "include"
    })
      .then(response => {
        if (response.ok) {
          return response.json();
        }
        throw new Error("No hay sesión activa");
      })
      .then(data => {
        setUsuario(data.usuario);
      })
      .catch(error => {
        console.log("Usuario no autenticado");
      });
  }, []);

  const handleLogout = async () => {
    try {
      const response = await fetch(`${API_URL}/logout`, {
        method: "POST",
        credentials: "include"
      });

      if (response.ok) {
        window.location.href = "/login";
      }
    } catch (error) {
      console.error("Error al cerrar sesión:", error);
    }
  };

  if (loading) {
    return (
      <div className={styles.container}>
        <div style={{ textAlign: "center", padding: "50px" }}>
          <i className="fas fa-spinner fa-spin" style={{ fontSize: "48px", color: "#FFD700" }}></i>
          <p>Cargando...</p>
        </div>
      </div>
    );
  }

  return (
    <>
      <Head>
        <title>EcoEnergy - Inicio</title>
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
        {usuario && (
          <div style={{ marginLeft: "auto", display: "flex", alignItems: "center", gap: "20px" }}>
            <span>Hola, {usuario.nombre}</span>
            <button 
              onClick={handleLogout}
              style={{
                background: "transparent",
                border: "1px solid #FFD700",
                color: "#FFD700",
                padding: "8px 16px",
                borderRadius: "5px",
                cursor: "pointer"
              }}
            >
              <i className="fas fa-sign-out-alt" style={{ marginRight: "5px" }}></i>
              Cerrar Sesión
            </button>
          </div>
        )}
      </header>

      <div className={styles.container}>
        <div className={`${styles.decoration} ${styles.decoration1}`}></div>
        <div className={`${styles.decoration} ${styles.decoration2}`}></div>

        <div className={styles.icono}>
          <i
            className="fas fa-home"
            style={{ color: "#FFD700", fontSize: "42px" }}
          ></i>
        </div>

        <h1>BIENVENIDO A ECOENERGY</h1>
        
        {error ? (
          <div style={{ 
            color: "#ff4444", 
            backgroundColor: "#ffe6e6", 
            padding: "20px", 
            borderRadius: "10px", 
            marginBottom: "20px",
            textAlign: "center"
          }}>
            <i className="fas fa-exclamation-triangle" style={{ marginRight: "10px" }}></i>
            {error}
          </div>
        ) : (
          <div style={{ 
            color: "#00aa00", 
            backgroundColor: "#e6ffe6", 
            padding: "20px", 
            borderRadius: "10px", 
            marginBottom: "20px",
            textAlign: "center",
            fontSize: "18px"
          }}>
            <i className="fas fa-check-circle" style={{ marginRight: "10px" }}></i>
            {mensaje}
          </div>
        )}

        {usuario ? (
          <div style={{ 
            backgroundColor: "#f0f8ff", 
            padding: "20px", 
            borderRadius: "10px", 
            marginBottom: "20px",
            textAlign: "center"
          }}>
            <h3>Información del Usuario</h3>
            <p><strong>Nombre:</strong> {usuario.nombre}</p>
            <p><strong>Correo:</strong> {usuario.correo}</p>
            <p><strong>Fecha de registro:</strong> {usuario.fecha_registro}</p>
          </div>
        ) : (
          <div style={{ textAlign: "center" }}>
            <p>Para acceder a todas las funcionalidades, inicia sesión o regístrate</p>
            <div style={{ marginTop: "20px", display: "flex", gap: "20px", justifyContent: "center" }}>
              <a href="/login" style={{ 
                background: "#FFD700", 
                color: "#000", 
                padding: "12px 24px", 
                borderRadius: "5px", 
                textDecoration: "none",
                fontWeight: "bold"
              }}>
                <i className="fas fa-sign-in-alt" style={{ marginRight: "8px" }}></i>
                Iniciar Sesión
              </a>
              <a href="/registro" style={{ 
                background: "transparent", 
                color: "#FFD700", 
                border: "2px solid #FFD700", 
                padding: "10px 22px", 
                borderRadius: "5px", 
                textDecoration: "none",
                fontWeight: "bold"
              }}>
                <i className="fas fa-user-plus" style={{ marginRight: "8px" }}></i>
                Registrarse
              </a>
            </div>
          </div>
        )}
      </div>
    </>
  );
}
