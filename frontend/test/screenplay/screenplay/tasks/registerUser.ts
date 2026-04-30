import type { Task } from "../task";
import { Actor } from "../actor";
import { BrowseTheWeb } from "../abilities/browseTheWeb";
import { buildUrl } from "../../support/env";

export type UserRegistration = {
  nombre: string;
  apellidos: string;
  correo: string;
  contrasena: string;
};

export class RegisterUser implements Task {
  constructor(
    private readonly baseUrl: string,
    private readonly user: UserRegistration,
  ) {}

  static with(user: UserRegistration, baseUrl: string) {
    return new RegisterUser(baseUrl, user);
  }

  async performAs(actor: Actor): Promise<void> {
    const page = actor.abilityTo(BrowseTheWeb).page;

    await page.goto(buildUrl(this.baseUrl, "/registro"));
    await page.getByPlaceholder(/nombre/i).fill(this.user.nombre);
    await page.getByPlaceholder(/apellidos/i).fill(this.user.apellidos);
    await page.getByPlaceholder(/correo/i).fill(this.user.correo);
    await page.getByPlaceholder(/contrasena/i).fill(this.user.contrasena);
    await page.getByRole("button", { name: /COMPLETAR REGISTRO/i }).click();
    await page.waitForURL(/\/login$/);
  }
}
