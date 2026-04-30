import type { Question } from "../question";
import { Actor } from "../actor";
import { BrowseTheWeb } from "../abilities/browseTheWeb";
import { inputWithValue } from "../locators/displayValue";

export class DeviceStatus implements Question<string> {
  constructor(private readonly name: string) {}

  static forDevice(name: string) {
    return new DeviceStatus(name);
  }

  async answeredBy(actor: Actor): Promise<string> {
    const page = actor.abilityTo(BrowseTheWeb).page;
    const item = page.locator("li", {
      has: inputWithValue(page, this.name),
    });
    const status = item.locator("span").filter({
      hasText: /Conectado|Desconectado/i,
    });

    await status.first().waitFor();
    return (await status.first().innerText()).trim();
  }
}
