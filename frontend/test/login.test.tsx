import React from "react";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import Login from "../app/login/page";

const pushMock = (globalThis as any).__routerPush as ReturnType<typeof vi.fn>;

const mockFetch = (status: number, body: any) => {
  return vi.spyOn(global, "fetch").mockResolvedValue(
    new Response(JSON.stringify(body), {
      status,
      headers: { "Content-Type": "application/json" },
    }) as any,
  );
};

describe("Login | casos de formulario", () => {
  beforeEach(() => {
    pushMock?.mockReset?.();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("Email existente y contraseña correcta", async () => {
    mockFetch(200, {
      success: true,
      redirect: "/home",
      usuario: { correo: "admin@gmail.com" },
    });

    render(<Login />);

    await userEvent.type(
      screen.getByPlaceholderText("Tu correo electrónico"),
      "admin@gmail.com",
    );
    await userEvent.type(screen.getByPlaceholderText("Tu contraseña"), "admin");
    await userEvent.click(screen.getByRole("button", { name: /ingresar/i }));

    await waitFor(() => expect(pushMock).toHaveBeenCalledWith("/home"));
  });

  it("Ambos campos vacíos", async () => {
    const fetchSpy = vi.spyOn(global, "fetch");

    render(<Login />);

    await userEvent.click(screen.getByRole("button", { name: /ingresar/i }));

    // Validación nativa evita submit: no se debe llamar a fetch
    expect(fetchSpy).not.toHaveBeenCalled();
  });

  it("Email correcto y sin contraseña", async () => {
    const fetchSpy = vi.spyOn(global, "fetch");

    render(<Login />);

    await userEvent.type(
      screen.getByPlaceholderText("Tu correo electrónico"),
      "admin@gmail.com",
    );
    await userEvent.click(screen.getByRole("button", { name: /ingresar/i }));

    expect(fetchSpy).not.toHaveBeenCalled();
  });

  it("Email vacío y contraseña válida", async () => {
    const fetchSpy = vi.spyOn(global, "fetch");

    render(<Login />);

    await userEvent.type(screen.getByPlaceholderText("Tu contraseña"), "admin");
    await userEvent.click(screen.getByRole("button", { name: /ingresar/i }));

    expect(fetchSpy).not.toHaveBeenCalled();
  });

  it("Email correcto y contraseña incorrecta", async () => {
    mockFetch(401, { error: "Credenciales inválidas" });

    render(<Login />);

    await userEvent.type(
      screen.getByPlaceholderText("Tu correo electrónico"),
      "admin@gmail.com",
    );
    await userEvent.type(
      screen.getByPlaceholderText("Tu contraseña"),
      "ayayai",
    );
    await userEvent.click(screen.getByRole("button", { name: /ingresar/i }));

    await waitFor(() => screen.getByText("Credenciales inválidas"));
  });

  it("Email sin texto después del arroba", async () => {
    const fetchSpy = vi.spyOn(global, "fetch");

    render(<Login />);

    await userEvent.type(
      screen.getByPlaceholderText("Tu correo electrónico"),
      "admin@",
    );
    await userEvent.type(screen.getByPlaceholderText("Tu contraseña"), "admin");
    await userEvent.click(screen.getByRole("button", { name: /ingresar/i }));

    expect(fetchSpy).not.toHaveBeenCalled();
  });

  it("Email sin @", async () => {
    const fetchSpy = vi.spyOn(global, "fetch");

    render(<Login />);

    await userEvent.type(
      screen.getByPlaceholderText("Tu correo electrónico"),
      "admin",
    );
    await userEvent.type(screen.getByPlaceholderText("Tu contraseña"), "admin");
    await userEvent.click(screen.getByRole("button", { name: /ingresar/i }));

    expect(fetchSpy).not.toHaveBeenCalled();
  });

  it("Email válido pero sin cuenta y contraseña válida", async () => {
    mockFetch(401, { error: "Credenciales inválidas" });

    render(<Login />);

    await userEvent.type(
      screen.getByPlaceholderText("Tu correo electrónico"),
      "tomi123@gmail.com",
    );
    await userEvent.type(screen.getByPlaceholderText("Tu contraseña"), "admin");
    await userEvent.click(screen.getByRole("button", { name: /ingresar/i }));

    await waitFor(() => screen.getByText("Credenciales inválidas"));
  });
});
