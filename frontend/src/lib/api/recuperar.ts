import { API_URL } from "../config/api";
import { postJson, JsonResult } from "../http/jsonClient";

export type RecuperarPayload = {
  correo: string;
  nueva_contrasena: string;
};

export type RecuperarResponse = {
  message?: string;
  redirect?: string;
  error?: string;
};

export async function postRecuperar(payload: RecuperarPayload): Promise<JsonResult<RecuperarResponse>> {
  return postJson<RecuperarResponse>(`${API_URL}/recuperar`, payload);
}
