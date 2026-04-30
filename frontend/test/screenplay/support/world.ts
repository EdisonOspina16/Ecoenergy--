import { setWorldConstructor, World, IWorldOptions } from "@cucumber/cucumber";
import type { Browser, BrowserContext, Page } from "playwright";
import { Actor } from "../screenplay/actor";
import { BrowseTheWeb } from "../screenplay/abilities/browseTheWeb";
import { getBaseUrl, getCredentials } from "./env";

export type ScenarioData = {
  email?: string;
  password?: string;
  deviceId?: string;
  deviceName?: string;
  homeName?: string;
  address?: string;
};

export class ScreenplayWorld extends World {
  baseUrl: string;
  credentials = getCredentials();
  data: ScenarioData = {};
  browser?: Browser;
  context?: BrowserContext;
  page?: Page;
  actor?: Actor;

  constructor(options: IWorldOptions) {
    super(options);
    this.baseUrl = getBaseUrl();
  }

  attachActor(page: Page) {
    this.page = page;
    this.actor = Actor.named("Usuario").whoCan(BrowseTheWeb.using(page));
  }
}

setWorldConstructor(ScreenplayWorld);
