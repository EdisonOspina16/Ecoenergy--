import React from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it } from "vitest";
import Login from "@/app/login/page";
import { expect } from "chai";

describe("Frontend Security | Inyección y protección de datos", () => {
  it("Los inputs de correo no deben interpretar scripts como HTML (Protección XSS básica)", async () => {
    render(<Login />);

    const xssPayload = "<script>alert('xss')</script>@gmail.com";
    const emailInput = screen.getByPlaceholderText("Tu correo electrónico") as HTMLInputElement;
    
    await userEvent.type(emailInput, xssPayload);
    
    // Verificamos que React mantenga el texto literal como valor y no lo inyecte en el DOM
    expect(emailInput.value).to.equal(xssPayload);
  });

  it("El campo de contraseña debe mantener el tipo 'password' para no exponer texto en pantalla", () => {
    render(<Login />);

    const passwordInput = screen.getByPlaceholderText("Tu contrasena") as HTMLInputElement;
    
    expect(passwordInput.type).to.equal("password");
  });
});
