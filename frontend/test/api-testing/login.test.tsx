import React from "react";
import { render, screen, waitFor, fireEvent } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, it, vi } from "vitest";
import Login from "@/app/login/page";
import { loginRequest } from "@/lib/api/auth";
import { expect } from "chai";

vi.mock("@/lib/api/auth", () => ({
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
    const fetchSpy = vi.spyOn(globalThis, "fetch");
    vi.mocked(loginRequest).mockResolvedValue({
      ok: false,
      message: "",
    });

    render(<Login />);

    await userEvent.click(screen.getByRole("button", { name: /ingresar/i }));

    // Validación evita submit: no se debe llamar a fetch ni loginRequest
    expect(fetchSpy.mock.calls.length).to.equal(0);
    expect(vi.mocked(loginRequest).mock.calls.length).to.equal(0);
  });

  it("Email correcto y sin contrasena", async () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch");
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
    expect(fetchSpy.mock.calls.length).to.equal(0);
    expect(vi.mocked(loginRequest).mock.calls.length).to.equal(0);
  });

  it("Email vacío y contrasena válida", async () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch");
    vi.mocked(loginRequest).mockResolvedValue({
      ok: false,
      message: "",
    });

    render(<Login />);

    await userEvent.type(screen.getByPlaceholderText("Tu contrasena"), "admin");
    await userEvent.click(screen.getByRole("button", { name: /ingresar/i }));

    expect(fetchSpy.mock.calls.length).to.equal(0);
    expect(vi.mocked(loginRequest).mock.calls.length).to.equal(0);
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
    const loginCalls = vi.mocked(loginRequest).mock.calls;
    expect(loginCalls.length).to.equal(1);
    expect(loginCalls[0][0]).to.deep.equal({
      correo: "admin@gmail.com",
      contrasena: "ayayai",
    });
  });

  it("Email sin texto después del arroba", async () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch");
    vi.mocked(loginRequest).mockResolvedValue({ ok: false, message: "" });

    render(<Login />);

    await userEvent.type(
      screen.getByPlaceholderText("Tu correo electrónico"),
      "admin@",
    );
    await userEvent.type(screen.getByPlaceholderText("Tu contrasena"), "admin");
    await userEvent.click(screen.getByRole("button", { name: /ingresar/i }));

    expect(fetchSpy.mock.calls.length).to.equal(0);
    expect(vi.mocked(loginRequest).mock.calls.length).to.equal(0);
  });

  it("Email sin @", async () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch");
    vi.mocked(loginRequest).mockResolvedValue({ ok: false, message: "" });

    render(<Login />);

    await userEvent.type(
      screen.getByPlaceholderText("Tu correo electrónico"),
      "admin",
    );
    await userEvent.type(screen.getByPlaceholderText("Tu contrasena"), "admin");
    await userEvent.click(screen.getByRole("button", { name: /ingresar/i }));

    expect(fetchSpy.mock.calls.length).to.equal(0);
    expect(vi.mocked(loginRequest).mock.calls.length).to.equal(0);
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
    const loginCalls = vi.mocked(loginRequest).mock.calls;
    expect(loginCalls.length).to.equal(1);
    expect(loginCalls[0][0]).to.deep.equal({
      correo: "tomi123@gmail.com",
      contrasena: "admin",
    });
  });

  it("Debería iniciar sesión y redirigir con éxito (Camino Normal)", async () => {
    // === Arrange ===
    vi.mocked(loginRequest).mockResolvedValue({
      ok: true,
      redirect: "/home",
    });

    render(<Login />);

    await userEvent.type(
      screen.getByPlaceholderText("Tu correo electrónico"),
      "admin@gmail.com",
    );
    await userEvent.type(screen.getByPlaceholderText("Tu contrasena"), "admin");

    // === Act ===
    await userEvent.click(screen.getByRole("button", { name: /ingresar/i }));

    // === Assert ===
    await waitFor(() => {
      // @ts-expect-error router push is mocked in setupTests
      const routerPushCalls = globalThis.__routerPush.mock.calls;
      expect(routerPushCalls.length).to.equal(1);
      expect(routerPushCalls[0][0]).to.equal("/home");
    });
  });
});
