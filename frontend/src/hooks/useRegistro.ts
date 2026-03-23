export type RegistrarUsuarioSetters = {
  setLoading: (value: boolean) => void;
  setError: (value: string) => void;
};

import { postRegistro, resolveError } from "../lib/api/registro";

export async function registrarUsuario(
  nombre: string,
  apellidos: string,
  correo: string,
  contrasena: string,
  { setLoading, setError }: RegistrarUsuarioSetters
): Promise<void> {
  setError("");
  setLoading(true);

  try {
    const result = await postRegistro({ nombre, apellidos, correo, contrasena });

    if (result.ok) {
      window.location.href = result.redirect;
    } else {
      setError(result.error);
    }
  } catch (error) {
    setError(resolveError(error));
  } finally {
    setLoading(false);
  }
}