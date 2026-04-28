import React from "react";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, vi, beforeEach, afterEach } from "vitest";
import Principal from "@/app/page";
import { expect } from "chai";

vi.mock("next/navigation", () => ({
  useRouter: () => ({
    push: vi.fn(),
  }),
}));

// Mock the subscribe hook directly or the fetch request
globalThis.fetch = vi.fn();

describe("Frontend Regression | Flujo de Suscripción a Correo", () => {
  beforeEach(() => {
    vi.mocked(globalThis.fetch).mockReset();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("El flujo de registro de suscripción a correo debe funcionar (Regresión)", async () => {
    // === Arrange ===
    vi.mocked(globalThis.fetch).mockResolvedValue({
      ok: true,
      json: async () => ({ message: "Suscripción exitosa" }),
    } as Response);

    render(<Principal />);

    const emailInput = screen.getByPlaceholderText(/tu correo/i);
    const submitButton = screen.getByRole("button", { name: /unirse a la comunidad/i });

    // === Act ===
    await userEvent.type(emailInput, "newsletter@test.com");
    await userEvent.click(submitButton);

    // === Assert ===
    await waitFor(() => {
      expect(vi.mocked(globalThis.fetch).mock.calls.length).to.be.greaterThan(0);
    });

    const callArgs = vi.mocked(globalThis.fetch).mock.calls[0];
    expect(callArgs[0]).to.include("subscribe"); // Assuming the endpoint has subscribe
  });
});
