import React from "react";
import { render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, it, vi } from "vitest";
import Profile from "@/app/perfil/page";
import { expect } from "chai";

const makeResponse = (body: any, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json" },
  });

const setupFetch = (...responses: Response[]) => {
  const spy = vi.spyOn(globalThis, "fetch");
  responses.forEach((res) => spy.mockResolvedValueOnce(res));
  return spy;
};

const waitForListado = async () => {
  await waitFor(() => screen.getByText(/Mis Dispositivos/i));
};

afterEach(() => {
  vi.restoreAllMocks();
});

describe("Listado de tomacorrientes en perfil", () => {
  it("CP-LIST-001 muestra dispositivos registrados", async () => {
    setupFetch(
      makeResponse({
        success: true,
        hogar: {},
        dispositivos: [
          { id: 1, name: "Cargador", icon: "plug", connected: false },
          { id: 2, name: "Lavadora", icon: "plug", connected: true },
        ],
      }),
    );

    render(<Profile />);
    await waitForListado();

    expect(screen.queryByDisplayValue("Cargador")).to.not.equal(null);
    expect(screen.queryByDisplayValue("Lavadora")).to.not.equal(null);
  });

  it("CP-LIST-002 lista vacía muestra mensaje", async () => {
    setupFetch(makeResponse({ success: true, hogar: {}, dispositivos: [] }));

    render(<Profile />);
    await waitForListado();

    expect(
      screen.queryByText(/No tienes dispositivos registrados/i),
    ).to.not.equal(null);
  });

  it("CP-LIST-003 estado desconectado visible", async () => {
    setupFetch(
      makeResponse({
        success: true,
        hogar: {},
        dispositivos: [
          { id: 3, name: "Cargador", icon: "plug", connected: false },
        ],
      }),
    );

    render(<Profile />);
    await waitForListado();
    const desconectados = screen.getAllByText(/Desconectado/i);
    expect(desconectados.length).to.be.greaterThan(0);
  });

  it("CP-LIST-004 estado conectado visible", async () => {
    setupFetch(
      makeResponse({
        success: true,
        hogar: {},
        dispositivos: [
          { id: 4, name: "Lavadora", icon: "plug", connected: true },
        ],
      }),
    );

    render(<Profile />);
    await waitForListado();

    const conectados = screen.getAllByText(/Conectado/i);
    expect(conectados.length).to.be.greaterThan(0);
  });

  it("CP-LIST-005 botones de acción presentes", async () => {
    setupFetch(
      makeResponse({
        success: true,
        hogar: {},
        dispositivos: [
          { id: 5, name: "Microondas", icon: "plug", connected: true },
        ],
      }),
    );

    render(<Profile />);
    await waitForListado();

    expect(screen.queryByRole("button", { name: /Desconectar/i })).to.not.equal(
      null,
    );
    expect(screen.queryByTitle(/Eliminar dispositivo/i)).to.not.equal(null);
  });

  it("CP-LIST-007 soporta múltiples dispositivos (5+)", async () => {
    const muchos_dispositivos = Array.from({ length: 6 }, (_, i) => ({
      id: i + 10,
      name: `Disp-${i + 1}`,
      icon: "plug",
      connected: i % 2 === 0,
    }));

    setupFetch(
      makeResponse({
        success: true,
        hogar: {},
        dispositivos: muchos_dispositivos,
      }),
    );

    render(<Profile />);
    await waitForListado();

    muchos_dispositivos.forEach((d) => {
      expect(screen.queryByDisplayValue(d.name)).to.not.equal(null);
    });
  });

  it("CP-LIST-008 refresh mantiene lista", async () => {
    setupFetch(
      makeResponse({
        success: true,
        hogar: {},
        dispositivos: [
          { id: 30, name: "Cafetera", icon: "plug", connected: true },
        ],
      }),
      makeResponse({
        success: true,
        hogar: {},
        dispositivos: [
          { id: 30, name: "Cafetera", icon: "plug", connected: true },
        ],
      }),
    );

    const first = render(<Profile />);
    await waitForListado();
    expect(screen.queryByDisplayValue("Cafetera")).to.not.equal(null);

    first.unmount();
    render(<Profile />);
    await waitForListado();
    expect(screen.queryByDisplayValue("Cafetera")).to.not.equal(null);
  });

  it("CP-LIST-009 tooltip eliminar presente", async () => {
    setupFetch(
      makeResponse({
        success: true,
        hogar: {},
        dispositivos: [
          { id: 40, name: "Cargador", icon: "plug", connected: false },
        ],
      }),
    );

    render(<Profile />);
    await waitForListado();

    expect(screen.queryByTitle("Eliminar dispositivo")).to.not.equal(null);
  });

  it("CP-LIST-010 redirige a login en 401", async () => {
    const originalLocation = globalThis.location;
    delete (globalThis as any).location;
    globalThis.location = { ...originalLocation, href: "" } as Location;

    setupFetch(makeResponse({}, 401));

    render(<Profile />);
    await waitFor(() => {
      expect(globalThis.location.href).to.equal("/login");
    });

    globalThis.location = originalLocation;
  });

  it("CP-LIST-011 muestra error y limpia dispositivos en fallo", async () => {
    setupFetch(makeResponse({ error: "fallo" }, 500));

    render(<Profile />);
    await waitForListado();

    await screen.findByText(/Error 500|fallo/i);
    expect(
      screen.queryByText(/No tienes dispositivos registrados/i),
    ).to.not.equal(null);
  });

  it("CP-LIST-012 dispositivos undefined cae a lista vacía", async () => {
    setupFetch(
      makeResponse({ success: true, hogar: {}, dispositivos: undefined }),
    );

    render(<Profile />);
    await waitForListado();

    expect(
      screen.queryByText(/No tienes dispositivos registrados/i),
    ).to.not.equal(null);
  });

  it("CP-LIST-013 hogar nulo no rompe y lista dispositivos", async () => {
    setupFetch(
      makeResponse({
        success: true,
        hogar: null,
        dispositivos: [
          { id: 77, name: "Sensor", icon: "plug", connected: true },
        ],
      }),
    );

    render(<Profile />);
    await waitForListado();

    expect(screen.queryByDisplayValue("Sensor")).to.not.equal(null);
  });
});
