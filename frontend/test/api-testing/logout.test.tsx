import React from "react";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import Dashboard from "@/app/dashboard/page";

// Aquí configuramos window.location.href
const hrefSpy = vi.fn();
const installLocationMock = () => {
  const loc: any = {
    ...window.location,
    assign: hrefSpy,
    reload: vi.fn(),
    get href() {
      return "";
    },
    set href(val: string) {
      hrefSpy(val);
    },
  };
  Object.defineProperty(window, "location", {
    value: loc,
    writable: true,
  });
};

describe("Dashboard | logout", () => {
  beforeEach(() => {
    hrefSpy.mockReset();
    installLocationMock();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("CP-LOG-001 Cerrar sesión correctamente desde el botón", async () => {
    const fetchMock = vi
      .spyOn(global, "fetch")
      .mockResolvedValueOnce(
        new Response(
          JSON.stringify({
            usuario: { nombre: "Admin", correo: "admin@gmail.com" },
          }),
          { status: 200, headers: { "Content-Type": "application/json" } },
        ) as any,
      )
      .mockResolvedValueOnce(
        new Response(JSON.stringify({ success: true }), {
          status: 200,
          headers: { "Content-Type": "application/json" },
        }) as any,
      );

    render(<Dashboard />);

    await waitFor(() => screen.getByText(/hola, admin/i));
    await userEvent.click(
      screen.getByRole("button", { name: /cerrar sesión/i }),
    );

    await waitFor(() => expect(hrefSpy).toHaveBeenCalledWith("/login"));
    expect(fetchMock).toHaveBeenCalledTimes(2);
  });

  it("CP-LOG-002 Intentar acceder al Dashboard sin sesión (debería pedir login)", async () => {
    const fetchMock = vi
      .spyOn(global, "fetch")
      .mockResolvedValueOnce(new Response("", { status: 401 })) as any;

    render(<Dashboard />);

    await waitFor(() => screen.getByText(/Debes iniciar sesión/i));
    expect(fetchMock).toHaveBeenCalledTimes(1);
    expect(screen.queryByRole("button", { name: /cerrar sesión/i })).toBeNull();
  });

  it("CP-LOG-003 Logout idempotente (múltiples clics seguidos)", async () => {
    const fetchMock = vi
      .spyOn(global, "fetch")
      .mockResolvedValueOnce(
        new Response(
          JSON.stringify({
            usuario: { nombre: "Admin", correo: "admin@gmail.com" },
          }),
          { status: 200, headers: { "Content-Type": "application/json" } },
        ) as any,
      )
      .mockResolvedValueOnce(
        new Response(JSON.stringify({ success: true }), { status: 200 }) as any,
      )
      .mockResolvedValueOnce(
        new Response(JSON.stringify({ success: true }), { status: 200 }) as any,
      );

    render(<Dashboard />);

    await waitFor(() => screen.getByText(/hola, admin/i));
    const btn = screen.getByRole("button", { name: /cerrar sesión/i });

    await userEvent.click(btn);
    await userEvent.click(btn);

    // Debe haber llamado a 1 GET y a 2 POST
    expect(fetchMock).toHaveBeenCalledTimes(3);
    await waitFor(() => expect(hrefSpy).toHaveBeenCalled());
  });

  it("CP-LOG-004 Botón logout sin sesión activa (no debería mostrarse)", async () => {
    const fetchMock = vi
      .spyOn(global, "fetch")
      .mockResolvedValueOnce(new Response("", { status: 401 }) as any);

    render(<Dashboard />);

    await waitFor(() => screen.getByText(/Debes iniciar sesión/i));
    expect(screen.queryByRole("button", { name: /cerrar sesión/i })).toBeNull();
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });

  it("CP-LOG-005 No debe mostrarse dashboard tras cerrar y 'cerrar navegador' (nuevo render limpio)", async () => {
    const fetchMock = vi
      .spyOn(global, "fetch")
      // Render inicial OK
      .mockResolvedValueOnce(
        new Response(
          JSON.stringify({
            usuario: { nombre: "Admin", correo: "admin@gmail.com" },
          }),
          { status: 200, headers: { "Content-Type": "application/json" } },
        ) as any,
      )
      // Logout
      .mockResolvedValueOnce(
        new Response(JSON.stringify({ success: true }), { status: 200 }) as any,
      )
      // "Nuevo navegador"/nueva sesión => 401 directo
      .mockResolvedValueOnce(new Response("", { status: 401 }) as any);

    const { unmount } = render(<Dashboard />);
    await waitFor(() => screen.getByText(/hola, admin/i));

    await userEvent.click(
      screen.getByRole("button", { name: /cerrar sesión/i }),
    );
    await waitFor(() => expect(hrefSpy).toHaveBeenCalled());

    // Simula abrir nueva pestaña/navegador: unmount + render fresco
    unmount();
    render(<Dashboard />);
    await waitFor(() => screen.getByText(/Debes iniciar sesión/i));
    expect(fetchMock).toHaveBeenCalledTimes(3);
  });

  it("CP-LOG-006 Registra error en consola si el logout falla", async () => {
    const fetchMock = vi
      .spyOn(global, "fetch")
      // Perfil OK para mostrar el botón
      .mockResolvedValueOnce(
        new Response(
          JSON.stringify({
            usuario: { nombre: "Admin", correo: "admin@gmail.com" },
          }),
          { status: 200, headers: { "Content-Type": "application/json" } },
        ) as any,
      )
      // Logout falla por error de red
      .mockRejectedValueOnce(new Error("Network down"));

    const consoleErrorSpy = vi
      .spyOn(console, "error")
      .mockImplementation(() => {});

    render(<Dashboard />);
    await waitFor(() => screen.getByText(/hola, admin/i));

    await userEvent.click(
      screen.getByRole("button", { name: /cerrar sesión/i }),
    );

    await waitFor(() => {
      expect(consoleErrorSpy).toHaveBeenCalledWith(
        "Error al cerrar sesión:",
        expect.any(Error),
      );
    });

    expect(hrefSpy).not.toHaveBeenCalled();
    expect(fetchMock).toHaveBeenCalledTimes(2);
  });
});

