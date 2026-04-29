import React from "react";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, vi, beforeEach, afterEach } from "vitest";
import Recuperar from "@/app/recuperar/page";
import { expect } from "chai";

vi.mock("next/navigation", () => ({
  useRouter: () => ({
    push: vi.fn(),
  }),
}));

describe("Frontend Regression | Flujo de Recuperar Contraseña", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("El flujo para recuperar/cambiar contraseña debe mantener sus elementos (Regresión)", async () => {
    // === Arrange ===
    const { container } = render(<Recuperar />);
    
    expect(container.innerHTML).to.not.be.empty;

    const emailInput = screen.queryByPlaceholderText(/correo/i) || screen.queryByRole("textbox");
    const submitButton = screen.queryByRole("button", { name: /recuperar/i }) || screen.queryByRole("button");

    // === Act ===
    if (emailInput && submitButton) {
      await userEvent.type(emailInput, "test@test.com");
      await userEvent.click(submitButton);
    }

    // === Assert ===
    // Aseguramos que la interfaz renderice correctamente
    expect(emailInput).to.exist;
    expect(submitButton).to.exist;
  });
});
