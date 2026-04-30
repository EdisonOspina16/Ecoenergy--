import type { Question } from "../question";
import { Actor } from "../actor";
import { BrowseTheWeb } from "../abilities/browseTheWeb";

export class TextVisible implements Question<boolean> {
  constructor(private readonly text: string | RegExp) {}

  static of(text: string | RegExp) {
    return new TextVisible(text);
  }

  async answeredBy(actor: Actor): Promise<boolean> {
    const page = actor.abilityTo(BrowseTheWeb).page;
    const locator =
      typeof this.text === "string"
        ? page.getByText(this.text, { exact: false })
        : page.getByText(this.text);

    await locator.first().waitFor();
    return locator.first().isVisible();
  }
}
