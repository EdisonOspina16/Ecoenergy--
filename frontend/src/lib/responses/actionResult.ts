import { JsonResult } from "../http/jsonClient";

type Messages = {
  success?: string;
  fallbackError: string;
  customError?: (response: any) => string | undefined;
};

export type ActionResult<T> =
  | { ok: true; data: T; message: string }
  | { ok: false; message: string };

export function buildActionResult<TResponse, TData>(
  result: JsonResult<TResponse>,
  pickData: (response: TResponse) => TData | undefined,
  messages: Messages,
): ActionResult<TData> {
  if (!result.ok) {
    return { ok: false, message: result.message || messages.fallbackError };
  }

  const derivedError = messages.customError?.(result.data);
  if (derivedError) {
    return { ok: false, message: derivedError };
  }

  const data = pickData(result.data);
  if (data) {
    return {
      ok: true,
      data,
      message: messages.success ?? "Operación exitosa",
    };
  }

  return { ok: false, message: messages.fallbackError };
}
