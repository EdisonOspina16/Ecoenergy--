"use client";

import styles from "../../styles/registro.module.css";
import Head from "next/head";

export default function RegistroPage() {
  return (
    <>
      <Head>
        <title> Registro - EcoEnergy</title>
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
      
      <div className={styles.formContainer}>
        <div className={styles.iconContainer}>
          <div className={styles.lightbulb}>
            <span className={styles.bolt}>⚡</span>
          </div>
        </div>
        
        <h1 className={styles.title}>Crear una cuenta nueva</h1>
        
        <p className={styles.subtitle}>
          ¿Ya estás registrado? <a href="/login" className={styles.link}>Accede</a>
        </p>
        
        <form className={styles.form}>
          <div className={styles.inputGroup}>
            <label className={styles.label}>NOMBRES *</label>
            <input 
              type="text" 
              placeholder="Ej: Alma Marcela"
              className={styles.input}
            />
          </div>
          
          <div className={styles.inputGroup}>
            <label className={styles.label}>APELLIDOS *</label>
            <input 
              type="text" 
              placeholder="Ej: Gozo"
              className={styles.input}
            />
          </div>
          
          <div className={styles.inputGroup}>
            <label className={styles.label}>CORREO ELECTRÓNICO *</label>
            <input 
              type="email" 
              placeholder="TU@CORREO.COM"
              className={styles.input}
            />
          </div>
          
          <div className={styles.inputGroup}>
            <label className={styles.label}>CONTRASEÑA *</label>
            <input 
              type="password" 
              placeholder="••••••••"
              className={styles.input}
            />
          </div>
          
          <button type="submit" className={styles.submitButton}>
            CREAR
          </button>
        </form>
      </div>
    </>
  )
}