import { API_URL } from "../config/api";
import { getJson, postJson, JsonResult } from "../http/jsonClient";

export type PerfilResponse = {
  success?: boolean;
  hogar?: { direccion?: string; nombre_hogar?: string } | null;
  dispositivos?: PerfilDevice[];
  error?: string;
};

export type PerfilDevice = {
  id: number;
  name: string;
  icon: string;
  connected: boolean;
};

export async function fetchPerfil(): Promise<JsonResult<PerfilResponse>> {
  return getJson<PerfilResponse>(`${API_URL}/perfil`);
}

export type PostProfilePayload = {
  address: string;
  nombre_hogar: string;
};

export type PostProfileResponse = {
  success?: boolean;
  message?: string;
  error?: string;
};

export async function postProfile(payload: PostProfilePayload): Promise<JsonResult<PostProfileResponse>> {
  return postJson<PostProfileResponse>(`${API_URL}/perfil`, payload);
}
