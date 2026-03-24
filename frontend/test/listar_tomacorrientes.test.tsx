import React from "react";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";
import Profile from "../src/app/perfil/page";

const makeResponse = (body: any, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json" },
  }) as any;

const setupFetch = (...responses: Response[]) => {
  const spy = vi.spyOn(global, "fetch");
  responses.forEach((res) => spy.mockResolvedValueOnce(res as any));
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

    expect(screen.getByDisplayValue("Cargador")).toBeInTheDocument();
    expect(screen.getByDisplayValue("Lavadora")).toBeInTheDocument();
  });

  it("CP-LIST-002 lista vacía muestra mensaje", async () => {
    setupFetch(makeResponse({ success: true, hogar: {}, dispositivos: [] }));

    render(<Profile />);
    await waitForListado();

    expect(
      screen.getByText(/No tienes dispositivos registrados/i),
    ).toBeInTheDocument();
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
    expect(desconectados.length).toBeGreaterThanOrEqual(1);
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
    expect(conectados.length).toBeGreaterThanOrEqual(1);
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

    expect(
      screen.getByRole("button", { name: /Desconectar/i }),
    ).toBeInTheDocument();
    expect(screen.getByTitle(/Eliminar dispositivo/i)).toBeInTheDocument();
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
      expect(screen.getByDisplayValue(d.name)).toBeInTheDocument();
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
    expect(screen.getByDisplayValue("Cafetera")).toBeInTheDocument();

    first.unmount();
    render(<Profile />);
    await waitForListado();
    expect(screen.getByDisplayValue("Cafetera")).toBeInTheDocument();
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

    expect(screen.getByTitle("Eliminar dispositivo")).toBeInTheDocument();
  });
});
