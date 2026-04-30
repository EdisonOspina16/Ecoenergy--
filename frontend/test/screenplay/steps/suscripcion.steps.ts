import { Given, When, Then } from "@cucumber/cucumber";
import { expect } from "chai";
import { ScreenplayWorld } from "../support/world";
import { SubscribeEmail } from "../screenplay/tasks/subscribeEmail";
import { OpenPage } from "../screenplay/tasks/openPage";
import { BrowseTheWeb } from "../screenplay/abilities/browseTheWeb";
import { uniqueEmail } from "../support/env";

Given(
  "el usuario esta en la pagina de inicio",
  async function (this: ScreenplayWorld) {
    await this.actor?.attemptsTo(OpenPage.at("/", this.baseUrl));
  },
);

When(
  "registra su correo en la comunidad",
  async function (this: ScreenplayWorld) {
    const email = uniqueEmail();
    this.data.email = email;
    await this.actor?.attemptsTo(SubscribeEmail.with(email));
  },
);

Then(
  "deberia ver mensaje de suscripcion",
  async function (this: ScreenplayWorld) {
    const page = this.actor?.abilityTo(BrowseTheWeb).page;
    const locator = page?.getByText(/Gracias por unirte a la comunidad/i);
    await locator?.waitFor();
    const visible = await locator?.isVisible();
    expect(visible).to.equal(true);
  },
);
