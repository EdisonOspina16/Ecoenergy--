import React from "react";
import { render, screen, waitFor, fireEvent } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import Login from "../src/app/login/page";
import { loginRequest } from "../src/lib/api/auth";

vi.mock("../src/lib/api/auth", () => ({
  loginRequest: vi.fn(),
}));

const pushMock = (globalThis as any).__routerPush as ReturnType<typeof vi.fn>;

describe("Login | casos de formulario", () => {
  beforeEach(() => {
    pushMock?.mockReset?.();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("Ambos campos vacíos", async () => {
    const fetchSpy = vi.spyOn(global, "fetch");
    vi.mocked(loginRequest).mockResolvedValue({
      ok: false,
      message: "",
    });

    render(<Login />);

    await userEvent.click(screen.getByRole("button", { name: /ingresar/i }));

    // Validación evita submit: no se debe llamar a fetch ni loginRequest
    expect(fetchSpy).not.toHaveBeenCalled();
    expect(loginRequest).not.toHaveBeenCalled();
  });

  it("Email correcto y sin contrasena", async () => {
    const fetchSpy = vi.spyOn(global, "fetch");
    vi.mocked(loginRequest).mockResolvedValue({
      ok: false,
      message: "",
    });

    const { container } = render(<Login />);

    await userEvent.type(
      screen.getByPlaceholderText("Tu correo electrónico"),
      "admin@gmail.com",
    );
    const form = container.querySelector("form")!;
    fireEvent.submit(form);

    await screen.findByText(/Ingresa correo y contraseña/i);
    expect(fetchSpy).not.toHaveBeenCalled();
    expect(loginRequest).not.toHaveBeenCalled();
  });

  it("Email vacío y contrasena válida", async () => {
    const fetchSpy = vi.spyOn(global, "fetch");
    vi.mocked(loginRequest).mockResolvedValue({
      ok: false,
      message: "",
    });

    render(<Login />);

    await userEvent.type(screen.getByPlaceholderText("Tu contrasena"), "admin");
    await userEvent.click(screen.getByRole("button", { name: /ingresar/i }));

    expect(fetchSpy).not.toHaveBeenCalled();
    expect(loginRequest).not.toHaveBeenCalled();
  });

  it("Email correcto y contrasena incorrecta", async () => {
    vi.mocked(loginRequest).mockResolvedValue({
      ok: false,
      message: "Credenciales inválidas",
    });

    render(<Login />);

    await userEvent.type(
      screen.getByPlaceholderText("Tu correo electrónico"),
      "admin@gmail.com",
    );
    await userEvent.type(
      screen.getByPlaceholderText("Tu contrasena"),
      "ayayai",
    );
    await userEvent.click(screen.getByRole("button", { name: /ingresar/i }));

    await waitFor(() => screen.getByText("Credenciales inválidas"));
    expect(loginRequest).toHaveBeenCalledWith({
      correo: "admin@gmail.com",
      contrasena: "ayayai",
    });
  });

  it("Email sin texto después del arroba", async () => {
    const fetchSpy = vi.spyOn(global, "fetch");
    vi.mocked(loginRequest).mockResolvedValue({ ok: false, message: "" });

    render(<Login />);

    await userEvent.type(
      screen.getByPlaceholderText("Tu correo electrónico"),
      "admin@",
    );
    await userEvent.type(screen.getByPlaceholderText("Tu contrasena"), "admin");
    await userEvent.click(screen.getByRole("button", { name: /ingresar/i }));

    expect(fetchSpy).not.toHaveBeenCalled();
    expect(loginRequest).not.toHaveBeenCalled();
  });

  it("Email sin @", async () => {
    const fetchSpy = vi.spyOn(global, "fetch");
    vi.mocked(loginRequest).mockResolvedValue({ ok: false, message: "" });

    render(<Login />);

    await userEvent.type(
      screen.getByPlaceholderText("Tu correo electrónico"),
      "admin",
    );
    await userEvent.type(screen.getByPlaceholderText("Tu contrasena"), "admin");
    await userEvent.click(screen.getByRole("button", { name: /ingresar/i }));

    expect(fetchSpy).not.toHaveBeenCalled();
    expect(loginRequest).not.toHaveBeenCalled();
  });

  it("Email válido pero sin cuenta y contrasena válida", async () => {
    vi.mocked(loginRequest).mockResolvedValue({
      ok: false,
      message: "Credenciales inválidas",
    });

    render(<Login />);

    await userEvent.type(
      screen.getByPlaceholderText("Tu correo electrónico"),
      "tomi123@gmail.com",
    );
    await userEvent.type(screen.getByPlaceholderText("Tu contrasena"), "admin");
    await userEvent.click(screen.getByRole("button", { name: /ingresar/i }));

    await waitFor(() => screen.getByText("Credenciales inválidas"));
    expect(loginRequest).toHaveBeenCalledWith({
      correo: "tomi123@gmail.com",
      contrasena: "admin",
    });
  });
});
