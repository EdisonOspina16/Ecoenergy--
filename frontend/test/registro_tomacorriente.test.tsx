import React from "react";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";
import Profile from "../app/perfil/page";

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

const waitForFormulario = async () => {
  await waitFor(() => screen.getByText(/Registrar Nuevo Tomacorriente/i));
};

afterEach(() => {
  vi.restoreAllMocks();
});

describe("Registro de tomacorriente", () => {
  it("CP-TOM-FR-001 registro tomacorriente válido", async () => {
    const fetchSpy = setupFetch(
      makeResponse({ success: true, hogar: {}, dispositivos: [] }),
      makeResponse(
        {
          success: true,
          dispositivo: {
            id: 1,
            name: "Nevera",
            icon: "plug",
            connected: false,
          },
        },
        201,
      ),
    );

    render(<Profile />);
    await waitForFormulario();

    await userEvent.type(
      screen.getByPlaceholderText("Ingresa el código del dispositivo"),
      "TOM001",
    );
    await userEvent.type(
      screen.getByPlaceholderText("Ej: Cargador del móvil"),
      "Nevera",
    );
    await userEvent.click(
      screen.getByRole("button", { name: /Registrar Tomacorriente/i }),
    );

    await waitFor(() =>
      screen.getByText(/Dispositivo registrado exitosamente/i),
    );
    expect(fetchSpy).toHaveBeenCalledTimes(2);
    expect(screen.getByDisplayValue("Nevera")).toBeInTheDocument();
  });

  it("CP-FR dispositivo existente muestra error", async () => {
    setupFetch(
      makeResponse({ success: true, hogar: {}, dispositivos: [] }),
      makeResponse(
        { success: false, error: "Este dispositivo ya está registrado" },
        400,
      ),
    );

    render(<Profile />);
    await waitForFormulario();

    await userEvent.type(
      screen.getByPlaceholderText("Ingresa el código del dispositivo"),
      "TOM001",
    );
    await userEvent.type(
      screen.getByPlaceholderText("Ej: Cargador del móvil"),
      "Microondas",
    );
    await userEvent.click(
      screen.getByRole("button", { name: /Registrar Tomacorriente/i }),
    );

    await waitFor(() => screen.getByText(/ya está registrado/i));
  });

  it("CP-FR apodo demasiado largo produce error genérico", async () => {
    setupFetch(
      makeResponse({ success: true, hogar: {}, dispositivos: [] }),
      makeResponse({ success: false, error: "Apodo demasiado largo" }, 500),
    );

    render(<Profile />);
    await waitForFormulario();

    const apodoLargo =
      "Este es un apodo extremadamente largo que supera los cincuenta caracteres permitidos por el sistema jijiji";

    await userEvent.type(
      screen.getByPlaceholderText("Ingresa el código del dispositivo"),
      "TOM004",
    );
    await userEvent.type(
      screen.getByPlaceholderText("Ej: Cargador del móvil"),
      apodoLargo,
    );
    await userEvent.click(
      screen.getByRole("button", { name: /Registrar Tomacorriente/i }),
    );

    await waitFor(() => screen.getByText(/apodo demasiado largo/i));
  });

  it("CP-FR registra múltiples dispositivos consecutivos", async () => {
    setupFetch(
      makeResponse({ success: true, hogar: {}, dispositivos: [] }),
      makeResponse(
        {
          success: true,
          dispositivo: {
            id: 10,
            name: "Aire Acondicionado",
            icon: "plug",
            connected: false,
          },
        },
        201,
      ),
      makeResponse(
        {
          success: true,
          dispositivo: {
            id: 11,
            name: "Horno",
            icon: "plug",
            connected: false,
          },
        },
        201,
      ),
      makeResponse(
        {
          success: true,
          dispositivo: {
            id: 12,
            name: "Lavadora",
            icon: "plug",
            connected: false,
          },
        },
        201,
      ),
    );

    render(<Profile />);
    await waitForFormulario();

    const registrar = async (id: string, alias: string) => {
      await userEvent.clear(
        screen.getByPlaceholderText("Ingresa el código del dispositivo"),
      );
      await userEvent.clear(
        screen.getByPlaceholderText("Ej: Cargador del móvil"),
      );
      await userEvent.type(
        screen.getByPlaceholderText("Ingresa el código del dispositivo"),
        id,
      );
      await userEvent.type(
        screen.getByPlaceholderText("Ej: Cargador del móvil"),
        alias,
      );
      await userEvent.click(
        screen.getByRole("button", { name: /Registrar Tomacorriente/i }),
      );
      await waitFor(() =>
        screen.getByText(/Dispositivo registrado exitosamente/i),
      );
    };

    await registrar("TOM005", "Aire Acondicionado");
    await registrar("TOM006", "Horno");
    await registrar("TOM007", "Lavadora");

    expect(screen.getByDisplayValue("Aire Acondicionado")).toBeInTheDocument();
    expect(screen.getByDisplayValue("Horno")).toBeInTheDocument();
    expect(screen.getByDisplayValue("Lavadora")).toBeInTheDocument();
  });

  it("CP-FR apodo con caracteres especiales se muestra", async () => {
    setupFetch(
      makeResponse({ success: true, hogar: {}, dispositivos: [] }),
      makeResponse(
        {
          success: true,
          dispositivo: {
            id: 20,
            name: "Cargador@Móvil#2024",
            icon: "plug",
            connected: false,
          },
        },
        201,
      ),
    );

    render(<Profile />);
    await waitForFormulario();

    await userEvent.type(
      screen.getByPlaceholderText("Ingresa el código del dispositivo"),
      "TOM008",
    );
    await userEvent.type(
      screen.getByPlaceholderText("Ej: Cargador del móvil"),
      "Cargador@Móvil#2024",
    );
    await userEvent.click(
      screen.getByRole("button", { name: /Registrar Tomacorriente/i }),
    );

    await waitFor(() => screen.getByDisplayValue("Cargador@Móvil#2024"));
  });
});
