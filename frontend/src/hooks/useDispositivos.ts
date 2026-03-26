import { fetchDispositivos } from "../lib/api/dispositivos";

export type Device = {
  nombre: string;
  consumo?: number;
  estado?: string;
  [key: string]: any;
};

export type CargarDispositivosSetters = {
  setDevices: (devices: Device[]) => void;
  setLoadingDevices: (loading: boolean) => void;
};

export async function cargarDispositivos({
  setDevices,
  setLoadingDevices,
}: CargarDispositivosSetters): Promise<void> {
  try {
    const result = await fetchDispositivos();
    if (result.ok) {
      const dispositivosMapeados: Device[] = result.dispositivos.map((d) => ({
        nombre: d.nombre,
        consumo: Number(d.consumo) || 0,
        estado: d.estado || "Desconocido",
      }));
      setDevices(dispositivosMapeados);
    } else {
      setDevices([]);
    }
  } catch (error) {
    console.error("Error al cargar dispositivos:", error);
    setDevices([]);
  } finally {
    setLoadingDevices(false);
  }
}
