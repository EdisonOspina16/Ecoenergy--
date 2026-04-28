import React from "react";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, vi, beforeEach, afterEach } from "vitest";
import Login from "@/app/login/page";
import { loginRequest } from "@/lib/api/auth";
import { expect } from "chai";

vi.mock("@/lib/api/auth", () => ({
  loginRequest: vi.fn(),
}));

const pushMock = (globalThis as any).__routerPush as ReturnType<typeof vi.fn>;

describe("Frontend Regression | Flujo completo de Login", () => {
  beforeEach(() => {
    pushMock?.mockReset?.();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("El flujo principal de login debe seguir funcionando correctamente y no romperse por cambios (Regresión)", async () => {
    // === Arrange ===
    // Simulamos un comportamiento de servidor exitoso
    vi.mocked(loginRequest).mockResolvedValue({
      ok: true,
      redirect: "/home",
    });

    render(<Login />);

    const emailInput = screen.getByPlaceholderText("Tu correo electrónico");
    const passInput = screen.getByPlaceholderText("Tu contrasena");
    const submitButton = screen.getByRole("button", { name: /ingresar/i });

    // === Act ===
    await userEvent.type(emailInput, "regression_user@test.com");
    await userEvent.type(passInput, "SecurePass123!");
    await userEvent.click(submitButton);

    // === Assert ===
    // Comprobamos que el Request se formó de manera idéntica a como el servidor lo espera
    await waitFor(() => {
      expect(vi.mocked(loginRequest).mock.calls.length).to.be.at.least(1);
    });

    const callArgs = vi.mocked(loginRequest).mock.calls[0][0];
    expect(callArgs).to.deep.equal({
      correo: "regression_user@test.com",
      contrasena: "SecurePass123!",
    });

    // Comprobamos que se llamó al push de router para redirigir (flujo feliz intacto)
    await waitFor(() => {
      // @ts-expect-error router push is mocked globally in setupTests
      const routerPushCalls = globalThis.__routerPush.mock.calls;
      expect(routerPushCalls.length).to.equal(1);
      expect(routerPushCalls[0][0]).to.equal("/home");
    });
  });
});
