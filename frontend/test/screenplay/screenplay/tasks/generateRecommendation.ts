import type { Task } from "../task";
import { Actor } from "../actor";
import { BrowseTheWeb } from "../abilities/browseTheWeb";

export class GenerateRecommendation implements Task {
  async performAs(actor: Actor): Promise<void> {
    const page = actor.abilityTo(BrowseTheWeb).page;
    const button = page.getByRole("button", { name: /Obtener mi recomend/i });

    if (await button.count()) {
      await button.first().click();
      await button
        .first()
        .waitFor({ state: "hidden" })
        .catch(() => {});
    }
  }
}
