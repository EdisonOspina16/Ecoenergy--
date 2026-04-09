import { useState } from "react";
import { postProfile, PostProfilePayload } from "../lib/api/profile";

export function useProfileSubmit(
  mostrarMensaje: (type: "success" | "error", text: string) => void
) {
  const [profileSaving, setProfileSaving] = useState(false);

  const submitProfile = async (payload: PostProfilePayload) => {
    if (!payload.address || !payload.nombre_hogar) {
      mostrarMensaje("error", "La dirección y el nombre del hogar son requeridos");
      return;
    }

    try {
      setProfileSaving(true);
      const result = await postProfile(payload);

      if (result.ok) {
        if (result.data.success) {
          mostrarMensaje("success", result.data.message || "Perfil guardado con éxito");
        } else {
          mostrarMensaje("error", result.data.error || "Error al guardar el perfil");
        }
      } else {
        mostrarMensaje("error", result.message || "Error al conectar con el servidor");
      }
    } catch (error) {
      console.error("Error al guardar perfil:", error);
      mostrarMensaje("error", "Error al conectar con el servidor");
    } finally {
      setProfileSaving(false);
    }
  };

  return {
    profileSaving,
    submitProfile,
  };
}
