import { When, Then } from "@cucumber/cucumber";
import { expect } from "chai";
import { ScreenplayWorld } from "../support/world";
import { RegisterUser } from "../screenplay/tasks/registerUser";
import { uniqueEmail, uniquePassword } from "../support/env";
import { TextVisible } from "../screenplay/questions/textVisible";

When("registra un usuario nuevo", async function (this: ScreenplayWorld) {
  const email = uniqueEmail();
  const password = uniquePassword();
  this.data.email = email;
  this.data.password = password;

  await this.actor?.attemptsTo(
    RegisterUser.with(
      {
        nombre: "Usuario",
        apellidos: "Prueba",
        correo: email,
        contrasena: password,
      },
      this.baseUrl,
    ),
  );
});

Then("deberia ver la pagina de login", async function (this: ScreenplayWorld) {
  const visible = await this.actor?.asks(TextVisible.of(/INICIAR/i));
  expect(visible).to.equal(true);
});
