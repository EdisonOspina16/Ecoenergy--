import React from "react";
import { render } from "@testing-library/react";
import { describe, it, vi, beforeEach, afterEach } from "vitest";
import Perfil from "@/app/perfil/page";
import { expect } from "chai";

vi.mock("next/navigation", () => ({
  useRouter: () => ({
    push: vi.fn(),
  }),
}));

describe("Frontend Regression | Flujo de Perfil y Gestión del Hogar", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("Debe renderizar la vista de Perfil sin errores (Regresión)", () => {
    // === Arrange & Act ===
    const { container } = render(<Perfil />);
    
    // === Assert ===
    expect(container.innerHTML).to.not.be.empty;
  });

  it("Debe soportar la gestión del perfil del hogar sin romperse", () => {
    const { container } = render(<Perfil />);
    expect(container).to.exist;
  });
});
