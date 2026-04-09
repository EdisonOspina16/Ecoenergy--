import { API_URL } from "../config/api";
import { postJson, JsonResult } from "../http/jsonClient";

export type SubscribePayload = {
  email: string;
};

export type SubscribeResponse = {
  success?: boolean;
  message?: string;
  error?: string;
};

export async function postSubscribe(payload: SubscribePayload): Promise<JsonResult<SubscribeResponse>> {
  return postJson<SubscribeResponse>(`${API_URL}/subscribe`, payload);
}
