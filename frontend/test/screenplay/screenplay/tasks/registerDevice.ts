import type { Task } from "../task";
import { Actor } from "../actor";
import { BrowseTheWeb } from "../abilities/browseTheWeb";

export class RegisterDevice implements Task {
  constructor(
    private readonly deviceId: string,
    private readonly name: string,
  ) {}

  static with(deviceId: string, name: string) {
    return new RegisterDevice(deviceId, name);
  }

  async performAs(actor: Actor): Promise<void> {
    const page = actor.abilityTo(BrowseTheWeb).page;

    await page.getByLabel(/ID del Dispositivo/i).fill(this.deviceId);
    await page.getByLabel(/Apodo/i).fill(this.name);
    await page
      .getByRole("button", { name: /Registrar Tomacorriente/i })
      .click();
  }
}
