import React from "react";
import { describe, it, vi, beforeEach } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import PrincipalPage from "@/app/page";
import { expect } from "chai";

// Mock de next/navigation (Router)
vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: vi.fn(), replace: vi.fn() }),
}));

// Spy sobre nuestro custom hook useSubscribe
import * as useSubscribeHooks from "@/hooks/useSubscribe";

describe("Página: Landing Principal (Subscribe)", () => {
  const mockHandleSubscribe = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();

    vi.spyOn(useSubscribeHooks, "useSubscribe").mockReturnValue({
      email: "",
      setEmail: vi.fn(),
      loading: false,
      message: "",
      handleSubscribe: mockHandleSubscribe,
    });
  });

  it("debería renderizar la página hero con titulo correcto (Render Normal)", () => {
    render(<PrincipalPage />);

    // Al haber múltiples 'EcoEnergy' (header y footer), usamos getAllByText y validamos que al menos uno esté
    const logos = screen.getAllByText("EcoEnergy");
    expect(logos.length).to.be.greaterThan(0);
    expect(screen.queryByText(/Energía Inteligente para un/i)).to.not.equal(
      null,
    );
  });

  it("debería invocar la función handleSubscribe al dar click en el CTA de suscripción (Act / Spy)", () => {
    render(<PrincipalPage />);

    const botonSuscribir = screen.getByRole("button", {
      name: /Unirse a la comunidad/i,
    });
    fireEvent.click(botonSuscribir);

    expect(mockHandleSubscribe.mock.calls.length).to.equal(1);
  });

  it("debería actualizar visualmente la UI si loading está true en el estado del hook (Componente reactivo UI)", () => {
    vi.spyOn(useSubscribeHooks, "useSubscribe").mockReturnValue({
      email: "",
      setEmail: vi.fn(),
      loading: true,
      message: "",
      handleSubscribe: mockHandleSubscribe,
    });

    render(<PrincipalPage />);
    const botonSuscribir = screen.getByRole("button", { name: /Enviando.../i });
    expect(botonSuscribir.hasAttribute("disabled")).to.equal(true);
    expect(screen.queryByText(/Enviando.../i)).to.not.equal(null);
  });

  it("debería mostrar el feedback message que emite el Hook (Feedback UI render)", () => {
    vi.spyOn(useSubscribeHooks, "useSubscribe").mockReturnValue({
      email: "",
      setEmail: vi.fn(),
      loading: false,
      message: "¡Gracias por unirte a la comunidad! 🌱",
      handleSubscribe: mockHandleSubscribe,
    });

    render(<PrincipalPage />);
    expect(
      screen.queryByText("¡Gracias por unirte a la comunidad! 🌱"),
    ).to.not.equal(null);
  });
});
