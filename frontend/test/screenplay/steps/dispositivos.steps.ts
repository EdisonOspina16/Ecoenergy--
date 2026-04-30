import { When, Then } from "@cucumber/cucumber";
import { expect } from "chai";
import { ScreenplayWorld } from "../support/world";
import { RegisterDevice } from "../screenplay/tasks/registerDevice";
import { ToggleDevice } from "../screenplay/tasks/toggleDevice";
import { DeleteDevice } from "../screenplay/tasks/deleteDevice";
import { InputValueVisible } from "../screenplay/questions/inputValueVisible";
import { DeviceStatus } from "../screenplay/questions/deviceStatus";
import { TextVisible } from "../screenplay/questions/textVisible";
import { BrowseTheWeb } from "../screenplay/abilities/browseTheWeb";
import { inputWithValue } from "../screenplay/locators/displayValue";
import { uniqueDeviceId, uniqueDeviceName } from "../support/env";

When("registra un tomacorriente nuevo", async function (this: ScreenplayWorld) {
  const deviceId = uniqueDeviceId();
  const deviceName = uniqueDeviceName();
  this.data.deviceId = deviceId;
  this.data.deviceName = deviceName;

  await this.actor?.attemptsTo(RegisterDevice.with(deviceId, deviceName));
  const page = this.actor?.abilityTo(BrowseTheWeb).page;
  await page?.getByText(/Dispositivo registrado/i).waitFor();
});

Then(
  "deberia ver el tomacorriente en la lista",
  async function (this: ScreenplayWorld) {
    const deviceName = this.data.deviceName ?? "";
    const page = this.actor?.abilityTo(BrowseTheWeb).page;
    if (page) {
      await inputWithValue(page, deviceName).waitFor();
    }
    const visible = await this.actor?.asks(InputValueVisible.of(deviceName));
    expect(visible).to.equal(true);
  },
);

Then(
  "el dispositivo muestra estado valido",
  async function (this: ScreenplayWorld) {
    const deviceName = this.data.deviceName ?? "";
    const status = await this.actor?.asks(DeviceStatus.forDevice(deviceName));
    expect(["Conectado", "Desconectado"]).to.include(status);
  },
);

When(
  "cambia el estado del dispositivo",
  async function (this: ScreenplayWorld) {
    const deviceName = this.data.deviceName ?? "";
    await this.actor?.attemptsTo(ToggleDevice.named(deviceName));
  },
);

Then(
  "el dispositivo aparece como conectado",
  async function (this: ScreenplayWorld) {
    const deviceName = this.data.deviceName ?? "";
    const status = await this.actor?.asks(DeviceStatus.forDevice(deviceName));
    expect(status).to.equal("Conectado");
  },
);

Then("existen dispositivos conectados", async function (this: ScreenplayWorld) {
  const visible = await this.actor?.asks(TextVisible.of(/Conectado/i));
  expect(visible).to.equal(true);
});

When("elimina el tomacorriente", async function (this: ScreenplayWorld) {
  const deviceName = this.data.deviceName ?? "";
  await this.actor?.attemptsTo(DeleteDevice.named(deviceName));
});

Then(
  "el tomacorriente ya no aparece en la lista",
  async function (this: ScreenplayWorld) {
    const deviceName = this.data.deviceName ?? "";
    const page = this.actor?.abilityTo(BrowseTheWeb).page;
    if (page) {
      await inputWithValue(page, deviceName).waitFor({ state: "detached" });
    }
    const visible = await this.actor?.asks(InputValueVisible.of(deviceName));
    expect(visible).to.equal(false);
  },
);
