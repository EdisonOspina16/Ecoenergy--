const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000";

type RegistroPayload = {
  nombre: string;
  apellidos: string;
  correo: string;
  contrasena: string;
};

type RegistroResult =
  | { ok: true; redirect: string }
  | { ok: false; error: string };

export async function postRegistro(payload: RegistroPayload): Promise<RegistroResult> {
  const response = await fetch(`${API_URL}/registro`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify(payload),
  });

  const contentType = response.headers.get("content-type");
  if (!contentType?.includes("application/json")) {
    const text = await response.text();
    throw new Error(
      `Formato de respuesta incorrecto (${response.status}): ${text.substring(0, 200)}`
    );
  }

  const data = await response.json();

  return response.ok
    ? { ok: true, redirect: data.redirect }
    : { ok: false, error: data.error ?? "Error al procesar el registro" };
}

export function resolveError(error: unknown): string {
  if (!(error instanceof Error)) return "Error desconocido al conectar con el servidor";

  if (error.name === "TypeError" && error.message.includes("fetch")) {
    return "No se puede conectar con el servidor. Verifica que el backend esté corriendo en http://localhost:5000";
  }

  return `Error al conectar con el servidor: ${error.message}`;
}