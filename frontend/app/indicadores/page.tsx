"use client";
import { useEffect, useState } from "react";

interface Indicador {
  energia_ahorrada_kwh: number;
  reduccion_co2_kg: number;
  arboles_salvados: number;
  ahorro_economico: number;
  periodo: string;
}

export default function IndicadoresPage() {
  const [indicadores, setIndicadores] = useState<Indicador | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("http://localhost:5000/api/indicadores/1")
      .then((res) => res.json())
      .then((data) => {
        if (Array.isArray(data) && data.length > 0) {
          setIndicadores(data[0]);
        } else if (data) {
          setIndicadores(data);
        } else {
          setError("No hay indicadores disponibles");
        }
      })
      .catch((err) => {
        console.error("Error al obtener indicadores:", err);
        setError("Error al obtener indicadores");
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <p style={{ textAlign: "center", marginTop: "50px" }}>Cargando indicadores...</p>;
  }

  if (error) {
    return <p style={{ textAlign: "center", marginTop: "50px", color: "red" }}>{error}</p>;
  }

  if (!indicadores) {
    return <p style={{ textAlign: "center", marginTop: "50px" }}>No hay indicadores disponibles</p>;
  }

  return (
    <div style={{ minHeight: "100vh", backgroundColor: "#111", color: "white", padding: "40px" }}>
      <h1 style={{ textAlign: "center", marginBottom: "30px", color: "#FFD700" }}>
        Indicadores de Ahorro e Impacto Ambiental
      </h1>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))", gap: "20px" }}>
        {/* Energía Ahorrada */}
        <div style={{ background: "#222", padding: "20px", borderRadius: "10px", textAlign: "center" }}>
          <h2>Energía Ahorrada</h2>
          <p style={{ fontSize: "22px", color: "#00FF7F" }}>{indicadores.energia_ahorrada_kwh} kWh</p>
        </div>

        {/* Reducción de CO₂ */}
        <div style={{ background: "#222", padding: "20px", borderRadius: "10px", textAlign: "center" }}>
          <h2>Reducción de CO₂</h2>
          <p style={{ fontSize: "22px", color: "#1E90FF" }}>{indicadores.reduccion_co2_kg} kg</p>
        </div>

        {/* Árboles Salvados */}
        <div style={{ background: "#222", padding: "20px", borderRadius: "10px", textAlign: "center" }}>
          <h2>Árboles Salvados</h2>
          <p style={{ fontSize: "22px", color: "#32CD32" }}>{indicadores.arboles_salvados}</p>
        </div>

        {/* Ahorro Económico */}
        <div style={{ background: "#222", padding: "20px", borderRadius: "10px", textAlign: "center" }}>
          <h2>Ahorro Económico</h2>
          <p style={{ fontSize: "22px", color: "#FFD700" }}>${indicadores.ahorro_economico}</p>
        </div>
      </div>

      <p style={{ textAlign: "center", marginTop: "40px", color: "#999" }}>
        Última actualización: {new Date(indicadores.periodo).toLocaleDateString()}
      </p>
    </div>
  );
}
