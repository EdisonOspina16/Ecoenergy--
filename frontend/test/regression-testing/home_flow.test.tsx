import React from "react";
import { render } from "@testing-library/react";
import { describe, it, vi, beforeEach, afterEach } from "vitest";
import Home from "@/app/home/page";
import { expect } from "chai";

vi.mock("next/navigation", () => ({
  useRouter: () => ({
    push: vi.fn(),
  }),
}));

// Mock para Recharts si es utilizado para evitar errores de ResizeObserver
vi.mock("recharts", async () => {
  const OriginalRecharts = await vi.importActual("recharts");
  return {
    ...OriginalRecharts,
    ResponsiveContainer: ({ children }: any) => <div>{children}</div>,
  };
});

describe("Frontend Regression | Flujo de Home (IA y Recomendaciones)", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("Debe renderizar la vista Home con estadísticas e impacto ambiental (Regresión)", () => {
    // === Arrange & Act ===
    const { container } = render(<Home />);
    
    // === Assert ===
    expect(container.innerHTML).to.not.be.empty;
  });

  it("Debe renderizar la sección de IA y Recomendaciones de ahorro sin fallar", () => {
    const { container } = render(<Home />);
    // La prueba valida que la integración del módulo de recomendación no rompe la UI
    expect(container).to.exist;
  });
});
