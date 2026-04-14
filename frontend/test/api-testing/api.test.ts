import { describe, it, expect, vi, beforeEach } from 'vitest';
import { fetchPerfil, postProfile } from '../src/lib/api/profile';
import { postRecuperar } from '../src/lib/api/recuperar';
import { postSubscribe } from '../src/lib/api/subscribe';

// Usaremos un Stub global sobre fetch para simular el comportamiento de jsonClient que consume estas APIs
describe('Capas API REST (lib/api/*)', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  describe('API: Perfil', () => {
    it('fetchPerfil debería hacer una solicitud GET a /perfil', async () => {
      // === Arrange ===
      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        status: 200,
        headers: new Headers({ 'content-type': 'application/json' }),
        json: async () => ({ success: true, hogar: { nombre_hogar: "Mi casa test" } })
      });

      // === Act ===
      const result = await fetchPerfil();

      // === Assert ===
      expect(global.fetch).toHaveBeenCalledWith(expect.stringContaining('/perfil'), expect.objectContaining({ method: 'GET' }));
      expect(result.ok).toBe(true);
      if (result.ok) {
        expect(result.data.hogar?.nombre_hogar).toBe("Mi casa test");
      }
    });

    it('postProfile debería hacer una solicitud POST a /perfil con payload correcto', async () => {
      // === Arrange ===
      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        status: 200,
        headers: new Headers({ 'content-type': 'application/json' }),
        json: async () => ({ success: true, message: "OK" })
      });

      const payload = { address: "123", nombre_hogar: "Hogar" };

      // === Act ===
      await postProfile(payload);

      // === Assert ===
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/perfil'),
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify(payload)
        })
      );
    });
  });

  describe('API: Recuperar', () => {
    it('postRecuperar debería procesar POST correctamente', async () => {
      // === Arrange ===
      global.fetch = vi.fn().mockResolvedValue({
        ok: false,
        status: 400,
        headers: new Headers({ 'content-type': 'application/json' }),
        json: async () => ({ error: "Token invalido" })
      });

      const payload = { correo: "test@test.com", nueva_contrasena: "123" };

      // === Act ===
      const result = await postRecuperar(payload);

      // === Assert ===
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/recuperar'),
        expect.objectContaining({ method: 'POST' })
      );
      expect(result.ok).toBe(false);
      // jsonClient extrae el error como result.message
      if (!result.ok) {
        expect(result.message).toBe("Token invalido");
      }
    });
  });

  describe('API: Subscribe', () => {
    it('postSubscribe debería procesar error de red como fallo genérico (Network Error)', async () => {
      // === Arrange ===
      global.fetch = vi.fn().mockRejectedValue(new TypeError("Failed to fetch"));

      const payload = { email: "fail@ecoenergy.com" };

      // === Act ===
      const result = await postSubscribe(payload);

      // === Assert ===
      // Esto valida la función del jsonClient cuando el fetch falla puramente
      expect(result.ok).toBe(false);
      if (!result.ok) {
        expect(result.message).toContain("No se puede conectar"); // mapNetworkError fallback 
      }
    });

    it('postSubscribe debería retornar payload de exito', async () => {
       global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        status: 200,
        headers: new Headers({ 'content-type': 'application/json' }),
        json: async () => ({ success: true })
      });
      const result = await postSubscribe({ email: "ok@eco.com" });
      expect(result.ok).toBe(true);
    });
  });
});
