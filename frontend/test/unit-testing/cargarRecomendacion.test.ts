import { describe, it, expect, vi, beforeEach } from "vitest";
import {
  cargarRecomendacion,
  DeviceForRecomendacion,
} from "@/lib/cargarRecomendacion";

describe("cargarRecomendacion", () => {
  let setRecommendationsSpy: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    vi.restoreAllMocks();
    setRecommendationsSpy = vi.fn();
  });

  // Dummy: Objetos de input usados simplemente para disparar ciclos iterativos en validaciones
  const device1: DeviceForRecomendacion = { id: "device-1" };
  const device2: DeviceForRecomendacion = { url: "https://test.com/reco" };

  it("debería cargar y combinar datos de todos los dispositivos exitosos (Camino Normal)", async () => {
    // === Arrange ===
    // Stub Secuencial: Simulamos resultados para 2 fetch consecutivos distintos
    globalThis.fetch = vi
      .fn()
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ recomendacion: "reco1" }),
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ recomendacion: "reco2" }),
      });

    // === Act ===
    await cargarRecomendacion([device1, device2], setRecommendationsSpy);

    // === Assert ===
    expect(globalThis.fetch).toHaveBeenCalledTimes(2);
    // Spy result verification
    expect(setRecommendationsSpy).toHaveBeenCalledWith([
      { recomendacion: "reco1" },
      { recomendacion: "reco2" },
    ]);
  });

  it('debería incluir "no response" si un fetch no devuelve HTTP ok (Caso Borde/Error Controlado)', async () => {
    // === Arrange ===
    // Stub: Repuesta HTTP que no pasa (ej: caída ligera del server parcial)
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: false,
    });

    // === Act ===
    await cargarRecomendacion([device1], setRecommendationsSpy);

    // === Assert ===
    expect(setRecommendationsSpy).toHaveBeenCalledWith([
      { error: "no response" },
    ]);
  });

  it("debería vaciar la lista (set[]) si la promesa originaria falla súbitamente (Caso Error Severo)", async () => {
    // === Arrange ===
    // Stub Network Reject
    globalThis.fetch = vi.fn().mockRejectedValue(new Error("Network error"));

    // === Act ===
    await cargarRecomendacion([device1], setRecommendationsSpy);

    // === Assert ===
    expect(setRecommendationsSpy).toHaveBeenCalledWith([]);
  });

  it("debería vaciar la lista si la promesa del JSON falla - invalid json (Caso Borde parseo)", async () => {
    // === Arrange ===
    // Stub
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => {
        throw new Error("Parse error");
      },
    });

    // === Act ===
    await cargarRecomendacion([device1], setRecommendationsSpy);

    // === Assert ===
    // Debido al bloque catch de json(), debe parar el for y retornar arreglo vacio
    expect(setRecommendationsSpy).toHaveBeenCalledWith([]);
  });
});
