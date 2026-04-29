import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { renderHook, act } from "@testing-library/react";
import { useRecuperar } from "@/hooks/useRecuperar";
import { postRecuperar } from "@/lib/api/recuperar";

// Mock: Simulamos postRecuperar aislando esta prueba del ecosistema de fetch/backend.
vi.mock("@/lib/api/recuperar", () => ({
  postRecuperar: vi.fn(),
}));

describe("Hook: useRecuperar", () => {
  const originalLocation = globalThis.location;

  beforeEach(() => {
    vi.clearAllMocks();

    // Fake Timers: Falsificamos el reloj de ejecución de JS.
    // Ésto evita esperar 2000ms en el test para verificar la redirección (Caso Normal).
    vi.useFakeTimers();

    // Mockeamos el location para constatar a dónde redirige el script.
    Object.defineProperty(globalThis, "location", {
      value: { href: "" },
      writable: true,
    });
  });

  afterEach(() => {
    // Restauramos Timers reales
    vi.useRealTimers();
    Object.defineProperty(globalThis, "location", {
      value: originalLocation,
      writable: true,
    });
  });

  it("debería setear éxito, esperar e ir a redirect (Camino Normal)", async () => {
    // === Arrange ===
    // Stub: Configuración controlada para éxito puro de recuperación
    (postRecuperar as any).mockResolvedValue({
      ok: true,
      data: {
        error: undefined,
        message: "Contraseña enviada a su correo",
        redirect: "/login",
      },
    });

    const { result } = renderHook(() => useRecuperar());
    const eventMock = { preventDefault: vi.fn() } as any;

    act(() => {
      result.current.setCorreo("test@example.com");
      result.current.setNuevacontrasena("1234");
    });

    // === Act ===
    await act(async () => {
      await result.current.handleSubmit(eventMock);
    });

    // === Assert ===
    expect(postRecuperar).toHaveBeenCalledWith({
      correo: "test@example.com",
      nueva_contrasena: "1234",
    });
    expect(result.current.success).toBe("Contraseña enviada a su correo");
    expect(result.current.error).toBe("");

    // === Act 2 (Fake Timers) ===
    // Avanzamos el reloj virtual de forma sincrona para ejecutar los setTimeout
    act(() => {
      vi.runAllTimers();
    });

    // Validamos redirección
    expect(globalThis.location.href).toBe("/login");
  });

  it("debería setear error recibido si back retorna error con .ok=true (Caso de Error Manejado)", async () => {
    // === Arrange ===
    (postRecuperar as any).mockResolvedValue({
      ok: true,
      data: { error: "El correo no existe" },
    });

    const { result } = renderHook(() => useRecuperar());
    const eventMock = { preventDefault: vi.fn() } as any;

    // === Act ===
    await act(async () => {
      await result.current.handleSubmit(eventMock);
    });

    // === Assert ===
    expect(result.current.error).toBe("El correo no existe");
    expect(result.current.success).toBe("");
  });

  it("debería setear error interno o de red si status no es ok (Caso Borde/Red)", async () => {
    // === Arrange ===
    // Stub simulando rotura de red o status 500
    (postRecuperar as any).mockResolvedValue({
      ok: false,
      message: "Gateway timeout",
    });

    const { result } = renderHook(() => useRecuperar());
    const eventMock = { preventDefault: vi.fn() } as any;

    // === Act ===
    await act(async () => {
      await result.current.handleSubmit(eventMock);
    });

    // === Assert ===
    expect(result.current.error).toBe("Gateway timeout");
  });

  it("debería setear fallback error/success si data devuelta no los tiene explícitamente (Fallback Messages)", async () => {
    // === Arrange ===
    (postRecuperar as any).mockResolvedValue({
      ok: true,
      data: {}, // error y message vacios
    });

    const { result } = renderHook(() => useRecuperar());
    const eventMock = { preventDefault: vi.fn() } as any;

    act(() => {
      result.current.setCorreo("test@correo.com");
    });

    // === Act ===
    await act(async () => {
      await result.current.handleSubmit(eventMock);
    });

    // === Assert ===
    // Asegurarse de que salta el fallback string del hook "Contraseña actualizada exitosamente"
    expect(result.current.success).toBe("Contraseña actualizada exitosamente");
  });

  it("debería setear fallback error al fallar sin mensaje expreso si data.error está vacío (Fallback Errors)", async () => {
    // === Arrange ===
    (postRecuperar as any).mockResolvedValue({
      ok: true,
      data: { error: undefined, success: false, redirect: undefined },
    });

    // Para forzar el error debemos lograr que `!result.data.error` de falso, pero esta es logica: if (!result.data.error) entra a succes.
    // Si queremos el error debemos mandar result.data.error = ''. Como en js '' es falso entrara al success...
    // Sin embargo, si simulamos que falla el OK, veamos los fallbacks...
    (postRecuperar as any).mockResolvedValue({
      ok: false,
    });

    const { result } = renderHook(() => useRecuperar());
    const eventMock = { preventDefault: vi.fn() } as any;

    // === Act ===
    await act(async () => {
      await result.current.handleSubmit(eventMock);
    });

    // === Assert ===
    // Esperamos el fallback "Error al conectar con el servidor" cuando .ok es falso y no trae message
    expect(result.current.error).toBe("Error al conectar con el servidor");
  });

  it("debería capturar errores de ejecución y mostrar el fallback genérico de catch (Catch Exception)", async () => {
    // === Arrange ===
    (postRecuperar as any).mockRejectedValue(
      new Error("Fatal error backend crashed"),
    );

    const consoleSpy = vi.spyOn(console, "error").mockImplementation(() => {});

    const { result } = renderHook(() => useRecuperar());
    const eventMock = { preventDefault: vi.fn() } as any;

    // === Act ===
    await act(async () => {
      await result.current.handleSubmit(eventMock);
    });

    // === Assert ===
    expect(consoleSpy).toHaveBeenCalled();
    expect(result.current.error).toBe("Error al conectar con el servidor");
    expect(result.current.loading).toBe(false);
  });
});
