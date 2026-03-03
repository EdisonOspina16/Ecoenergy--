import "@testing-library/jest-dom";
import "whatwg-fetch";
import { vi } from "vitest";

// Mock next/navigation useRouter para poder espiar push/replace
const pushMock = vi.fn();
const replaceMock = vi.fn();
const prefetchMock = vi.fn();

// Exponemos los mocks en globalThis para que los tests los lean
// (solo para evitar un archivo de mock dedicado)
// @ts-expect-error propiedad de ayuda para tests
globalThis.__routerPush = pushMock;

vi.mock("next/navigation", () => {
  return {
    useRouter: () => ({
      push: pushMock,
      replace: replaceMock,
      prefetch: prefetchMock,
    }),
  };
});
