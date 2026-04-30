import type { Question } from "../question";
import { Actor } from "../actor";
import { BrowseTheWeb } from "../abilities/browseTheWeb";

export class CurrentPath implements Question<string> {
  async answeredBy(actor: Actor): Promise<string> {
    const page = actor.abilityTo(BrowseTheWeb).page;
    return new URL(page.url()).pathname;
  }
}
