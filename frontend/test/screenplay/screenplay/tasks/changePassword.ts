import type { Task } from "../task";
import { Actor } from "../actor";
import { BrowseTheWeb } from "../abilities/browseTheWeb";
import { buildUrl } from "../../support/env";

export class ChangePassword implements Task {
  constructor(
    private readonly baseUrl: string,
    private readonly email: string,
    private readonly newPassword: string,
  ) {}

  static with(email: string, newPassword: string, baseUrl: string) {
    return new ChangePassword(baseUrl, email, newPassword);
  }

  async performAs(actor: Actor): Promise<void> {
    const page = actor.abilityTo(BrowseTheWeb).page;

    await page.goto(buildUrl(this.baseUrl, "/recuperar"));
    await page.getByPlaceholder(/correo/i).fill(this.email);
    await page.getByPlaceholder(/Nueva contrasena/i).fill(this.newPassword);
    await page.getByRole("button", { name: /ACTUALIZAR CONTRASENA/i }).click();
  }
}
