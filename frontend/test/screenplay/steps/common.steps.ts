import { Given, Then } from "@cucumber/cucumber";
import { expect } from "chai";
import { ScreenplayWorld } from "../support/world";
import { OpenPage } from "../screenplay/tasks/openPage";
import { CurrentPath } from "../screenplay/questions/currentPath";
import { TextVisible } from "../screenplay/questions/textVisible";

Given(
  "el usuario esta en la pagina {string}",
  async function (this: ScreenplayWorld, path: string) {
    await this.actor?.attemptsTo(OpenPage.at(path, this.baseUrl));
  },
);

Then(
  "deberia estar en la ruta {string}",
  async function (this: ScreenplayWorld, path: string) {
    const current = await this.actor?.asks(new CurrentPath());
    expect(current).to.equal(path);
  },
);

Then(
  "deberia ver el texto {string}",
  async function (this: ScreenplayWorld, text: string) {
    const visible = await this.actor?.asks(TextVisible.of(text));
    expect(visible).to.equal(true);
  },
);
