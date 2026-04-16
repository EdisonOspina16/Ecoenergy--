import { describe, it, expect, vi, beforeEach } from 'vitest';
import { fetchDispositivos } from '@/lib/api/dispositivos';
import { cargarDispositivos } from '@/hooks/useDispositivos';

describe('Dispositivos API (fetchDispositivos)', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('debería retornar dispositivos cuando la respuesta es ok (Camino Normal)', async () => {
    // === Arrange ===
    // Stub: Simula respuesta exitosa del servidor.
    // Usamos Stub porque no queremos hacer llamadas HTTP reales en las pruebas.
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ success: true, dispositivos: [{ nombre: 'TV', consumo: 100, estado: 'Encendido' }] })
    });

    // === Act ===
    const result = await fetchDispositivos();

    // === Assert ===
    expect(global.fetch).toHaveBeenCalledWith(expect.stringContaining('/dispositivos'), expect.any(Object));
    expect(result).toEqual({
      ok: true,
      dispositivos: [{ nombre: 'TV', consumo: 100, estado: 'Encendido' }]
    });
  });

  it('debería arrojar error cuando falla la petición de servidor (Caso de Error)', async () => {
    // === Arrange ===
    // Stub: Simula error HTTP 500 o similar, respuesta no 'ok'.
    global.fetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 500
    });

    // === Act & Assert ===
    await expect(fetchDispositivos()).rejects.toThrow("Error al obtener dispositivos");
  });
});

describe('Hook: cargarDispositivos', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('debería llamar a los setters correctamente cuando el API responde exitosamente (Camino Normal)', async () => {
    // === Arrange ===
    // Stub global.fetch para enrutar el camino feliz y asegurar datos correctos
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ success: true, dispositivos: [{ nombre: 'TV', consumo: '50' }] })
    });

    // Spy: Observamos las funciones setters para validar la interacción interna del hook
    const setDevicesSpy = vi.fn();
    const setLoadingDevicesSpy = vi.fn();

    // === Act ===
    await cargarDispositivos({ setDevices: setDevicesSpy, setLoadingDevices: setLoadingDevicesSpy });

    // === Assert ===
    expect(setDevicesSpy).toHaveBeenCalledWith([{ nombre: 'TV', consumo: 50, estado: 'Desconocido' }]);
    expect(setLoadingDevicesSpy).toHaveBeenCalledWith(false);
  });

  it('debería asignar un array vacío cuando ocurre una excepción en la carga (Caso de Error)', async () => {
    // === Arrange ===
    // Stub: Simular rechazo de red (Error interno)
    global.fetch = vi.fn().mockRejectedValue(new Error('Network error'));
    
    // Configurar silenciado de console.error temporalmente para este test
    const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    
    const setDevicesSpy = vi.fn();
    const setLoadingDevicesSpy = vi.fn();

    // === Act ===
    await cargarDispositivos({ setDevices: setDevicesSpy, setLoadingDevices: setLoadingDevicesSpy });

    // === Assert ===
    // Verifica que en caso de catch lance array vacio y finalice carga
    expect(setDevicesSpy).toHaveBeenCalledWith([]);
    expect(setLoadingDevicesSpy).toHaveBeenCalledWith(false);
    expect(consoleSpy).toHaveBeenCalled();
  });
});

