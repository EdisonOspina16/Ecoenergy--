import React from 'react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import PrincipalPage from '../../src/app/page';

// Mock de next/navigation (Router)
vi.mock('next/navigation', () => ({
  useRouter: () => ({ push: vi.fn(), replace: vi.fn() })
}));

// Spy sobre nuestro custom hook useSubscribe
import * as useSubscribeHooks from '../../src/hooks/useSubscribe';

describe('Página: Landing Principal (Subscribe)', () => {
  const mockHandleSubscribe = vi.fn();
  
  beforeEach(() => {
    vi.clearAllMocks();

    vi.spyOn(useSubscribeHooks, 'useSubscribe').mockReturnValue({
      email: '',
      setEmail: vi.fn(),
      loading: false,
      message: '',
      handleSubscribe: mockHandleSubscribe
    });
  });

  it('debería renderizar la página hero con titulo correcto (Render Normal)', () => {
    render(<PrincipalPage />);
    
    // Al haber múltiples 'EcoEnergy' (header y footer), usamos getAllByText y validamos que al menos uno esté
    const logos = screen.getAllByText('EcoEnergy');
    expect(logos.length).toBeGreaterThan(0);
    expect(screen.getByText(/Energía Inteligente para un/i)).toBeInTheDocument();
  });

  it('debería invocar la función handleSubscribe al dar click en el CTA de suscripción (Act / Spy)', () => {
    render(<PrincipalPage />);
    
    const botonSuscribir = screen.getByRole('button', { name: /Unirse a la comunidad/i });
    fireEvent.click(botonSuscribir);

    expect(mockHandleSubscribe).toHaveBeenCalled();
  });

  it('debería actualizar visualmente la UI si loading está true en el estado del hook (Componente reactivo UI)', () => {
    vi.spyOn(useSubscribeHooks, 'useSubscribe').mockReturnValue({
      email: '',
      setEmail: vi.fn(),
      loading: true,
      message: '',
      handleSubscribe: mockHandleSubscribe
    });

    render(<PrincipalPage />);
    const botonSuscribir = screen.getByRole('button', { name: /Enviando.../i });
    expect(botonSuscribir).toBeDisabled();
    expect(screen.getByText(/Enviando.../i)).toBeInTheDocument();
  });

  it('debería mostrar el feedback message que emite el Hook (Feedback UI render)', () => {
    vi.spyOn(useSubscribeHooks, 'useSubscribe').mockReturnValue({
      email: '',
      setEmail: vi.fn(),
      loading: false,
      message: '¡Gracias por unirte a la comunidad! 🌱',
      handleSubscribe: mockHandleSubscribe
    });

    render(<PrincipalPage />);
    expect(screen.getByText('¡Gracias por unirte a la comunidad! 🌱')).toBeInTheDocument();
  });
});
