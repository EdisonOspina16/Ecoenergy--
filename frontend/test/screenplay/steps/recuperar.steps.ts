import { Given, When, Then } from "@cucumber/cucumber";
import { expect } from "chai";
import { ScreenplayWorld } from "../support/world";
import { RegisterUser } from "../screenplay/tasks/registerUser";
import { ChangePassword } from "../screenplay/tasks/changePassword";
import { uniqueEmail, uniquePassword } from "../support/env";
import { BrowseTheWeb } from "../screenplay/abilities/browseTheWeb";

Given("existe un usuario registrado", async function (this: ScreenplayWorld) {
  const email = uniqueEmail();
  const password = uniquePassword();
  this.data.email = email;
  this.data.password = password;

  await this.actor?.attemptsTo(
    RegisterUser.with(
      {
        nombre: "Usuario",
        apellidos: "Recuperar",
        correo: email,
        contrasena: password,
      },
      this.baseUrl,
    ),
  );
});

When("solicita cambio de contrasena", async function (this: ScreenplayWorld) {
  const email = this.data.email ?? this.credentials.email;
  const newPassword = uniquePassword();
  this.data.password = newPassword;

  await this.actor?.attemptsTo(
    ChangePassword.with(email, newPassword, this.baseUrl),
  );
});

Then(
  "deberia ver confirmacion de contrasena",
  async function (this: ScreenplayWorld) {
    const page = this.actor?.abilityTo(BrowseTheWeb).page;
    await page?.getByText(/actualizada/i).waitFor();
    const visible = await page?.getByText(/actualizada/i).isVisible();
    expect(visible).to.equal(true);
  },
);
