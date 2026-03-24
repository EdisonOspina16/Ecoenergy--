import { useState } from "react";
import { registerDevice, DeviceData } from "../lib/api/devices";

export type Notify = (type: "success" | "error", message: string) => void;

export function useDeviceRegistration(
  onRegistered: (device: DeviceData) => void,
  notify: Notify,
) {
  const [deviceId, setDeviceId] = useState("");
  const [nickname, setNickname] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const resetForm = () => {
    setDeviceId("");
    setNickname("");
  };

  const submit = async () => {
    const validation = validateInput(deviceId, nickname);
    if (!validation.ok) {
      notify("error", validation.message);
      return;
    }

    setSubmitting(true);
    const result = await registerDevice({ deviceId, nickname });
    setSubmitting(false);

    if (!result.ok) {
      notify("error", result.message);
      return;
    }

    onRegistered(result.data);
    resetForm();
    notify("success", result.message);
  };

  return {
    deviceId,
    nickname,
    submitting,
    setDeviceId,
    setNickname,
    submit,
  };
}

type ValidationResult = { ok: true } | { ok: false; message: string };

function validateInput(id: string, name: string): ValidationResult {
  if (!id.trim())
    return { ok: false, message: "Ingresa el ID del dispositivo" };
  if (!name.trim())
    return { ok: false, message: "Ingresa el apodo del dispositivo" };
  return { ok: true };
}
