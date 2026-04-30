import type { Task } from "../task";
import { Actor } from "../actor";
import { BrowseTheWeb } from "../abilities/browseTheWeb";
import { buildUrl } from "../../support/env";

export class Login implements Task {
  constructor(
    private readonly baseUrl: string,
    private readonly email: string,
    private readonly password: string,
  ) {}

  static with(email: string, password: string, baseUrl: string) {
    return new Login(baseUrl, email, password);
  }

  async performAs(actor: Actor): Promise<void> {
    const page = actor.abilityTo(BrowseTheWeb).page;

    await page.goto(buildUrl(this.baseUrl, "/login"));
    await page.getByPlaceholder(/correo/i).fill(this.email);
    await page.getByPlaceholder(/contrasena/i).fill(this.password);
    await page.getByRole("button", { name: /INGRESAR/i }).click();
    await page.waitForURL(/\/(home|dashboard)$/);
  }
}
