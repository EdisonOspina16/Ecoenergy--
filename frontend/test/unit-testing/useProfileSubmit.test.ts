import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useProfileSubmit } from '@/hooks/useProfileSubmit';
import { postProfile } from '@/lib/api/profile';

// Mock: Simulamos la respuesta de postProfile porque ya se asume testeada aparte (o en el mismo suite).
// Usamos mock en lugar de spy/stub simple para interceptar importaciones directamente.
vi.mock('@/lib/api/profile', () => ({
  postProfile: vi.fn(),
  fetchPerfil: vi.fn(),
}));

describe('Hook: useProfileSubmit', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('debería actualizar el estado y enviar mensaje exitoso al guardar (Camino Normal)', async () => {
    // === Arrange ===
    // Spy: Función para verificar si se enviaron mensajes
    const mostrarMensajeSpy = vi.fn();
    
    // Stubbing el comportamiento del mock previamente definido
    (postProfile as any).mockResolvedValue({
      ok: true,
      data: { success: true, message: "Perfil guardado con éxito" }
    });

    const { result } = renderHook(() => useProfileSubmit(mostrarMensajeSpy));

    // === Act ===
    await act(async () => {
      await result.current.submitProfile({ address: "Calle 123", nombre_hogar: "Mi Casa" });
    });

    // === Assert ===
    // Nos aseguramos que al finalizar devuelva false en el flag "profileSaving"
    expect(result.current.profileSaving).toBe(false);
    expect(postProfile).toHaveBeenCalledWith({ address: "Calle 123", nombre_hogar: "Mi Casa" });
    expect(mostrarMensajeSpy).toHaveBeenCalledWith("success", "Perfil guardado con éxito");
  });

  it('debería retornar error cuando faltan campos mandatorios (Caso Borde)', async () => {
    // === Arrange ===
    const mostrarMensajeSpy = vi.fn();
    const { result } = renderHook(() => useProfileSubmit(mostrarMensajeSpy));

    // === Act ===
    await act(async () => {
      // Pasamos un objeto con campos nulos o vacíos
      await result.current.submitProfile({ address: "", nombre_hogar: "Mi Casa" });
    });

    // === Assert ===
    // Validamos que se lance de inmediato el mensaje de error sin llamar a la API
    expect(mostrarMensajeSpy).toHaveBeenCalledWith("error", "La dirección y el nombre del hogar son requeridos");
    expect(postProfile).not.toHaveBeenCalled();
  });

  it('debería recibir y emitir error del backend correctamente (Caso Error)', async () => {
    // === Arrange ===
    const mostrarMensajeSpy = vi.fn();
    // Stub del mock que devuelve error intencional (result.ok = false u ok con error)
    (postProfile as any).mockResolvedValue({
      ok: true,
      data: { success: false, error: "La dirección no es válida" }
    });

    const { result } = renderHook(() => useProfileSubmit(mostrarMensajeSpy));

    // === Act ===
    await act(async () => {
      await result.current.submitProfile({ address: "Inválida", nombre_hogar: "Mi Casa" });
    });

    // === Assert ===
    expect(mostrarMensajeSpy).toHaveBeenCalledWith("error", "La dirección no es válida");
  });

  it('debería capturar el error .ok falso sin succes o mensaje manejado (Fallback Error global) y fallbacks genéricos de fallback.data', async () => {
    const mostrarMensajeSpy = vi.fn();
    (postProfile as any).mockResolvedValue({
      ok: false
      // NO enviamos result.message, forzando el default
    });

    const { result } = renderHook(() => useProfileSubmit(mostrarMensajeSpy));

    // Act
    await act(async () => {
      await result.current.submitProfile({ address: "Inválida", nombre_hogar: "Mi Casa" });
    });

    // Assert de fallback global falso
    expect(mostrarMensajeSpy).toHaveBeenCalledWith("error", "Error al conectar con el servidor");
  });

  it('debería capturar el fallback de data en caso de no venir strings directos en la data (Fallback data.message o data.error)', async () => {
    const mostrarMensajeSpy = vi.fn();
    (postProfile as any).mockResolvedValue({
      ok: true,
      data: { success: true } // Fata result.data.message
    });

    const { result } = renderHook(() => useProfileSubmit(mostrarMensajeSpy));

    await act(async () => {
      await result.current.submitProfile({ address: "Inválida", nombre_hogar: "Mi Casa" });
    });

    // Verifica que se inyecta el String alterno al venir data sin message
    expect(mostrarMensajeSpy).toHaveBeenCalledWith("success", "Perfil guardado con éxito");
  });

  it('debería ejecutar el try/catch y mostrar mensaje generic al haber error critico (Case Exception Catch)', async () => {
    const mostrarMensajeSpy = vi.fn();
    (postProfile as any).mockRejectedValue(new Error("Net::Err_Connection_Refused"));
    const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

    const { result } = renderHook(() => useProfileSubmit(mostrarMensajeSpy));

    await act(async () => {
      await result.current.submitProfile({ address: "Inválida", nombre_hogar: "Mi Casa" });
    });

    expect(consoleSpy).toHaveBeenCalled();
    expect(mostrarMensajeSpy).toHaveBeenCalledWith("error", "Error al conectar con el servidor");
    expect(result.current.profileSaving).toBe(false);
  });
});

