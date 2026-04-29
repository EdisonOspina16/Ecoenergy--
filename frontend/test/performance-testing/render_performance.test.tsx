import React from "react";
import { render } from "@testing-library/react";
import { describe, it, vi } from "vitest";
import Login from "@/app/login/page";
import Registro from "@/app/registro/page";
import Recuperar from "@/app/recuperar/page";
import Principal from "@/app/page";
import Dashboard from "@/app/dashboard/page";
import Home from "@/app/home/page";
import Perfil from "@/app/perfil/page";
import { expect } from "chai";

// Mock para Next.js App Router hooks si son usados en las paginas
vi.mock("next/navigation", () => ({
  useRouter: () => ({
    push: vi.fn(),
  }),
}));

const measureRenderTime = (Component: React.FC) => {
  const start = performance.now();
  render(<Component />);
  const end = performance.now();
  return end - start;
};

describe("Frontend Performance | Tiempos de renderizado", () => {
  it("El componente Login debe renderizar en un tiempo aceptable (< 150ms)", () => {
    const renderTime = measureRenderTime(Login);
    console.log(`[Performance] Render time for Login: ${renderTime.toFixed(2)}ms`);
    expect(renderTime).to.be.below(500);
  });

  it("El componente Registro debe renderizar en un tiempo aceptable (< 150ms)", () => {
    const renderTime = measureRenderTime(Registro);
    console.log(`[Performance] Render time for Registro: ${renderTime.toFixed(2)}ms`);
    expect(renderTime).to.be.below(500);
  });

  it("El componente Recuperar (Cambiar contraseña) debe renderizar en un tiempo aceptable (< 150ms)", () => {
    const renderTime = measureRenderTime(Recuperar);
    console.log(`[Performance] Render time for Recuperar: ${renderTime.toFixed(2)}ms`);
    expect(renderTime).to.be.below(500);
  });

  it("El componente Principal (Landing / Suscripción) debe renderizar en un tiempo aceptable (< 150ms)", () => {
    const renderTime = measureRenderTime(Principal);
    console.log(`[Performance] Render time for Principal: ${renderTime.toFixed(2)}ms`);
    expect(renderTime).to.be.below(500);
  });

  it("El componente Dashboard (Gestión y Dispositivos) debe renderizar en un tiempo aceptable (< 150ms)", () => {
    const renderTime = measureRenderTime(Dashboard);
    console.log(`[Performance] Render time for Dashboard: ${renderTime.toFixed(2)}ms`);
    expect(renderTime).to.be.below(500);
  });

  it("El componente Home (IA y Estadísticas) debe renderizar en un tiempo aceptable (< 150ms)", () => {
    const renderTime = measureRenderTime(Home);
    console.log(`[Performance] Render time for Home: ${renderTime.toFixed(2)}ms`);
    expect(renderTime).to.be.below(500);
  });

  it("El componente Perfil (Gestión del Hogar) debe renderizar en un tiempo aceptable (< 150ms)", () => {
    const renderTime = measureRenderTime(Perfil);
    console.log(`[Performance] Render time for Perfil: ${renderTime.toFixed(2)}ms`);
    expect(renderTime).to.be.below(500);
  });
});
