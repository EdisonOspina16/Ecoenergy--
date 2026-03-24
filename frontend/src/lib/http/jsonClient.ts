import { extractErrorMessage, mapNetworkError } from "../errors/errorMapper";

export type JsonResult<T> =
  | { ok: true; data: T; status: number }
  | { ok: false; status: number; message: string };

type JsonRequestOptions = Pick<RequestInit, "credentials" | "headers">;

const defaultHeaders = { "Content-Type": "application/json" };

type JsonFetchOptions = Pick<RequestInit, "credentials" | "headers">;

export async function postJson<T>(
  url: string,
  body: unknown,
  options: JsonRequestOptions = {},
): Promise<JsonResult<T>> {
  const request: RequestInit = {
    method: "POST",
    credentials: options.credentials ?? "include",
    headers: { ...defaultHeaders, ...(options.headers ?? {}) },
    body: JSON.stringify(body),
  };

  try {
    const response = await fetch(url, request);
    const payload = await readJson(response);

    if (response.ok) {
      return { ok: true, data: payload as T, status: response.status };
    }

    return {
      ok: false,
      status: response.status,
      message: extractErrorMessage(response.status, payload),
    };
  } catch (error) {
    return { ok: false, status: 0, message: mapNetworkError(error) };
  }
}

export async function getJson<T>(
  url: string,
  options: JsonFetchOptions = {},
): Promise<JsonResult<T>> {
  const request: RequestInit = {
    method: "GET",
    credentials: options.credentials ?? "include",
    headers: { ...(options.headers ?? {}) },
  };

  try {
    const response = await fetch(url, request);
    const payload = await readJson(response);

    if (response.ok) {
      return { ok: true, data: payload as T, status: response.status };
    }

    return {
      ok: false,
      status: response.status,
      message: extractErrorMessage(response.status, payload),
    };
  } catch (error) {
    return { ok: false, status: 0, message: mapNetworkError(error) };
  }
}

async function readJson(response: Response): Promise<unknown> {
  const contentType = response.headers.get("content-type");
  const isJson = contentType?.includes("application/json");
  if (!isJson) return null;
  try {
    return await response.json();
  } catch {
    return null;
  }
}
