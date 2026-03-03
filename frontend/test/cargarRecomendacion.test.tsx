/**
 * Pruebas de caja blanca para cargarRecomendacion (frontend).
 * Verifica: fetch por cada device, res.ok, res.json(), setRecommendations,
 * manejo de res.ok = false, excepción de red, JSON malformado.
 */

import React from "react";
import { afterEach, beforeEach, describe, expect, test, vi } from "vitest";
import { cargarRecomendacion } from "../lib/cargarRecomendacion";

const mockFetch = vi.fn();

beforeEach(() => {
  vi.clearAllMocks();
  vi.stubGlobal("fetch", mockFetch);
});

afterEach(() => {
  vi.restoreAllMocks();
});

describe("cargarRecomendacion - caja blanca", () => {
  const setRecommendations = vi.fn();

  test("cargarRecomendacion - todo OK: fetch OK, res.ok true, datos en resultados", async () => {
    const datosDevice1 = { recomendacion: "Apagar luces", esAlerta: false };
    const datosDevice2 = { recomendacion: "Bajar clima", esAlerta: true };

    mockFetch
      .mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(datosDevice1),
      })
      .mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(datosDevice2),
      });

    await cargarRecomendacion([{ id: "1" }, { id: "2" }], setRecommendations);

    // C1: setRecommendations llamado con los resultados agregados
    expect(setRecommendations).toHaveBeenCalledTimes(1);
    expect(setRecommendations).toHaveBeenCalledWith([datosDevice1, datosDevice2]);
  });

  test("cargarRecomendacion - res.ok = false: agrega { error: 'no response' }", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 500,
    });

    await cargarRecomendacion([{ id: "1" }], setRecommendations);

    // C2: cuando !res.ok se agrega { error: "no response" } al resultado
    expect(setRecommendations).toHaveBeenCalledWith([{ error: "no response" }]);
  });

  test("cargarRecomendacion - excepción de red: setRecommendations([])", async () => {
    mockFetch.mockRejectedValueOnce(new Error("Network error"));

    await cargarRecomendacion([{ id: "1" }], setRecommendations);

    // C3: ante excepción se llama setRecommendations con array vacío
    expect(setRecommendations).toHaveBeenCalledWith([]);
  });

  test("cargarRecomendacion - JSON malformado: res.ok true pero res.json() lanza", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.reject(new SyntaxError("Unexpected token")),
    });

    await cargarRecomendacion([{ id: "1" }], setRecommendations);

    // C4: si res.json() lanza, se actualiza setRecommendations([])
    expect(setRecommendations).toHaveBeenCalledWith([]);
  });
});
