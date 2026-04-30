import type { Task } from "../task";
import { Actor } from "../actor";
import { BrowseTheWeb } from "../abilities/browseTheWeb";
import { buildUrl } from "../../support/env";

export class OpenPage implements Task {
  constructor(
    private readonly baseUrl: string,
    private readonly path: string,
  ) {}

  static at(path: string, baseUrl: string) {
    return new OpenPage(baseUrl, path);
  }

  async performAs(actor: Actor): Promise<void> {
    const page = actor.abilityTo(BrowseTheWeb).page;
    await page.goto(buildUrl(this.baseUrl, this.path));
  }
}
