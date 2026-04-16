import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useSubscribe } from '@/hooks/useSubscribe';
import { postSubscribe } from '@/lib/api/subscribe';

// Mock: Simulando request de Subscribe API
vi.mock('@/lib/api/subscribe', () => ({
  postSubscribe: vi.fn(),
}));

describe('Hook: useSubscribe', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('debería limpiar el form y dar un mensaje verde de éxito al suscribirse (Camino Normal)', async () => {
    // === Arrange ===
    (postSubscribe as any).mockResolvedValue({
      ok: true,
      data: { error: undefined, success: true }
    });

    const { result } = renderHook(() => useSubscribe());

    act(() => {
      result.current.setEmail('suscriptor@ecoenergy.com');
    });

    // === Act ===
    await act(async () => {
      await result.current.handleSubscribe();
    });

    // === Assert ===
    expect(postSubscribe).toHaveBeenCalledWith({ email: 'suscriptor@ecoenergy.com' });
    expect(result.current.message).toBe("¡Gracias por unirte a la comunidad! 🌱");
    expect(result.current.email).toBe(''); // Limpia state al tener exito
  });

  it('debería validar que no pasen correos vacíos sin llamar API (Caso Borde)', async () => {
    // === Arrange ===
    const { result } = renderHook(() => useSubscribe());

    act(() => {
      result.current.setEmail('');
    });

    // === Act ===
    await act(async () => {
      await result.current.handleSubscribe();
    });

    // === Assert ===
    expect(postSubscribe).not.toHaveBeenCalled();
    expect(result.current.message).toBe("Por favor ingresa un correo válido");
  });

  it('debería fallar de forma elegante si API retorna un error interno conocido (Caso Error)', async () => {
    // === Arrange ===
    (postSubscribe as any).mockResolvedValue({
      ok: true,
      data: { error: "El correo ya está suscrito" }
    });

    const { result } = renderHook(() => useSubscribe());

    act(() => {
      result.current.setEmail('existe@ecoenergy.com');
    });

    // === Act ===
    await act(async () => {
      await result.current.handleSubscribe();
    });

    // === Assert ===
    // Asegurarse de que el input email no se limpie para que el usuario pueda corregirlo si hace falta
    expect(result.current.message).toBe("El correo ya está suscrito");
    expect(result.current.email).toBe('existe@ecoenergy.com'); 
  });
});

