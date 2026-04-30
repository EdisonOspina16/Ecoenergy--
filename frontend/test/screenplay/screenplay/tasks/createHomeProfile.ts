import type { Task } from "../task";
import { Actor } from "../actor";
import { BrowseTheWeb } from "../abilities/browseTheWeb";
import { buildUrl } from "../../support/env";

export class CreateHomeProfile implements Task {
  constructor(
    private readonly baseUrl: string,
    private readonly homeName: string,
    private readonly address: string,
  ) {}

  static with(homeName: string, address: string, baseUrl: string) {
    return new CreateHomeProfile(baseUrl, homeName, address);
  }

  async performAs(actor: Actor): Promise<void> {
    const page = actor.abilityTo(BrowseTheWeb).page;

    await page.goto(buildUrl(this.baseUrl, "/perfil"));
    await page.getByPlaceholder(/Mi Casa/i).fill(this.homeName);
    await page.getByPlaceholder(/Calle/i).fill(this.address);
    await page.getByRole("button", { name: /Guardar Cambios/i }).click();
  }
}
