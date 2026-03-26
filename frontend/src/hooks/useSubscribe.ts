import { useState } from "react";
import { postSubscribe } from "../lib/api/subscribe";

export function useSubscribe() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const handleSubscribe = async () => {
    if (!email) {
      setMessage("Por favor ingresa un correo válido");
      return;
    }

    setLoading(true);
    setMessage("");

    try {
      const result = await postSubscribe({ email });

      if (result.ok) {
        if (!result.data.error) {
          setMessage("¡Gracias por unirte a la comunidad! 🌱");
          setEmail("");
        } else {
          setMessage(result.data.error || "Error al registrar el correo");
        }
      } else {
        setMessage(result.message || "Error al registrar el correo");
      }
    } catch (error) {
      console.error("Error al registrar correo:", error);
      setMessage("No se pudo conectar con el servidor");
    } finally {
      setLoading(false);
    }
  };

  return {
    email,
    setEmail,
    loading,
    message,
    handleSubscribe
  };
}
