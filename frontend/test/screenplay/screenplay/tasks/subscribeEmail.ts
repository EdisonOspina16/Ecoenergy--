import type { Task } from "../task";
import { Actor } from "../actor";
import { BrowseTheWeb } from "../abilities/browseTheWeb";
export class SubscribeEmail implements Task {
  constructor(private readonly email: string) {}

  static with(email: string) {
    return new SubscribeEmail(email);
  }

  async performAs(actor: Actor): Promise<void> {
    const page = actor.abilityTo(BrowseTheWeb).page;
    await page.getByPlaceholder(/correo/i).fill(this.email);
    await page.getByRole("button", { name: /Unirse a la comunidad/i }).click();
  }
}
