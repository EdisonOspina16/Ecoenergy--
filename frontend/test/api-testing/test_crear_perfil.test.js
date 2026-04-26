/**
 * Pruebas Unitarias - Frontend
 * Función: crearPerfil
 * Framework: Vitest
 */

import { describe, test, expect } from "vitest";

async function crearPerfil(address, homeName, fetchFn) {
  if (!address || !homeName) {
    return {
      mensaje: "La dirección y el nombre del hogar son requeridos",
      tipoMensaje: "error",
    };
  }

  try {
    const response = await fetchFn("/api/perfil", {
      method: "POST",
      body: JSON.stringify({ address, homeName }),
    });
    const data = await response.json();

    if (data.success) {
      return { mensaje: data.message, tipoMensaje: "success" };
    } else {
      return { mensaje: data.error, tipoMensaje: "error" };
    }
  } catch (e) {
    return {
      mensaje: "Error al conectar con el servidor",
      tipoMensaje: "error",
    };
  }
}

describe("crearPerfil", () => {
  test("C1 - Datos válidos, success=true: muestra mensaje de éxito", async () => {
    const fetchFn = async () => ({
      ok: true,
      json: async () => ({
        success: true,
        message: "Perfil creado correctamente",
      }),
    });

    const resultado = await crearPerfil("Calle 123", "Mi Hogar", fetchFn);

    expect(resultado.tipoMensaje).toBe("success");
    expect(resultado.mensaje).toBe("Perfil creado correctamente");
  });

  test("C2 - Datos válidos, success=false: muestra mensaje de error", async () => {
    const fetchFn = async () => ({
      ok: true,
      json: async () => ({ success: false, error: "Error al guardar perfil" }),
    });

    const resultado = await crearPerfil("Calle 123", "Mi Hogar", fetchFn);

    expect(resultado.tipoMensaje).toBe("error");
    expect(resultado.mensaje).toBe("Error al guardar perfil");
  });

  test("C3 - Error de red: fetch lanza excepción", async () => {
    const fetchFn = async () => {
      throw new Error("fetch error");
    };

    const resultado = await crearPerfil("Calle 123", "Mi Hogar", fetchFn);

    expect(resultado.tipoMensaje).toBe("error");
    expect(resultado.mensaje).toBe("Error al conectar con el servidor");
  });

  test("C4 - Validación falla: campos vacíos", async () => {
    const fetchFn = async () => ({});

    const resultado = await crearPerfil("", "", fetchFn);

    expect(resultado.tipoMensaje).toBe("error");
    expect(resultado.mensaje).toBe(
      "La dirección y el nombre del hogar son requeridos",
    );
  });
});
