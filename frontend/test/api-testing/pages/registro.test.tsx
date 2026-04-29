import React from "react";
import { describe, it, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import Registro from "@/app/registro/page";
import * as useRegistroHook from "@/hooks/useRegistro";
import { expect } from "chai";

vi.mock("next/head", () => ({
  default: ({ children }: { children: React.ReactNode }) => <>{children}</>,
}));

vi.mock("@/hooks/useRegistro", () => ({
  registrarUsuario: vi.fn(),
}));

describe("Página: Registro de Usuario", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("debería renderizar el formulario de registro correctamente", () => {
    render(<Registro />);

    expect(screen.queryByText("REGISTRO")).to.not.equal(null);
  });

  it("debería llamar a registrarUsuario con los datos del form al hacer submit", async () => {
    const mockRegistrarFn = vi.mocked(useRegistroHook.registrarUsuario);
    render(<Registro />);

    fireEvent.change(screen.getByPlaceholderText("Tu nombre"), {
      target: { value: "Juan" },
    });
    fireEvent.change(screen.getByPlaceholderText("Tus apellidos"), {
      target: { value: "Perez" },
    });
    fireEvent.change(screen.getByPlaceholderText("Tu correo electrónico"), {
      target: { value: "juan@mail.com" },
    });
    fireEvent.change(screen.getByPlaceholderText("Tu contrasena"), {
      target: { value: "123456" },
    });

    const boton = screen.getByRole("button", { name: /COMPLETAR REGISTRO/i });
    fireEvent.click(boton);

    const calls = mockRegistrarFn.mock.calls;
    expect(calls.length).to.equal(1);
    expect(calls[0][0]).to.equal("Juan");
    expect(calls[0][1]).to.equal("Perez");
    expect(calls[0][2]).to.equal("juan@mail.com");
    expect(calls[0][3]).to.equal("123456");
    expect(calls[0][4]).to.not.equal(undefined);
  });

  it("debería mostrar estado de cargando mientras se registra", async () => {
    const mockRegistrarFn = vi.mocked(useRegistroHook.registrarUsuario);
    mockRegistrarFn.mockImplementation((n, a, c, p, setters) => {
      setters.setLoading(true);
      return new Promise(() => {});
    });

    const { container } = render(<Registro />);

    const form = container.querySelector("form");
    if (form) {
      fireEvent.submit(form);
    } else {
      const boton = screen.getByRole("button", { name: /COMPLETAR REGISTRO/i });
      fireEvent.click(boton);
    }

    // Verificamos al menos que el botón se deshabilita, lo cual confirma que el estado cambió
    await waitFor(() => {
      const submitBtn = screen.getByRole("button");
      expect(submitBtn.hasAttribute("disabled")).to.equal(true);
    });
  });
});
