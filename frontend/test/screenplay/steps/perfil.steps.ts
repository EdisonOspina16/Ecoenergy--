import { Given, When, Then } from "@cucumber/cucumber";
import { expect } from "chai";
import { ScreenplayWorld } from "../support/world";
import { Login } from "../screenplay/tasks/login";
import { OpenPage } from "../screenplay/tasks/openPage";
import { CreateHomeProfile } from "../screenplay/tasks/createHomeProfile";
import { BrowseTheWeb } from "../screenplay/abilities/browseTheWeb";
import { uniqueAddress, uniqueHomeName } from "../support/env";

Given(
  "el usuario esta autenticado y en perfil",
  async function (this: ScreenplayWorld) {
    const { email, password } = this.credentials;
    await this.actor?.attemptsTo(Login.with(email, password, this.baseUrl));
    await this.actor?.attemptsTo(OpenPage.at("/perfil", this.baseUrl));
    const page = this.actor?.abilityTo(BrowseTheWeb).page;
    await page
      ?.getByText("Mi Perfil y Dispositivos", { exact: false })
      .waitFor();
  },
);

When(
  "crea o actualiza el perfil del hogar",
  async function (this: ScreenplayWorld) {
    const homeName = uniqueHomeName();
    const address = uniqueAddress();
    this.data.homeName = homeName;
    this.data.address = address;

    await this.actor?.attemptsTo(
      CreateHomeProfile.with(homeName, address, this.baseUrl),
    );
  },
);

Then(
  "deberia ver confirmacion del perfil",
  async function (this: ScreenplayWorld) {
    const page = this.actor?.abilityTo(BrowseTheWeb).page;
    const locator = page?.getByText(/Perfil (guardado|creado|actualizado)/i);
    await locator?.waitFor();
    const visible = await locator?.isVisible();
    expect(visible).to.equal(true);
  },
);
