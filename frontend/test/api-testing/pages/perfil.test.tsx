import React from "react";
import { describe, it, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import ProfilePage from "@/app/perfil/page";
import { expect } from "chai";

// Mocks
import * as useProfileHooks from "@/hooks/useProfileSubmit";
import * as useDeviceRegHooks from "@/hooks/useDeviceRegistration";
import * as profileApi from "@/lib/api/profile";

describe("Página: Profile / Perfil", () => {
  const mockSubmitProfile = vi.fn();
  const mockDeviceRegistroSubmit = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();

    vi.spyOn(profileApi, "fetchPerfil").mockResolvedValue({
      ok: true,
      data: {
        success: true,
        hogar: { direccion: "Av test", nombre_hogar: "MyHome" },
        dispositivos: [],
      },
      status: 200,
    });

    vi.spyOn(useProfileHooks, "useProfileSubmit").mockReturnValue({
      profileSaving: false,
      submitProfile: mockSubmitProfile,
    });

    vi.spyOn(useDeviceRegHooks, "useDeviceRegistration").mockReturnValue({
      deviceId: "",
      setDeviceId: vi.fn(),
      nickname: "",
      setNickname: vi.fn(),
      submitting: false,
      submit: mockDeviceRegistroSubmit,
    });

    Object.defineProperty(globalThis, "location", {
      value: { href: "" },
      writable: true,
    });
  });

  it("debería renderizar la página inicialmente en estado cargando y luego mostrar perfil (Camino Normal Render)", async () => {
    render(<ProfilePage />);

    // Verifica que el fetch API fue llamado al montar el componente
    expect(vi.mocked(profileApi.fetchPerfil).mock.calls.length).to.equal(1);

    // El texto "Cargando..." aparece hasta que se resuelva la promesa
    await waitFor(() => {
      expect(screen.queryByText("Cargando...")).to.equal(null);
    });

    // Se asume que renderizó bien y los effectos actualizaron state:
    expect(screen.queryByText("Perfil del Hogar")).to.not.equal(null);
  });

  it("debería ejecutar el envio del perfil en form handleSubmit (Interacción Eventos)", async () => {
    render(<ProfilePage />);
    await waitFor(() => {
      expect(screen.queryByText("Cargando...")).to.equal(null);
    });

    // Encontrar inputs
    const addressInput = screen.getByPlaceholderText(/Calle 50/i);
    fireEvent.change(addressInput, { target: { value: "Nueva Calle 123" } });

    const btnSubmit = screen.getByRole("button", { name: /Guardar Cambios/i });
    fireEvent.click(btnSubmit);

    // Debe llamar al hook con la nueva address
    expect(mockSubmitProfile.mock.calls.length).to.equal(1);
  });

  it("debería gestionar la UI de device registry llamando el hook asignado (Integración Sub-Forms)", async () => {
    render(<ProfilePage />);
    await waitFor(() => {
      expect(screen.queryByText("Cargando...")).to.equal(null);
    });

    const btnDevice = screen.getByRole("button", {
      name: /Registrar Tomacorriente/i,
    });
    // Buscamos el form que contiene el botón y disparamos submit
    const form = btnDevice.closest("form");
    if (form) {
      fireEvent.submit(form);
    } else {
      fireEvent.click(btnDevice);
    }

    expect(mockDeviceRegistroSubmit.mock.calls.length).to.equal(1);
  });
});
