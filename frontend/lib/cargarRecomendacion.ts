/**
 * Carga recomendaciones haciendo fetch por cada dispositivo.
 * Usado para pruebas de caja blanca (fetch por device, setRecommendations, manejo de errores).
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000";

export type DeviceForRecomendacion = { id: string } | { url: string };

/**
 * Por cada dispositivo hace GET; si res.ok agrega data al resultado, si no agrega { error: "no response" }.
 * Si fetch lanza o res.json() lanza, actualiza setRecommendations([]).
 */
export async function cargarRecomendacion(
  devices: DeviceForRecomendacion[],
  setRecommendations: (items: any[]) => void
): Promise<void> {
  const resultados: any[] = [];

  for (const device of devices) {
    const url = "url" in device ? device.url : `${API_URL}/recomendacion/${device.id}`;
    try {
      const res = await fetch(url, { credentials: "include" });
      if (res.ok) {
        try {
          const data = await res.json();
          resultados.push(data);
        } catch {
          setRecommendations([]);
          return;
        }
      } else {
        resultados.push({ error: "no response" });
      }
    } catch {
      setRecommendations([]);
      return;
    }
  }

  setRecommendations(resultados);
}
