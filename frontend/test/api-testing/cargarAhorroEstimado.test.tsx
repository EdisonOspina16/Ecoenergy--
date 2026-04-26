/**
 * Pruebas de caja blanca para cargarAhorroEstimado (frontend).
 * Verifica: GET /ahorro-estimado, response.ok, data.success, data.data,
 * setSavingData, setLoading, console.error, manejo de HTTP error, excepción de red, JSON malformado.
 */

import React from "react";
import { afterEach, beforeEach, describe, expect, test, vi } from "vitest";
import { cargarAhorroEstimado } from "@/lib/cargarAhorroEstimado";

const mockFetch = vi.fn();
const vacio = {
  ahorro_financiero: "",
  impacto_ambiental: "",
  indicador_didactico: "",
};

beforeEach(() => {
  vi.clearAllMocks();
  vi.stubGlobal("fetch", mockFetch);
  vi.spyOn(console, "error").mockImplementation(() => {});
});

afterEach(() => {
  vi.restoreAllMocks();
});

describe("cargarAhorroEstimado - caja blanca", () => {
  const setSavingData = vi.fn();
  const setLoading = vi.fn();

  test("cargarAhorroEstimado - todo OK + data válida", async () => {
    const ahorro_financiero = "50 €/mes";
    const impacto_ambiental = "100 kg CO2 menos";
    const indicador_didactico = "3 árboles";

    mockFetch.mockResolvedValue({
      ok: true,
      json: () =>
        Promise.resolve({
          success: true,
          data: {
            ahorro_financiero,
            impacto_ambiental,
            indicador_didactico,
          },
        }),
    });

    await cargarAhorroEstimado({ setSavingData, setLoading });

    // C1: setSavingData con los tres campos completos
    expect(setSavingData).toHaveBeenCalledWith({
      ahorro_financiero,
      impacto_ambiental,
      indicador_didactico,
    });
  });

  test("cargarAhorroEstimado - response OK pero data vacía (success false o data null)", async () => {
    mockFetch.mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ success: false }),
    });

    await cargarAhorroEstimado({ setSavingData, setLoading });

    // C2: setSavingData con valores vacíos
    expect(setSavingData).toHaveBeenCalledWith(vacio);
  });

  test("cargarAhorroEstimado - HTTP error 4xx/5xx: catch, setSavingData vacío, finally loading(false)", async () => {
    mockFetch.mockResolvedValue({
      ok: false,
      status: 500,
      statusText: "Internal Server Error",
    });

    await cargarAhorroEstimado({ setSavingData, setLoading });

    // C3: catch ejecutado -> setSavingData vacío
    expect(setSavingData).toHaveBeenCalledWith(vacio);
    // C3: finally -> setLoading(false)
    expect(setLoading).toHaveBeenLastCalledWith(false);
  });

  test("cargarAhorroEstimado - excepción de red: console.error y setSavingData vacío", async () => {
    mockFetch.mockRejectedValue(new Error("Failed to fetch"));

    await cargarAhorroEstimado({ setSavingData, setLoading });

    // C4: console.error llamado
    expect(console.error).toHaveBeenCalled();
    // C4: setSavingData vacío
    expect(setSavingData).toHaveBeenCalledWith(vacio);
  });

  test("cargarAhorroEstimado - JSON malformado: console.error y setSavingData vacío", async () => {
    mockFetch.mockResolvedValue({
      ok: true,
      json: () => Promise.reject(new SyntaxError("Unexpected token < in JSON")),
    });

    await cargarAhorroEstimado({ setSavingData, setLoading });

    // C5: console.error llamado
    expect(console.error).toHaveBeenCalled();
    // C5: setSavingData vacío
    expect(setSavingData).toHaveBeenCalledWith(vacio);
  });
});
