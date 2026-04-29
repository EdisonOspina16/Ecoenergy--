import React from "react";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, it, vi } from "vitest";
import Dashboard from "@/app/dashboard/page";
import { expect } from "chai";

// Aquí configuramos window.location.href
const hrefSpy = vi.fn();
const installLocationMock = () => {
  const loc: any = {
    ...globalThis.location,
    assign: hrefSpy,
    reload: vi.fn(),
    get href() {
      return "";
    },
    set href(val: string) {
      hrefSpy(val);
    },
  };
  Object.defineProperty(globalThis, "location", {
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
      .spyOn(globalThis, "fetch")
      .mockResolvedValueOnce(
        new Response(
          JSON.stringify({
            usuario: { nombre: "Admin", correo: "admin@gmail.com" },
          }),
          { status: 200, headers: { "Content-Type": "application/json" } },
        ),
      )
      .mockResolvedValueOnce(
        new Response(JSON.stringify({ success: true }), {
          status: 200,
          headers: { "Content-Type": "application/json" },
        }),
      );

    render(<Dashboard />);

    await waitFor(() => screen.getByText(/hola, admin/i));
    await userEvent.click(
      screen.getByRole("button", { name: /cerrar sesión/i }),
    );

    await waitFor(() => {
      const hrefCalls = hrefSpy.mock.calls;
      expect(hrefCalls.length).to.equal(1);
      expect(hrefCalls[0][0]).to.equal("/login");
    });
    expect(fetchMock.mock.calls.length).to.equal(2);
  });

  it("CP-LOG-002 Intentar acceder al Dashboard sin sesión (debería pedir login)", async () => {
    const fetchMock = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValueOnce(new Response("", { status: 401 }));

    render(<Dashboard />);

    await waitFor(() => screen.getByText(/Debes iniciar sesión/i));
    expect(fetchMock.mock.calls.length).to.equal(1);
    expect(screen.queryByRole("button", { name: /cerrar sesión/i })).to.equal(
      null,
    );
  });

  it("CP-LOG-003 Logout idempotente (múltiples clics seguidos)", async () => {
    const fetchMock = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValueOnce(
        new Response(
          JSON.stringify({
            usuario: { nombre: "Admin", correo: "admin@gmail.com" },
          }),
          { status: 200, headers: { "Content-Type": "application/json" } },
        ),
      )
      .mockResolvedValueOnce(
        new Response(JSON.stringify({ success: true }), { status: 200 }),
      )
      .mockResolvedValueOnce(
        new Response(JSON.stringify({ success: true }), { status: 200 }),
      );

    render(<Dashboard />);

    await waitFor(() => screen.getByText(/hola, admin/i));
    const btn = screen.getByRole("button", { name: /cerrar sesión/i });

    await userEvent.click(btn);
    await userEvent.click(btn);

    // Debe haber llamado a 1 GET y a 2 POST
    expect(fetchMock.mock.calls.length).to.equal(3);
    await waitFor(() => {
      expect(hrefSpy.mock.calls.length).to.be.greaterThan(0);
    });
  });

  it("CP-LOG-004 Botón logout sin sesión activa (no debería mostrarse)", async () => {
    const fetchMock = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValueOnce(new Response("", { status: 401 }));

    render(<Dashboard />);

    await waitFor(() => screen.getByText(/Debes iniciar sesión/i));
    expect(screen.queryByRole("button", { name: /cerrar sesión/i })).to.equal(
      null,
    );
    expect(fetchMock.mock.calls.length).to.equal(1);
  });

  it("CP-LOG-005 No debe mostrarse dashboard tras cerrar y 'cerrar navegador' (nuevo render limpio)", async () => {
    const fetchMock = vi
      .spyOn(globalThis, "fetch")
      // Render inicial OK
      .mockResolvedValueOnce(
        new Response(
          JSON.stringify({
            usuario: { nombre: "Admin", correo: "admin@gmail.com" },
          }),
          { status: 200, headers: { "Content-Type": "application/json" } },
        ),
      )
      // Logout
      .mockResolvedValueOnce(
        new Response(JSON.stringify({ success: true }), { status: 200 }),
      )
      // "Nuevo navegador"/nueva sesión => 401 directo
      .mockResolvedValueOnce(new Response("", { status: 401 }));

    const { unmount } = render(<Dashboard />);
    await waitFor(() => screen.getByText(/hola, admin/i));

    await userEvent.click(
      screen.getByRole("button", { name: /cerrar sesión/i }),
    );
    await waitFor(() => {
      expect(hrefSpy.mock.calls.length).to.be.greaterThan(0);
    });

    // Simula abrir nueva pestaña/navegador: unmount + render fresco
    unmount();
    render(<Dashboard />);
    await waitFor(() => screen.getByText(/Debes iniciar sesión/i));
    expect(fetchMock.mock.calls.length).to.equal(3);
  });

  it("CP-LOG-006 Registra error en consola si el logout falla", async () => {
    const fetchMock = vi
      .spyOn(globalThis, "fetch")
      // Perfil OK para mostrar el botón
      .mockResolvedValueOnce(
        new Response(
          JSON.stringify({
            usuario: { nombre: "Admin", correo: "admin@gmail.com" },
          }),
          { status: 200, headers: { "Content-Type": "application/json" } },
        ),
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
      const errorCalls = consoleErrorSpy.mock.calls;
      expect(errorCalls.length).to.equal(1);
      expect(errorCalls[0][0]).to.equal("Error al cerrar sesión:");
      expect(errorCalls[0][1]).to.be.instanceOf(Error);
    });

    expect(hrefSpy.mock.calls.length).to.equal(0);
    expect(fetchMock.mock.calls.length).to.equal(2);
  });
});
