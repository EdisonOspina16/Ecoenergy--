const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000";

export type DeviceResponse = {
  nombre: string;
  consumo?: number | string;
  estado?: string;
  [key: string]: any;
};

export type FetchDispositivosResult = 
  | { ok: true; dispositivos: DeviceResponse[] }
  | { ok: false; error: string };

export async function fetchDispositivos(): Promise<FetchDispositivosResult> {
  const response = await fetch(`${API_URL}/dispositivos`, {
    credentials: "include",
  });

  if (!response.ok) {
    throw new Error("Error al obtener dispositivos");
  }

  const data = await response.json();

  if (data?.success && Array.isArray(data.dispositivos)) {
    return { ok: true, dispositivos: data.dispositivos };
  } else {
    return { ok: true, dispositivos: [] };
  }
}
