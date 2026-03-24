export function mapNetworkError(error: unknown): string {
  if (error instanceof Error) {
    if (error.name === "TypeError" && error.message.includes("fetch")) {
      return "No se puede conectar con el servidor. Verifica que el backend esté disponible";
    }
    return `Error al conectar con el servidor: ${error.message}`;
  }
  return "Error desconocido al conectar con el servidor";
}

export function extractErrorMessage(status: number, payload: any): string {
  if (payload?.error) return String(payload.error);
  if (status === 401) return "Credenciales inválidas";
  if (status === 500) return "Error interno del servidor";
  if (status === 0) return "No se pudo completar la solicitud";
  return `Error ${status}`;
}
