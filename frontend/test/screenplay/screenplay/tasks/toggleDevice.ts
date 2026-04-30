import type { Task } from "../task";
import { Actor } from "../actor";
import { BrowseTheWeb } from "../abilities/browseTheWeb";
import { inputWithValue } from "../locators/displayValue";

export class ToggleDevice implements Task {
  constructor(private readonly name: string) {}

  static named(name: string) {
    return new ToggleDevice(name);
  }

  async performAs(actor: Actor): Promise<void> {
    const page = actor.abilityTo(BrowseTheWeb).page;
    const item = page.locator("li", {
      has: inputWithValue(page, this.name),
    });
    await item.getByRole("button", { name: /Conectar|Desconectar/i }).click();
  }
}
