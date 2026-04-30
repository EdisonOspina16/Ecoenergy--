import type { Task } from "../task";
import { Actor } from "../actor";
import { BrowseTheWeb } from "../abilities/browseTheWeb";

export class LogoutFromDashboard implements Task {
  async performAs(actor: Actor): Promise<void> {
    const page = actor.abilityTo(BrowseTheWeb).page;

    await page.getByRole("button", { name: /Cerrar/i }).click();
    await page.waitForURL(/\/login$/);
  }
}
