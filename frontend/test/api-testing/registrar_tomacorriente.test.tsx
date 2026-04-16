import React from "react";
import { render, screen, waitFor, fireEvent } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import Profile from "@/app/perfil/page";
import { registerDevice } from "@/lib/api/devices";

vi.mock("@/lib/api/devices", () => ({ registerDevice: vi.fn() }));

const makeResponse = (body: any, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json" },
  }) as any;

const renderPerfil = () => {
  vi.spyOn(global, "fetch").mockResolvedValue(
    makeResponse({ success: true, hogar: {}, dispositivos: [] }) as any,
  );
  return render(<Profile />);
};

afterEach(() => {
  vi.restoreAllMocks();
});

const fillNicknameOnly = () => {
  const nicknameInput = screen.getByPlaceholderText(/Cargador del móvil/i);
  fireEvent.change(nicknameInput, { target: { value: "Mi enchufe" } });
  return { nicknameInput };
};

const fillAllFields = () => {
  const idInput = screen.getByPlaceholderText(
    /Ingresa el código del dispositivo/i,
  );
  const nicknameInput = screen.getByPlaceholderText(/Cargador del móvil/i);
  fireEvent.change(idInput, { target: { value: "ABC-123" } });
  fireEvent.change(nicknameInput, { target: { value: "Patio" } });
  return { idInput, nicknameInput };
};

const submitRegistro = () => {
  const form = screen.getByText(/Registrar Tomacorriente/i).closest("form")!;
  fireEvent.submit(form);
};

describe("Registrar tomacorriente - handleDeviceRegister", () => {
  it("muestra error cuando falta el ID (validación y mostrarMensaje)", async () => {
    renderPerfil();
    await screen.findByText(/Registrar Nuevo Tomacorriente/i);

    fillNicknameOnly();
    submitRegistro();

    await screen.findByText(/Ingresa el ID del dispositivo/i);
    expect(registerDevice).not.toHaveBeenCalled();
  }, 8000);

  it("agrega el dispositivo y limpia el formulario cuando el registro es exitoso", async () => {
    vi.mocked(registerDevice).mockResolvedValue({
      ok: true,
      data: {
        id: 99,
        name: "Tomacorriente Patio",
        icon: "plug",
        connected: false,
      },
      message: "Dispositivo registrado exitosamente",
    });

    renderPerfil();
    await screen.findByText(/Registrar Nuevo Tomacorriente/i);

    const { idInput, nicknameInput } = fillAllFields();
    submitRegistro();

    await waitFor(() => expect(registerDevice).toHaveBeenCalled());
    await screen.findByText(/Dispositivo registrado exitosamente/i);
    await screen.findByDisplayValue("Tomacorriente Patio");

    await waitFor(() => {
      expect(idInput).toHaveValue("");
      expect(nicknameInput).toHaveValue("");
    });
  }, 8000);

  it("muestra error cuando el backend responde fallo", async () => {
    vi.mocked(registerDevice).mockResolvedValue({
      ok: false,
      message: "Error al registrar el dispositivo",
    });

    renderPerfil();
    await screen.findByText(/Registrar Nuevo Tomacorriente/i);

    const idInput = screen.getByPlaceholderText(
      /Ingresa el código del dispositivo/i,
    );
    const nicknameInput = screen.getByPlaceholderText(/Cargador del móvil/i);
    fireEvent.change(idInput, { target: { value: "XYZ" } });
    fireEvent.change(nicknameInput, { target: { value: "Sala" } });

    submitRegistro();

    await waitFor(() => expect(registerDevice).toHaveBeenCalled());
    await screen.findByText(/Error al registrar el dispositivo/i);
  }, 8000);
});

