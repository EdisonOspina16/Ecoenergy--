import { Given, When, Then } from "@cucumber/cucumber";
import { expect } from "chai";
import { ScreenplayWorld } from "../support/world";
import { Login } from "../screenplay/tasks/login";
import { OpenPage } from "../screenplay/tasks/openPage";
import { GenerateRecommendation } from "../screenplay/tasks/generateRecommendation";
import { BrowseTheWeb } from "../screenplay/abilities/browseTheWeb";

Given(
  "el usuario inicia sesion y abre home",
  async function (this: ScreenplayWorld) {
    const { email, password } = this.credentials;
    await this.actor?.attemptsTo(Login.with(email, password, this.baseUrl));
    await this.actor?.attemptsTo(OpenPage.at("/home", this.baseUrl));
    const page = this.actor?.abilityTo(BrowseTheWeb).page;
    await page?.getByText("Resumen de Consumo", { exact: false }).waitFor();
  },
);

When(
  "genera la recomendacion del dia si es necesario",
  async function (this: ScreenplayWorld) {
    await this.actor?.attemptsTo(new GenerateRecommendation());
  },
);

Then(
  "deberia ver recomendaciones del dia",
  async function (this: ScreenplayWorld) {
    const page = this.actor?.abilityTo(BrowseTheWeb).page;
    const button = page?.getByRole("button", { name: /Obtener mi recomend/i });
    await button?.waitFor({ state: "hidden" });
    const emptyVisible = await button?.isVisible();
    expect(emptyVisible).to.equal(false);
  },
);
