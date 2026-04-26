import React from "react";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, it, vi } from "vitest";
import Profile from "@/app/perfil/page";
import { expect } from "chai";

const makeResponse = (body: any, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json" },
  });

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
      .spyOn(globalThis, "fetch")
      .mockResolvedValueOnce(makeResponse(profilePayload));

    vi.spyOn(globalThis, "confirm").mockReturnValue(false);

    renderProfile();
    await waitForListado();

    await userEvent.click(screen.getByTitle(/eliminar dispositivo/i));

    expect(fetchMock.mock.calls.length).to.equal(1); // Solo el GET inicial
    expect(screen.queryByDisplayValue("Tomacorriente Sala")).to.not.equal(null);
  });

  it("CP-DEL-002 elimina el dispositivo y muestra mensaje de éxito", async () => {
    const fetchMock = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValueOnce(makeResponse(profilePayload))
      .mockResolvedValueOnce(makeResponse({ success: true }));

    vi.spyOn(globalThis, "confirm").mockReturnValue(true);

    renderProfile();
    await waitForListado();

    await userEvent.click(screen.getByTitle(/eliminar dispositivo/i));

    await waitFor(() => {
      expect(screen.queryByDisplayValue("Tomacorriente Sala")).to.equal(null);
    });
    expect(
      screen.queryByText(/Dispositivo eliminado exitosamente/i),
    ).to.not.equal(null);
    expect(fetchMock.mock.calls.length).to.equal(2);
  });

  it("CP-DEL-003 muestra error del backend y conserva el dispositivo", async () => {
    const fetchMock = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValueOnce(makeResponse(profilePayload))
      .mockResolvedValueOnce(
        makeResponse({ success: false, error: "No se pudo" }, 400),
      );

    vi.spyOn(globalThis, "confirm").mockReturnValue(true);

    renderProfile();
    await waitForListado();

    await userEvent.click(screen.getByTitle(/eliminar dispositivo/i));

    await waitFor(() => {
      expect(screen.queryByText(/No se pudo/i)).to.not.equal(null);
    });
    expect(screen.queryByDisplayValue("Tomacorriente Sala")).to.not.equal(null);
    expect(fetchMock.mock.calls.length).to.equal(2);
  });

  it("CP-DEL-004 usa el mensaje por defecto cuando el backend no envía 'error'", async () => {
    const fetchMock = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValueOnce(makeResponse(profilePayload))
      .mockResolvedValueOnce(makeResponse({ success: false }));

    vi.spyOn(globalThis, "confirm").mockReturnValue(true);

    renderProfile();
    await waitForListado();

    await userEvent.click(screen.getByTitle(/eliminar dispositivo/i));

    await waitFor(() => {
      expect(
        screen.queryByText(/Error al eliminar el dispositivo/i),
      ).to.not.equal(null);
    });
    expect(screen.queryByDisplayValue("Tomacorriente Sala")).to.not.equal(null);
    expect(fetchMock.mock.calls.length).to.equal(2);
  });

  it("CP-DEL-005 maneja error de red al eliminar y notifica con fallback", async () => {
    const fetchMock = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValueOnce(makeResponse(profilePayload))
      .mockRejectedValueOnce(new Error("Network down"));

    vi.spyOn(globalThis, "confirm").mockReturnValue(true);
    const consoleErrorSpy = vi
      .spyOn(console, "error")
      .mockImplementation(() => {});

    renderProfile();
    await waitForListado();

    await userEvent.click(screen.getByTitle(/eliminar dispositivo/i));

    await waitFor(() => {
      expect(
        screen.queryByText(/Error al conectar con el servidor/i),
      ).to.not.equal(null);
    });
    const errorCalls = consoleErrorSpy.mock.calls;
    expect(errorCalls.length).to.equal(1);
    expect(errorCalls[0][0]).to.equal("Error al eliminar dispositivo:");
    expect(errorCalls[0][1]).to.be.instanceOf(Error);
    expect(screen.queryByDisplayValue("Tomacorriente Sala")).to.not.equal(null);
    expect(fetchMock.mock.calls.length).to.equal(2);
  });
});
