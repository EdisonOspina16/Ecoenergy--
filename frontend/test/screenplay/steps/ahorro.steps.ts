import { Then } from "@cucumber/cucumber";
import { expect } from "chai";
import { ScreenplayWorld } from "../support/world";
import { TextVisible } from "../screenplay/questions/textVisible";

Then(
  "deberia ver la tarjeta de ahorro financiero",
  async function (this: ScreenplayWorld) {
    const visible = await this.actor?.asks(
      TextVisible.of("Ahorro Financiero Proyectado"),
    );
    expect(visible).to.equal(true);
  },
);

Then(
  "deberia ver la tarjeta de impacto ambiental",
  async function (this: ScreenplayWorld) {
    const visible = await this.actor?.asks(TextVisible.of("Impacto Ambiental"));
    expect(visible).to.equal(true);
  },
);

Then(
  "deberia ver la tarjeta de indicador didactico",
  async function (this: ScreenplayWorld) {
    const visible = await this.actor?.asks(TextVisible.of(/Indicador/i));
    expect(visible).to.equal(true);
  },
);
