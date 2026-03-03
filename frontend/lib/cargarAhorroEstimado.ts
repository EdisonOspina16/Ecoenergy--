/**
 * Carga ahorro estimado vía GET /ahorro-estimado.
 * Usado para pruebas de caja blanca (fetch, setSavingData, setLoading, manejo de errores).
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000";

export type SavingData = {
  ahorro_financiero: string;
  impacto_ambiental: string;
  indicador_didactico: string;
};

const VACIO: SavingData = {
  ahorro_financiero: "",
  impacto_ambiental: "",
  indicador_didactico: "",
};

export type CargarAhorroSetters = {
  setSavingData: (data: SavingData) => void;
  setLoading?: (value: boolean) => void;
};

/**
 * GET /ahorro-estimado; actualiza setSavingData según data.success y data.data.
 * En errores o JSON malformado llama setSavingData vacío y console.error; finally setLoading(false).
 */
export async function cargarAhorroEstimado({
  setSavingData,
  setLoading,
}: CargarAhorroSetters): Promise<void> {
  if (setLoading) setLoading(true);
  try {
    const response = await fetch(`${API_URL}/ahorro-estimado`, { credentials: "include" });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();

    if (data?.success && data?.data) {
      const d = data.data;
      setSavingData({
        ahorro_financiero: d.ahorro_financiero ?? "",
        impacto_ambiental: d.impacto_ambiental ?? "",
        indicador_didactico: d.indicador_didactico ?? "",
      });
    } else {
      setSavingData(VACIO);
    }
  } catch (error) {
    console.error("Error al cargar ahorro estimado:", error);
    setSavingData(VACIO);
  } finally {
    if (setLoading) setLoading(false);
  }
}
