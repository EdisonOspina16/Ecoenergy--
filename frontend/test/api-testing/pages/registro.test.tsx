import React from 'react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Registro from '@/app/registro/page';
import * as useRegistroHook from '@/hooks/useRegistro';

vi.mock('next/head', () => ({
  default: ({ children }: { children: React.ReactNode }) => <>{children}</>,
}));

vi.mock('@/hooks/useRegistro', () => ({
  registrarUsuario: vi.fn(),
}));

describe('Página: Registro de Usuario', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('debería renderizar el formulario de registro correctamente', () => {
    render(<Registro />);
    
    expect(screen.getByText('REGISTRO')).toBeInTheDocument();
  });

  it('debería llamar a registrarUsuario con los datos del form al hacer submit', async () => {
    const mockRegistrarFn = vi.mocked(useRegistroHook.registrarUsuario);
    render(<Registro />);
    
    fireEvent.change(screen.getByPlaceholderText('Tu nombre'), { target: { value: 'Juan' } });
    fireEvent.change(screen.getByPlaceholderText('Tus apellidos'), { target: { value: 'Perez' } });
    fireEvent.change(screen.getByPlaceholderText('Tu correo electrónico'), { target: { value: 'juan@mail.com' } });
    fireEvent.change(screen.getByPlaceholderText('Tu contrasena'), { target: { value: '123456' } });

    const boton = screen.getByRole('button', { name: /COMPLETAR REGISTRO/i });
    fireEvent.click(boton);

    expect(mockRegistrarFn).toHaveBeenCalledWith('Juan', 'Perez', 'juan@mail.com', '123456', expect.any(Object));
  });

  it('debería mostrar estado de cargando mientras se registra', async () => {
    const mockRegistrarFn = vi.mocked(useRegistroHook.registrarUsuario);
    mockRegistrarFn.mockImplementation((n, a, c, p, setters) => {
      setters.setLoading(true);
      return new Promise(() => {});
    });

    const { container } = render(<Registro />);
    
    const form = container.querySelector('form');
    if (form) {
      fireEvent.submit(form);
    } else {
      const boton = screen.getByRole('button', { name: /COMPLETAR REGISTRO/i });
      fireEvent.click(boton);
    }

    // Verificamos al menos que el botón se deshabilita, lo cual confirma que el estado cambió
    await waitFor(() => {
       expect(screen.getByRole('button')).toBeDisabled();
    });
  });
});

