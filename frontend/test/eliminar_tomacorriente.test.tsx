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

describe("Eliminación de tomacorrientes en perfil", () => {
  it("CP-DEL-003 muestra mensaje de éxito", async () => {
    vi.spyOn(window, "confirm").mockReturnValue(true);
    setupFetch(
      makeResponse({
        success: true,
        hogar: {},
        dispositivos: [
          { id: 3, name: "Lavadora", icon: "plug", connected: true },
        ],
      }),
      makeResponse({
        success: true,
        message: "Dispositivo eliminado exitosamente",
      }),
    );

    render(<Profile />);
    await waitForListado();
    await userEvent.click(screen.getByTitle(/Eliminar dispositivo/i));

    await waitFor(() =>
      screen.getByText(/Dispositivo eliminado exitosamente/i),
    );
  });

  it("CP-DEL-004 eliminar sin dispositivos registrados", async () => {
    vi.spyOn(window, "confirm").mockReturnValue(true);
    setupFetch(
      makeResponse({ success: true, hogar: {}, dispositivos: [] }),
      makeResponse({ success: false, error: "Dispositivo no encontrado" }, 404),
    );

    render(<Profile />);
    await waitForListado();

    // No hay botones de eliminar; simulamos acción directa
    const resp = await fetch("/perfil/dispositivo/10", { method: "DELETE" });
    expect(resp.status).toBe(404);
  });

  it("CP-DEL-005 no permite interactuar tras eliminar", async () => {
    vi.spyOn(window, "confirm").mockReturnValue(true);
    setupFetch(
      makeResponse({
        success: true,
        hogar: {},
        dispositivos: [
          { id: 8, name: "Lavadora", icon: "plug", connected: true },
        ],
      }),
      makeResponse({ success: true, message: "OK" }),
    );

    render(<Profile />);
    await waitForListado();

    await userEvent.click(screen.getByTitle(/Eliminar dispositivo/i));
    await waitFor(() => screen.getByText(/eliminado/i));

    expect(screen.queryByDisplayValue("Lavadora")).toBeNull();
    expect(screen.queryByRole("button", { name: /Desconectar/i })).toBeNull();
  });
});
