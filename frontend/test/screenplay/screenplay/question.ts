import type { Actor } from "./actor";

export interface Question<T> {
  answeredBy(actor: Actor): Promise<T>;
}
