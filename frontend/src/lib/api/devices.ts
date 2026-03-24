import { API_URL } from "../config/api";
import { postJson } from "../http/jsonClient";
import { buildActionResult, ActionResult } from "../responses/actionResult";

export type RegisterDevicePayload = {
  deviceId: string;
  nickname: string;
};

export type DeviceResponse = {
  success?: boolean;
  dispositivo?: DeviceData;
  error?: string;
};

export type DeviceData = {
  id: number;
  name: string;
  icon: string;
  connected: boolean;
};

export async function registerDevice(
  payload: RegisterDevicePayload,
): Promise<ActionResult<DeviceData>> {
  const result = await postJson<DeviceResponse>(`${API_URL}/perfil`, payload);

  return buildActionResult(result, (response) => response.dispositivo, {
    success: "Dispositivo registrado exitosamente",
    fallbackError: "Error al registrar el dispositivo",
    customError: (response) => response.error,
  });
}
