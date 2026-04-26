import { describe, it, vi, beforeEach } from "vitest";
import { renderHook, act } from "@testing-library/react";
import { useLogin } from "@/hooks/useLogin";
import { loginRequest } from "@/lib/api/auth";
import { useRouter } from "next/navigation";
import { expect } from "chai";

// Mock dependencias externas
vi.mock("@/lib/api/auth", () => ({
  loginRequest: vi.fn(),
}));

vi.mock("next/navigation", () => ({
  useRouter: vi.fn(),
}));

describe("Hook: useLogin", () => {
  const mockPush = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
    (useRouter as any).mockReturnValue({ push: mockPush });
  });

  it("debería rutear al redirect y frenar el loading si es ok (Camino Normal)", async () => {
    // === Arrange ===
    (loginRequest as any).mockResolvedValue({
      ok: true,
      redirect: "/dashboard",
    });

    const { result } = renderHook(() => useLogin());

    act(() => {
      result.current.setCorreo("test@correo.com");
      result.current.setContrasena("1234");
    });

    // === Act ===
    await act(async () => {
      await result.current.submit();
    });

    // === Assert ===
    const loginCalls = vi.mocked(loginRequest).mock.calls;
    expect(loginCalls.length).to.equal(1);
    expect(loginCalls[0][0]).to.deep.equal({
      correo: "test@correo.com",
      contrasena: "1234",
    });
    const pushCalls = mockPush.mock.calls;
    expect(pushCalls.length).to.equal(1);
    expect(pushCalls[0][0]).to.equal("/dashboard");
    expect(result.current.loading).to.equal(false);
  });
});
