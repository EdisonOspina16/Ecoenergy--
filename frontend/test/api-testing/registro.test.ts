import { describe, it, expect, vi, beforeEach } from "vitest";
import { postRegistro, resolveError } from "@/lib/api/registro";

describe("API Registro (postRegistro / resolveError)", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  // Dummy para los datos de registro que no afectan la lógica de la llamada
  const dummyPayload = {
    nombre: "Test",
    apellidos: "User",
    correo: "test@example.com",
    contrasena: "password123",
  };

  it("debería retornar éxito y redireccionar cuando el fetch es exitoso (Camino Normal)", async () => {
    // === Arrange (Preparar) ===
    // Stub: Simulamos la respuesta exitosa del servidor evitando la llamada real.
    // Esto previene que nuestras pruebas dependan de servicios web o backends vivos.
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: true,
      headers: new Headers({ "content-type": "application/json" }),
      json: async () => ({ redirect: "/dashboard" }),
    });

    // === Act (Actuar) ===
    const resultado = await postRegistro(dummyPayload);

    // === Assert (Afirmar) ===
    // Spy implícito (vi.fn): Se utiliza para verificar con qué argumentos se llamó el 'fetch'.
    expect(globalThis.fetch).toHaveBeenCalledWith(
      expect.stringContaining("/registro"),
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify(dummyPayload),
      }),
    );
    expect(resultado).toEqual({ ok: true, redirect: "/dashboard" });
  });

  it("debería retornar error cuando la respuesta no es ok (Caso Error)", async () => {
    // === Arrange ===
    // Stub: Simulamos una respuesta fallida controlada (ej. 400 Bad Request)
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 400,
      headers: new Headers({ "content-type": "application/json" }),
      json: async () => ({ error: "El correo ya existe" }),
    });

    // === Act ===
    const resultado = await postRegistro(dummyPayload);

    // === Assert ===
    expect(resultado).toEqual({ ok: false, error: "El correo ya existe" });
  });

  it("debería lanzar error si el formato no es JSON (Caso Borde)", async () => {
    // === Arrange ===
    // Stub: Simulamos respuesta HTML o texto plano para probar validaciones.
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      headers: new Headers({ "content-type": "text/html" }),
      text: async () => "<html>Error</html>",
    });

    // === Act & Assert ===
    // Con expects a rechazos asíncronos "rejects.toThrow", el Act y el Assert ocurren simultáneamente.
    await expect(postRegistro(dummyPayload)).rejects.toThrow(
      /Formato de respuesta incorrecto/,
    );
  });
});

describe("resolveError", () => {
  it("debería manejar errores genéricos de Error (Normal Error)", () => {
    // === Arrange ===
    // Dummy: Objeto de Error usado solo para cumplir con la firma.
    const error = new Error("Mensaje de prueba");

    // === Act ===
    const resultado = resolveError(error);

    // === Assert ===
    expect(resultado).toBe(
      "Error al conectar con el servidor: Mensaje de prueba",
    );
  });

  it("debería manejar TypeError relacionados a fetch (Borde/Error de Red)", () => {
    // === Arrange ===
    const error = new TypeError("Failed to fetch");

    // === Act ===
    const resultado = resolveError(error);

    // === Assert ===
    expect(resultado).toContain("Verifica que el backend esté corriendo");
  });

  it("debería manejar errores de origen desconocido (Caso Borde)", () => {
    // === Arrange ===
    const errorInvalido = "String error";

    // === Act ===
    const resultado = resolveError(errorInvalido);

    // === Assert ===
    expect(resultado).toBe("Error desconocido al conectar con el servidor");
  });
});
