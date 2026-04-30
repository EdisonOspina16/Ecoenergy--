import { Given, When, Then } from "@cucumber/cucumber";
import { expect } from "chai";
import { ScreenplayWorld } from "../support/world";
import { Login } from "../screenplay/tasks/login";
import { OpenPage } from "../screenplay/tasks/openPage";
import { LogoutFromDashboard } from "../screenplay/tasks/logout";
import { BrowseTheWeb } from "../screenplay/abilities/browseTheWeb";

When(
  "inicia sesion con credenciales validas",
  async function (this: ScreenplayWorld) {
    const { email, password } = this.credentials;
    await this.actor?.attemptsTo(Login.with(email, password, this.baseUrl));
  },
);

Given(
  "el usuario inicia sesion y abre el dashboard",
  async function (this: ScreenplayWorld) {
    const { email, password } = this.credentials;
    await this.actor?.attemptsTo(Login.with(email, password, this.baseUrl));
    await this.actor?.attemptsTo(OpenPage.at("/dashboard", this.baseUrl));
  },
);

When(
  "cierra sesion desde el dashboard",
  async function (this: ScreenplayWorld) {
    await this.actor?.attemptsTo(new LogoutFromDashboard());
  },
);

Then(
  "deberia ver el dashboard principal",
  async function (this: ScreenplayWorld) {
    const page = this.actor?.abilityTo(BrowseTheWeb).page;
    const homeLocator = page?.getByText("Resumen de Consumo", { exact: false });
    const dashboardLocator = page?.getByText(/DASHBOARD/i);

    const waits = [homeLocator?.waitFor(), dashboardLocator?.waitFor()].filter(
      (waiter): waiter is Promise<void> => Boolean(waiter),
    );

    await Promise.race(waits);

    const hasHome = await homeLocator?.isVisible();
    const hasDashboard = await dashboardLocator?.isVisible();
    expect(Boolean(hasHome || hasDashboard)).to.equal(true);
  },
);
