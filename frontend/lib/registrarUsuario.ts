/**
 * Lógica de registro de usuario (extraída para pruebas unitarias).
 * POST a /registro, maneja response.ok, data.redirect y errores (TypeError fetch, Error, string).
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000";

export type RegistrarUsuarioSetters = {
  setLoading: (value: boolean) => void;
  setError: (value: string) => void;
};

export async function registrarUsuario(
  nombre: string,
  apellidos: string,
  correo: string,
  contrasena: string,
  { setLoading, setError }: RegistrarUsuarioSetters
): Promise<void> {
  setError("");
  setLoading(true);

  console.log("Intentando registro con:", { nombre, apellidos, correo, contrasena: "***" });

  try {
    const response = await fetch(`${API_URL}/registro`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
      body: JSON.stringify({
        nombre,
        apellidos,
        correo,
        contrasena,
      }),
    });

    console.log("Response status:", response.status);
    console.log("Response headers:", response.headers);

    if (!response.ok) {
      console.error("Error response:", response.status, response.statusText);
    }

    const contentType = response.headers.get("content-type");
    if (!contentType || !contentType.includes("application/json")) {
      const text = await response.text();
      console.error("Respuesta no es JSON:", text.substring(0, 200));
      throw new Error(`El servidor respondió con un formato de respuesta incorrecto (Estado: ${response.status})`);
    }

    const data = await response.json();
    console.log("Response data:", data);

    if (response.ok) {
      console.log("Registro exitoso, redirigiendo a:", data.redirect);
      window.location.href = data.redirect;
    } else {
      console.error("Error en registro:", data.error);
      setError(data.error || "Error al procesar el registro");
    }
  } catch (error) {
    console.error("Error en la petición:", error);

    if (error instanceof Error) {
      console.error("Tipo de error:", error.name);
      console.error("Mensaje:", error.message);

      if (error.name === "TypeError" && error.message.includes("fetch")) {
        setError(
          "No se puede conectar con el servidor. Verifica que el backend esté corriendo en http://localhost:5000"
        );
      } else {
        setError("Error al conectar con el servidor: " + error.message);
      }
    } else {
      setError("Error desconocido al conectar con el servidor");
    }
  } finally {
    setLoading(false);
  }
}
