import React from 'react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Recuperar from '../../src/app/recuperar/page';
import * as useRecuperarHook from '../../src/hooks/useRecuperar';

// Mockeamos head para evitar errores de next/head
vi.mock('next/head', () => ({
  default: ({ children }: { children: React.ReactNode }) => <>{children}</>,
}));

describe('Página: Recuperar Contraseña', () => {
  let mockUseRecuperar: any;

  beforeEach(() => {
    vi.clearAllMocks();
    mockUseRecuperar = {
      correo: '',
      setCorreo: vi.fn(),
      nuevacontrasena: '',
      setNuevacontrasena: vi.fn(),
      error: '',
      success: '',
      loading: false,
      handleSubmit: vi.fn((e) => e.preventDefault()),
    };

    // Spy a la implementación del hook
    vi.spyOn(useRecuperarHook, 'useRecuperar').mockReturnValue(mockUseRecuperar);
  });

  it('debería renderizar la página correctamente sin errores (Render Dummy)', () => {
    render(<Recuperar />);
    
    // Verifica elementos
    expect(screen.getByText('RECUPERAR contrasena')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Tu correo electrónico')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Nueva contrasena')).toBeInTheDocument();
  });

  it('debería llamar los setters cuando el usuario escribe en inputs (Act)', () => {
    Object.defineProperty(mockUseRecuperar, 'correo', { value: 'nuevo@mail' });
    Object.defineProperty(mockUseRecuperar, 'nuevacontrasena', { value: 'pass' });
    
    // Aislamos el hook devolviendo callbacks que actuen 
    vi.spyOn(useRecuperarHook, 'useRecuperar').mockReturnValue({
      ...mockUseRecuperar,
      setCorreo: mockUseRecuperar.setCorreo,
      setNuevacontrasena: mockUseRecuperar.setNuevacontrasena
    });

    render(<Recuperar />);
    
    const inputEmail = screen.getByPlaceholderText('Tu correo electrónico');
    fireEvent.change(inputEmail, { target: { value: 'a@a.com' } });
    
    expect(mockUseRecuperar.setCorreo).toHaveBeenCalledWith('a@a.com');

    const inputPass = screen.getByPlaceholderText('Nueva contrasena');
    fireEvent.change(inputPass, { target: { value: '123' } });

    expect(mockUseRecuperar.setNuevacontrasena).toHaveBeenCalledWith('123');
  });

  it('debería llamar a handleSubmit al enviar el form (Spy sobre Submit)', async () => {
    const { container } = render(<Recuperar />);
    
    // Llenar campos requeridos para evitar cualquier bloqueo de validación nativa (aunque JSDOM suele ignorarlos, es mejor práctica)
    const inputEmail = screen.getByPlaceholderText('Tu correo electrónico');
    fireEvent.change(inputEmail, { target: { value: 'a@a.com' } });
    const inputPass = screen.getByPlaceholderText('Nueva contrasena');
    fireEvent.change(inputPass, { target: { value: '123' } });

    const form = container.querySelector('form');
    if (form) {
      fireEvent.submit(form);
    } else {
      const botonAceptar = screen.getByRole('button', { name: /ACTUALIZAR CONTRASENA/i });
      fireEvent.click(botonAceptar);
    }

    expect(mockUseRecuperar.handleSubmit).toHaveBeenCalled();
  });

  it('debería mostrar mensaje de error si el hook tiene estado error configurado (Assert Render)', () => {
    // Caso de uso: UI reactiva
    vi.spyOn(useRecuperarHook, 'useRecuperar').mockReturnValue({
      ...mockUseRecuperar,
      error: 'Correo no encontrado'
    });

    render(<Recuperar />);
    
    expect(screen.getByText('Correo no encontrado')).toBeInTheDocument();
  });

  it('debería mostrar mensaje de success si el hook tiene estado success (Assert Render)', () => {
    vi.spyOn(useRecuperarHook, 'useRecuperar').mockReturnValue({
      ...mockUseRecuperar,
      success: 'Exito rotundo'
    });

    render(<Recuperar />);
    expect(screen.getByText('Exito rotundo')).toBeInTheDocument();
  });
  
  it('debería deshabilitar e indicar LOADING visualmente cuando hook loading=true', () => {
    vi.spyOn(useRecuperarHook, 'useRecuperar').mockReturnValue({
      ...mockUseRecuperar,
      loading: true
    });

    render(<Recuperar />);
    const boton = screen.getByRole('button');
    expect(boton).toBeDisabled();
    expect(screen.getByText(/ACTUALIZANDO/i)).toBeInTheDocument();
  });
});
