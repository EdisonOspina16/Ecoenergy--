"use client";

import { useCallback, useState } from "react";
import { useRouter } from "next/navigation";
import { loginRequest } from "../lib/api/auth";

type LoginState = {
  correo: string;
  contrasena: string;
  error: string;
  loading: boolean;
};

const initialState: LoginState = {
  correo: "",
  contrasena: "",
  error: "",
  loading: false,
};

export function useLogin() {
  const router = useRouter();
  const [state, setState] = useState<LoginState>(initialState);

  const setCorreo = useCallback((value: string) => {
    setState((prev) => ({ ...prev, correo: value }));
  }, []);

  const setContrasena = useCallback((value: string) => {
    setState((prev) => ({ ...prev, contrasena: value }));
  }, []);

  const resetError = useCallback(() => {
    setState((prev) => ({ ...prev, error: "" }));
  }, []);

  const submit = useCallback(async () => {
    const { correo, contrasena } = state;
    if (!correo || !contrasena) {
      setState((prev) => ({ ...prev, error: "Ingresa correo y contraseña" }));
      return;
    }

    setState((prev) => ({ ...prev, loading: true, error: "" }));

    const result = await loginRequest({ correo, contrasena });

    if (result.ok) {
      setState((prev) => ({ ...prev, loading: false }));
      router.push(result.redirect);
      return;
    }

    setState((prev) => ({ ...prev, loading: false, error: result.message }));
  }, [state, router]);

  return {
    correo: state.correo,
    contrasena: state.contrasena,
    error: state.error,
    loading: state.loading,
    setCorreo,
    setContrasena,
    resetError,
    submit,
  };
}
