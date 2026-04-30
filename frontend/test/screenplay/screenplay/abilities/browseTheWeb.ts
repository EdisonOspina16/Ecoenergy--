import type { Page } from "playwright";
import type { Ability } from "../actor";

export class BrowseTheWeb implements Ability {
  static using(page: Page) {
    return new BrowseTheWeb(page);
  }

  constructor(public readonly page: Page) {}
}
