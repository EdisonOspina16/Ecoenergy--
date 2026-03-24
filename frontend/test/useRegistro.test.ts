import { describe, it, expect, vi, beforeEach } from 'vitest';
import { registrarUsuario, RegistrarUsuarioSetters } from '../src/hooks/useRegistro';
import * as apiRegistro from '../src/lib/api/registro';

// Mock del módulo entero: Aisla completamente la lógica de validación de los Custom Hooks
// garantizando que no dispare lógica de fetch accidentalmente. Emplea Stubs globales.
vi.mock('../src/lib/api/registro', () => ({
  postRegistro: vi.fn(),
  resolveError: vi.fn((err: any) => err?.message || 'Error resuelto')
}));

describe('useRegistro - registrarUsuario', () => {
  // Spies: Usados para verificar que los estados de carga se alteren adecuadamente
  let setLoadingSpy: ReturnType<typeof vi.fn>;
  let setErrorSpy: ReturnType<typeof vi.fn>;
  let setters: RegistrarUsuarioSetters;

  beforeEach(() => {
    vi.restoreAllMocks();
    setLoadingSpy = vi.fn();
    setErrorSpy = vi.fn();
    setters = { setLoading: setLoadingSpy, setError: setErrorSpy };
    
    // Stub global: mockeamos la propiedad location para evitar que JS intente navegar, previniendo errores en JSDOM.
    Object.defineProperty(window, 'location', {
      value: { href: '' },
      writable: true,
    });
  });

  // Dummy de strings usados sistemáticamente como argumentos
  const dummyNombre = 'N';
  const dummyApellido = 'A';
  const dummyCorreo = 'c@c.com';
  const dummyPass = 'p';

  it('debería registrar y redirigir exitosamente (Camino Normal)', async () => {
    // === Arrange ===
    // Stub: Simulamos respuesta exitosa del objeto Mock
    vi.mocked(apiRegistro.postRegistro).mockResolvedValue({
      ok: true,
      redirect: '/home'
    });

    // === Act ===
    await registrarUsuario(dummyNombre, dummyApellido, dummyCorreo, dummyPass, setters);

    // === Assert ===
    // Spy verification
    expect(setErrorSpy).toHaveBeenCalledWith('');
    expect(setLoadingSpy).toHaveBeenCalledWith(true);
    expect(apiRegistro.postRegistro).toHaveBeenCalledTimes(1);
    expect(window.location.href).toBe('/home');
    expect(setLoadingSpy).toHaveBeenLastCalledWith(false);
  });

  it('debería actualizar error si la respuesta del post fue rechazada lógicamente (Caso Error)', async () => {
    // === Arrange ===
    // Stub: Simulamos error interno procesado
    vi.mocked(apiRegistro.postRegistro).mockResolvedValue({
      ok: false,
      error: 'Contraseña débil'
    });

    // === Act ===
    await registrarUsuario(dummyNombre, dummyApellido, dummyCorreo, dummyPass, setters);

    // === Assert ===
    expect(setErrorSpy).toHaveBeenCalledWith('Contraseña débil');
    expect(setLoadingSpy).toHaveBeenLastCalledWith(false); // Validamos que se cerró el loader
  });

  it('debería usar catch y resolver el error si la promesa subyacente falla (Caso de Excepción)', async () => {
    // === Arrange ===
    // Stub / Dummy: Promesa de mockRejection y Error falso
    const errorSimulado = new Error('Network error');
    vi.mocked(apiRegistro.postRegistro).mockRejectedValue(errorSimulado);
    
    // === Act ===
    await registrarUsuario(dummyNombre, dummyApellido, dummyCorreo, dummyPass, setters);

    // === Assert ===
    expect(setErrorSpy).toHaveBeenCalledWith('Network error');
    expect(setLoadingSpy).toHaveBeenLastCalledWith(false);
  });
});
