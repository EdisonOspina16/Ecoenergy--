import { describe, it, vi, beforeEach } from "vitest";
import { fetchPerfil, postProfile } from "@/lib/api/profile";
import { postRecuperar } from "@/lib/api/recuperar";
import { postSubscribe } from "@/lib/api/subscribe";
import { expect } from "chai";

// Usaremos un Stub global sobre fetch para simular el comportamiento de jsonClient que consume estas APIs
describe("Capas API REST (lib/api/*)", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  describe("API: Perfil", () => {
    it("fetchPerfil debería hacer una solicitud GET a /perfil", async () => {
      // === Arrange ===
      globalThis.fetch = vi.fn().mockResolvedValue({
        ok: true,
        status: 200,
        headers: new Headers({ "content-type": "application/json" }),
        json: async () => ({
          success: true,
          hogar: { nombre_hogar: "Mi casa test" },
        }),
      });

      // === Act ===
      const result = await fetchPerfil();

      // === Assert ===
      const fetchCalls = vi.mocked(globalThis.fetch).mock.calls;
      expect(fetchCalls.length).to.equal(1);
      const [url, init] = fetchCalls[0] as [string, RequestInit];
      expect(url).to.contain("/perfil");
      expect(init.method).to.equal("GET");
      expect(result.ok).to.equal(true);
      if (result.ok) {
        expect(result.data.hogar?.nombre_hogar).to.equal("Mi casa test");
      }
    });

    it("postProfile debería hacer una solicitud POST a /perfil con payload correcto", async () => {
      // === Arrange ===
      globalThis.fetch = vi.fn().mockResolvedValue({
        ok: true,
        status: 200,
        headers: new Headers({ "content-type": "application/json" }),
        json: async () => ({ success: true, message: "OK" }),
      });

      const payload = { address: "123", nombre_hogar: "Hogar" };

      // === Act ===
      await postProfile(payload);

      // === Assert ===
      const fetchCalls = vi.mocked(globalThis.fetch).mock.calls;
      expect(fetchCalls.length).to.equal(1);
      const [url, init] = fetchCalls[0] as [string, RequestInit];
      expect(url).to.contain("/perfil");
      expect(init.method).to.equal("POST");
      expect(init.body).to.equal(JSON.stringify(payload));
    });
  });

  describe("API: Recuperar", () => {
    it("postRecuperar debería procesar POST correctamente", async () => {
      // === Arrange ===
      globalThis.fetch = vi.fn().mockResolvedValue({
        ok: false,
        status: 400,
        headers: new Headers({ "content-type": "application/json" }),
        json: async () => ({ error: "Token invalido" }),
      });

      const payload = { correo: "test@test.com", nueva_contrasena: "123" };

      // === Act ===
      const result = await postRecuperar(payload);

      // === Assert ===
      const fetchCalls = vi.mocked(globalThis.fetch).mock.calls;
      expect(fetchCalls.length).to.equal(1);
      const [url, init] = fetchCalls[0] as [string, RequestInit];
      expect(url).to.contain("/recuperar");
      expect(init.method).to.equal("POST");
      expect(result.ok).to.equal(false);
      // jsonClient extrae el error como result.message
      if (!result.ok) {
        expect(result.message).to.equal("Token invalido");
      }
    });
  });

  describe("API: Subscribe", () => {
    it("postSubscribe debería procesar error de red como fallo genérico (Network Error)", async () => {
      // === Arrange ===
      globalThis.fetch = vi
        .fn()
        .mockRejectedValue(new TypeError("Failed to fetch"));

      const payload = { email: "fail@ecoenergy.com" };

      // === Act ===
      const result = await postSubscribe(payload);

      // === Assert ===
      // Esto valida la función del jsonClient cuando el fetch falla puramente
      expect(result.ok).to.equal(false);
      if (!result.ok) {
        expect(result.message).to.contain("No se puede conectar"); // mapNetworkError fallback
      }
    });

    it("postSubscribe debería retornar payload de exito", async () => {
      globalThis.fetch = vi.fn().mockResolvedValue({
        ok: true,
        status: 200,
        headers: new Headers({ "content-type": "application/json" }),
        json: async () => ({ success: true }),
      });
      const result = await postSubscribe({ email: "ok@eco.com" });
      expect(result.ok).to.equal(true);
    });
  });
});
