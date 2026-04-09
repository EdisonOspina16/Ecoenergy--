import { useState } from "react";
import { postRecuperar } from "../lib/api/recuperar";

export function useRecuperar() {
  const [correo, setCorreo] = useState("");
  const [nuevacontrasena, setNuevacontrasena] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    setLoading(true);

    try {
      const result = await postRecuperar({ correo, nueva_contrasena: nuevacontrasena });

      if (result.ok) {
        if (!result.data.error) {
          setSuccess(result.data.message || "Contraseña actualizada exitosamente");
          setTimeout(() => {
            if (result.data.redirect) {
              window.location.href = result.data.redirect;
            }
          }, 2000);
        } else {
          setError(result.data.error || "Error al recuperar contrasena");
        }
      } else {
        setError(result.message || "Error al conectar con el servidor");
      }
    } catch (err) {
      console.error("Error en la petición:", err);
      setError("Error al conectar con el servidor");
    } finally {
      setLoading(false);
    }
  };

  return {
    correo,
    setCorreo,
    nuevacontrasena,
    setNuevacontrasena,
    error,
    success,
    loading,
    handleSubmit
  };
}
