/**
 * Pruebas Unitarias - Frontend
 * Función: cambiarContrasena
 * Framework: Vitest
 */

import { describe, test, expect } from "vitest";

// ── Función bajo prueba ──────────────────────────────────────────

async function cambiarContrasena(correo, nuevaContrasena, fetchFn) {
    let success = null;
    let error = null;
    let redirect = null;

    try {
        const response = await fetchFn("/api/cambiar-contrasena", {
            method: "POST",
            body: JSON.stringify({ correo, nuevaContrasena })
        });

        if (response.ok) {
            const data = await response.json();
            success = data.message;
            redirect = "/login";
        } else {
            const data = await response.json();
            error = data.error;
        }
    } catch (e) {
        error = "Error al conectar con el servidor";
    }

    return { success, error, redirect };
}

// ── PRUEBAS ─────────────────────────────────────────────────────

describe("cambiarContrasena", () => {

    test("C1 - Flujo exitoso: response.ok=true, redirige a /login", async () => {
        const fetchFn = async () => ({
            ok: true,
            json: async () => ({ message: "Contraseña actualizada" })
        });

        const resultado = await cambiarContrasena("user@test.com", "Segura123!", fetchFn);

        expect(resultado.success).toBe("Contraseña actualizada");
        expect(resultado.redirect).toBe("/login");
        expect(resultado.error).toBeNull();
    });

    test("C2 - Correo no existe: response.ok=false, muestra error", async () => {
        const fetchFn = async () => ({
            ok: false,
            json: async () => ({ error: "Usuario no encontrado" })
        });

        const resultado = await cambiarContrasena("noexiste@x.com", "Clave456!", fetchFn);

        expect(resultado.error).toBe("Usuario no encontrado");
        expect(resultado.redirect).toBeNull();
        expect(resultado.success).toBeNull();
    });

    test("C3 - Error de red: fetch lanza excepción, muestra error de servidor", async () => {
        const fetchFn = async () => { throw new TypeError("Failed to fetch"); };

        const resultado = await cambiarContrasena("user@test.com", "Pass789!", fetchFn);

        expect(resultado.error).toBe("Error al conectar con el servidor");
        expect(resultado.success).toBeNull();
        expect(resultado.redirect).toBeNull();
    });

});