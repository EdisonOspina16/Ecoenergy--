import type { Actor } from "./actor";

export interface Task {
  performAs(actor: Actor): Promise<void>;
}
