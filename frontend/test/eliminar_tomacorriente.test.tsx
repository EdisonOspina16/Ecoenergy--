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

const profilePayload = {
  success: true,
  hogar: { direccion: "Calle 123", nombre_hogar: "Mi hogar" },
  dispositivos: [
    { id: 1, name: "Tomacorriente Sala", icon: "lightbulb", connected: true },
  ],
};

const renderProfile = () => render(<Profile />);

const waitForListado = async () => {
  await waitFor(() => screen.getByText(/Mis Dispositivos/i));
};

afterEach(() => {
  vi.restoreAllMocks();
});

describe("Eliminación de tomacorrientes en perfil", () => {
  it("CP-DEL-001 no elimina si el usuario cancela la confirmación", async () => {
    const fetchMock = vi
      .spyOn(global, "fetch")
      .mockResolvedValueOnce(makeResponse(profilePayload));

    vi.spyOn(window, "confirm").mockReturnValue(false);

    renderProfile();
    await waitForListado();

    await userEvent.click(screen.getByTitle(/eliminar dispositivo/i));

    expect(fetchMock).toHaveBeenCalledTimes(1); // Solo el GET inicial
    expect(screen.getByDisplayValue("Tomacorriente Sala")).toBeInTheDocument();
  });

  it("CP-DEL-002 elimina el dispositivo y muestra mensaje de éxito", async () => {
    const fetchMock = vi
      .spyOn(global, "fetch")
      .mockResolvedValueOnce(makeResponse(profilePayload))
      .mockResolvedValueOnce(makeResponse({ success: true }));

    vi.spyOn(window, "confirm").mockReturnValue(true);

    renderProfile();
    await waitForListado();

    await userEvent.click(screen.getByTitle(/eliminar dispositivo/i));

    await waitFor(() =>
      expect(
        screen.queryByDisplayValue("Tomacorriente Sala"),
      ).not.toBeInTheDocument(),
    );
    expect(
      screen.getByText(/Dispositivo eliminado exitosamente/i),
    ).toBeInTheDocument();
    expect(fetchMock).toHaveBeenCalledTimes(2);
  });

  it("CP-DEL-003 muestra error del backend y conserva el dispositivo", async () => {
    const fetchMock = vi
      .spyOn(global, "fetch")
      .mockResolvedValueOnce(makeResponse(profilePayload))
      .mockResolvedValueOnce(
        makeResponse({ success: false, error: "No se pudo" }, 400),
      );

    vi.spyOn(window, "confirm").mockReturnValue(true);

    renderProfile();
    await waitForListado();

    await userEvent.click(screen.getByTitle(/eliminar dispositivo/i));

    await waitFor(() =>
      expect(screen.getByText(/No se pudo/i)).toBeInTheDocument(),
    );
    expect(screen.getByDisplayValue("Tomacorriente Sala")).toBeInTheDocument();
    expect(fetchMock).toHaveBeenCalledTimes(2);
  });

  it("CP-DEL-004 usa el mensaje por defecto cuando el backend no envía 'error'", async () => {
    const fetchMock = vi
      .spyOn(global, "fetch")
      .mockResolvedValueOnce(makeResponse(profilePayload))
      .mockResolvedValueOnce(makeResponse({ success: false }));

    vi.spyOn(window, "confirm").mockReturnValue(true);

    renderProfile();
    await waitForListado();

    await userEvent.click(screen.getByTitle(/eliminar dispositivo/i));

    await waitFor(() =>
      expect(
        screen.getByText(/Error al eliminar el dispositivo/i),
      ).toBeInTheDocument(),
    );
    expect(screen.getByDisplayValue("Tomacorriente Sala")).toBeInTheDocument();
    expect(fetchMock).toHaveBeenCalledTimes(2);
  });

  it("CP-DEL-005 maneja error de red al eliminar y notifica con fallback", async () => {
    const fetchMock = vi
      .spyOn(global, "fetch")
      .mockResolvedValueOnce(makeResponse(profilePayload))
      .mockRejectedValueOnce(new Error("Network down"));

    vi.spyOn(window, "confirm").mockReturnValue(true);
    const consoleErrorSpy = vi
      .spyOn(console, "error")
      .mockImplementation(() => {});

    renderProfile();
    await waitForListado();

    await userEvent.click(screen.getByTitle(/eliminar dispositivo/i));

    await waitFor(() =>
      expect(
        screen.getByText(/Error al conectar con el servidor/i),
      ).toBeInTheDocument(),
    );
    expect(consoleErrorSpy).toHaveBeenCalledWith(
      "Error al eliminar dispositivo:",
      expect.any(Error),
    );
    expect(screen.getByDisplayValue("Tomacorriente Sala")).toBeInTheDocument();
    expect(fetchMock).toHaveBeenCalledTimes(2);
  });
});
