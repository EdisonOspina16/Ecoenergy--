import { API_URL } from "../config/api";
import { postJson } from "../http/jsonClient";

export type LoginPayload = {
  correo: string;
  contrasena: string;
};

export type LoginResult =
  | { ok: true; redirect: string; usuario?: Record<string, unknown> }
  | { ok: false; message: string };

type LoginResponse = {
  redirect?: string;
  usuario?: Record<string, unknown>;
  error?: string;
};

export async function loginRequest(
  payload: LoginPayload,
): Promise<LoginResult> {
  const result = await postJson<LoginResponse>(`${API_URL}/login`, payload, {
    credentials: "include",
  });

  if (result.ok) {
    const redirect = result.data.redirect ?? "/dashboard";
    return { ok: true, redirect, usuario: result.data.usuario };
  }

  return { ok: false, message: result.message };
}
