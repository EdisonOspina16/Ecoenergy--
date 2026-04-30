import { Before, After, setDefaultTimeout } from "@cucumber/cucumber";
import { chromium, firefox, webkit } from "playwright";
import { ScreenplayWorld } from "./world";
import { getBrowserName, isHeadless } from "./env";

const resolveBrowser = (name: string) => {
  switch (name) {
    case "firefox":
      return firefox;
    case "webkit":
      return webkit;
    default:
      return chromium;
  }
};

setDefaultTimeout(60000);

Before(async function (this: ScreenplayWorld) {
  const browserType = resolveBrowser(getBrowserName());
  this.browser = await browserType.launch({ headless: isHeadless() });
  this.context = await this.browser.newContext();
  const page = await this.context.newPage();
  this.attachActor(page);
});

After(async function (this: ScreenplayWorld) {
  await this.context?.close();
  await this.browser?.close();
});
