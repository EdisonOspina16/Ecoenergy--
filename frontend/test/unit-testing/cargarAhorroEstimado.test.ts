import { describe, it, expect, vi, beforeEach } from "vitest";
import {
  cargarAhorroEstimado,
  CargarAhorroSetters,
} from "@/lib/cargarAhorroEstimado";

describe("cargarAhorroEstimado", () => {
  // Spies: Interceptar funciones de state sin implementar la lógica de UI
  let setSavingDataSpy: ReturnType<typeof vi.fn>;
  let setLoadingSpy: ReturnType<typeof vi.fn>;
  let setters: CargarAhorroSetters;

  beforeEach(() => {
    vi.restoreAllMocks();
    setSavingDataSpy = vi.fn();
    setLoadingSpy = vi.fn();
    setters = { setSavingData: setSavingDataSpy, setLoading: setLoadingSpy };
    // Stub: Apagar consola de error en tests para output limpio
    vi.spyOn(console, "error").mockImplementation(() => {});
  });

  it("debería cargar y setear los datos si el fetch y json son exitosos (Camino Normal)", async () => {
    // === Arrange ===
    // Stub global: Controlar la promesa fetch al vuelo para testear sin interrupción.
    const fakeDataResponse = {
      success: true,
      data: {
        ahorro_financiero: "100 USD",
        impacto_ambiental: "50kg CO2",
        indicador_didactico: "Buena!",
      },
    };

    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => fakeDataResponse,
    });

    // === Act ===
    await cargarAhorroEstimado(setters);

    // === Assert ===
    // Validar invocaciones de los Spies
    expect(setLoadingSpy).toHaveBeenCalledWith(true);
    expect(setSavingDataSpy).toHaveBeenCalledWith({
      ahorro_financiero: "100 USD",
      impacto_ambiental: "50kg CO2",
      indicador_didactico: "Buena!",
    });
    expect(setLoadingSpy).toHaveBeenLastCalledWith(false);
  });

  it("debería colocar los datos VACIOs si el fetch lanza un error de status (Caso Error)", async () => {
    // === Arrange ===
    // Stub: Rechazo basado en fetch API properties
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 404,
      statusText: "Not Found",
    });

    // === Act ===
    await cargarAhorroEstimado(setters);

    // === Assert ===
    expect(setSavingDataSpy).toHaveBeenCalledWith({
      ahorro_financiero: "",
      impacto_ambiental: "",
      indicador_didactico: "",
    });
    expect(console.error).toHaveBeenCalled();
  });

  it("debería colocar datos VACIOs si success es falso en el json (Caso Borde)", async () => {
    // === Arrange ===
    // Stub
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ success: false }),
    });

    // === Act ===
    await cargarAhorroEstimado(setters);

    // === Assert ===
    expect(setSavingDataSpy).toHaveBeenCalledWith({
      ahorro_financiero: "",
      impacto_ambiental: "",
      indicador_didactico: "",
    });
  });
});
