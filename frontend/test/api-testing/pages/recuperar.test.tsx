import React from "react";
import { describe, it, vi, beforeEach } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import Recuperar from "@/app/recuperar/page";
import * as useRecuperarHook from "@/hooks/useRecuperar";
import { expect } from "chai";

// Mockeamos head para evitar errores de next/head
vi.mock("next/head", () => ({
  default: ({ children }: { children: React.ReactNode }) => <>{children}</>,
}));

describe("Página: Recuperar Contraseña", () => {
  let mockUseRecuperar: any;

  beforeEach(() => {
    vi.clearAllMocks();
    mockUseRecuperar = {
      correo: "",
      setCorreo: vi.fn(),
      nuevacontrasena: "",
      setNuevacontrasena: vi.fn(),
      error: "",
      success: "",
      loading: false,
      handleSubmit: vi.fn((e) => e.preventDefault()),
    };

    // Spy a la implementación del hook
    vi.spyOn(useRecuperarHook, "useRecuperar").mockReturnValue(
      mockUseRecuperar,
    );
  });

  it("debería renderizar la página correctamente sin errores (Render Dummy)", () => {
    render(<Recuperar />);

    // Verifica elementos
    expect(screen.queryByText("RECUPERAR contrasena")).to.not.equal(null);
    expect(screen.queryByPlaceholderText("Tu correo electrónico")).to.not.equal(
      null,
    );
    expect(screen.queryByPlaceholderText("Nueva contrasena")).to.not.equal(
      null,
    );
  });

  it("debería llamar los setters cuando el usuario escribe en inputs (Act)", () => {
    Object.defineProperty(mockUseRecuperar, "correo", { value: "nuevo@mail" });
    Object.defineProperty(mockUseRecuperar, "nuevacontrasena", {
      value: "pass",
    });

    // Aislamos el hook devolviendo callbacks que actuen
    vi.spyOn(useRecuperarHook, "useRecuperar").mockReturnValue({
      ...mockUseRecuperar,
      setCorreo: mockUseRecuperar.setCorreo,
      setNuevacontrasena: mockUseRecuperar.setNuevacontrasena,
    });

    render(<Recuperar />);

    const inputEmail = screen.getByPlaceholderText("Tu correo electrónico");
    fireEvent.change(inputEmail, { target: { value: "a@a.com" } });

    const setCorreoCalls = mockUseRecuperar.setCorreo.mock.calls;
    expect(setCorreoCalls.length).to.equal(1);
    expect(setCorreoCalls[0][0]).to.equal("a@a.com");

    const inputPass = screen.getByPlaceholderText("Nueva contrasena");
    fireEvent.change(inputPass, { target: { value: "123" } });

    const setPassCalls = mockUseRecuperar.setNuevacontrasena.mock.calls;
    expect(setPassCalls.length).to.equal(1);
    expect(setPassCalls[0][0]).to.equal("123");
  });

  it("debería llamar a handleSubmit al enviar el form (Spy sobre Submit)", async () => {
    const { container } = render(<Recuperar />);

    // Llenar campos requeridos para evitar cualquier bloqueo de validación nativa (aunque JSDOM suele ignorarlos, es mejor práctica)
    const inputEmail = screen.getByPlaceholderText("Tu correo electrónico");
    fireEvent.change(inputEmail, { target: { value: "a@a.com" } });
    const inputPass = screen.getByPlaceholderText("Nueva contrasena");
    fireEvent.change(inputPass, { target: { value: "123" } });

    const form = container.querySelector("form");
    if (form) {
      fireEvent.submit(form);
    } else {
      const botonAceptar = screen.getByRole("button", {
        name: /ACTUALIZAR CONTRASENA/i,
      });
      fireEvent.click(botonAceptar);
    }

    expect(mockUseRecuperar.handleSubmit.mock.calls.length).to.equal(1);
  });

  it("debería mostrar mensaje de error si el hook tiene estado error configurado (Assert Render)", () => {
    // Caso de uso: UI reactiva
    vi.spyOn(useRecuperarHook, "useRecuperar").mockReturnValue({
      ...mockUseRecuperar,
      error: "Correo no encontrado",
    });

    render(<Recuperar />);

    expect(screen.queryByText("Correo no encontrado")).to.not.equal(null);
  });

  it("debería mostrar mensaje de success si el hook tiene estado success (Assert Render)", () => {
    vi.spyOn(useRecuperarHook, "useRecuperar").mockReturnValue({
      ...mockUseRecuperar,
      success: "Exito rotundo",
    });

    render(<Recuperar />);
    expect(screen.queryByText("Exito rotundo")).to.not.equal(null);
  });

  it("debería deshabilitar e indicar LOADING visualmente cuando hook loading=true", () => {
    vi.spyOn(useRecuperarHook, "useRecuperar").mockReturnValue({
      ...mockUseRecuperar,
      loading: true,
    });

    render(<Recuperar />);
    const boton = screen.getByRole("button");
    expect(boton.hasAttribute("disabled")).to.equal(true);
    expect(screen.queryByText(/ACTUALIZANDO/i)).to.not.equal(null);
  });
});
