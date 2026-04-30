import type { Question } from "../question";
import { Actor } from "../actor";
import { BrowseTheWeb } from "../abilities/browseTheWeb";
import { inputWithValue } from "../locators/displayValue";

export class InputValueVisible implements Question<boolean> {
  constructor(private readonly value: string) {}

  static of(value: string) {
    return new InputValueVisible(value);
  }

  async answeredBy(actor: Actor): Promise<boolean> {
    const page = actor.abilityTo(BrowseTheWeb).page;
    return inputWithValue(page, this.value).isVisible();
  }
}
