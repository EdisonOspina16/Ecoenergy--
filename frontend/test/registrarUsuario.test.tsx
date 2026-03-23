/**
 * Pruebas de caja blanca para registrarUsuario (frontend).
 * Verifica: fetch POST, response.ok, data.redirect, setLoading, setError,
 * manejo de TypeError(fetch), Error genérico, error como string,
 * console.log, console.error, window.location.href.
 */

import React from "react";
import { afterEach, beforeEach, describe, expect, test, vi } from "vitest";
import { registrarUsuario } from "../src/hooks/useRegistro";


// Mock global de fetch
const mockFetch = vi.fn();

// Backup de location para restaurar después
const originalLocation = window.location;

beforeEach(() => {
  vi.clearAllMocks();
  vi.stubGlobal("fetch", mockFetch);

  // Mock de window.location
  delete (window as any).location;
  window.location = { ...originalLocation, href: "" } as Location;

  // Mocks de console para verificar llamadas
  vi.spyOn(console, "log").mockImplementation(() => {});
  vi.spyOn(console, "error").mockImplementation(() => {});
});

afterEach(() => {
  vi.restoreAllMocks();
  window.location = originalLocation;
});

describe("registrarUsuario - caja blanca", () => {
  const setLoading = vi.fn();
  const setError = vi.fn();

  const params = {
    nombre: "Ana",
    apellidos: "López",
    correo: "ana@mail.com",
    contrasena: "1234",
  };

  test("registrarUsuario - happy path: registro exitoso y redirección a /login", async () => {
    mockFetch.mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ redirect: "/login" }),
    });

    await registrarUsuario(params.nombre, params.apellidos, params.correo, params.contrasena, {
      setLoading,
      setError,
    });

    // C1: Verificar que se llamó a fetch POST con la URL correcta
    expect(mockFetch).toHaveBeenCalledWith(
      expect.stringContaining("/registro"),
      expect.objectContaining({
        method: "POST",
        headers: expect.objectContaining({ "Content-Type": "application/json" }),
        body: JSON.stringify({
          nombre: params.nombre,
          apellidos: params.apellidos,
          correo: params.correo,
          contrasena: params.contrasena,
        }),
      })
    );

    // C1: console.log debe haberse llamado (intento de registro y/o redirección)
    expect(console.log).toHaveBeenCalled();

    // C1: Redirección a /login
    expect(window.location.href).toBe("/login");

    // C1: setLoading(false) en finally
    expect(setLoading).toHaveBeenLastCalledWith(false);
  });

  test("registrarUsuario - correo ya registrado (409)", async () => {
    mockFetch.mockResolvedValue({
      ok: false,
      status: 409,
      statusText: "Conflict",
      json: () => Promise.resolve({ error: "Correo ya registrado" }),
    });

    await registrarUsuario(params.nombre, params.apellidos, params.correo, params.contrasena, {
      setLoading,
      setError,
    });

    // C2: console.error llamado con el error del backend
    expect(console.error).toHaveBeenCalled();

    // C2: setError con el mensaje del backend
    expect(setError).toHaveBeenCalledWith("Correo ya registrado");

    // C2: setLoading(false)
    expect(setLoading).toHaveBeenLastCalledWith(false);
  });

  test("registrarUsuario - backend apagado (TypeError con 'fetch')", async () => {
    const error = new TypeError("Failed to fetch");
    mockFetch.mockRejectedValue(error);

    await registrarUsuario(params.nombre, params.apellidos, params.correo, params.contrasena, {
      setLoading,
      setError,
    });

    // C3: error es instancia de Error y message incluye "fetch"
    expect(error instanceof Error).toBe(true);
    expect(error.message).toContain("fetch");

    // C3: setError con mensaje de servidor no disponible
    expect(setError).toHaveBeenCalledWith(
      "No se puede conectar con el servidor. Verifica que el backend esté corriendo en http://localhost:5000"
    );

    // C3: setLoading(false)
    expect(setLoading).toHaveBeenLastCalledWith(false);
  });

  test("registrarUsuario - error genérico (Network timeout)", async () => {
    const error = new Error("Network timeout");
    mockFetch.mockRejectedValue(error);

    await registrarUsuario(params.nombre, params.apellidos, params.correo, params.contrasena, {
      setLoading,
      setError,
    });

    // C4: error es Error pero no TypeError con fetch
    expect(error instanceof Error).toBe(true);
    expect(error.name).not.toBe("TypeError");
    expect(error.message).not.toContain("fetch");

    // C4: setError con mensaje genérico
    expect(setError).toHaveBeenCalledWith("Error al conectar con el servidor: Network timeout");

    // C4: setLoading(false)
    expect(setLoading).toHaveBeenLastCalledWith(false);
  });

  test("registrarUsuario - error lanzado como string", async () => {
    mockFetch.mockRejectedValue("error_cadena");

    await registrarUsuario(params.nombre, params.apellidos, params.correo, params.contrasena, {
      setLoading,
      setError,
    });

    // C5: el valor rechazado no es instancia de Error
    expect("error_cadena" instanceof Error).toBe(false);

    // C5: setError con mensaje desconocido
    expect(setError).toHaveBeenCalledWith("Error desconocido al conectar con el servidor");

    // C5: setLoading(false)
    expect(setLoading).toHaveBeenLastCalledWith(false);
  });
});
