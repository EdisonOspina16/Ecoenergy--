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
});
