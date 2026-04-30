import type { Task } from "./task";
import type { Question } from "./question";

export type Ability = {
  readonly page?: unknown;
};

type AbilityCtor<T extends Ability> = new (...args: any[]) => T;

export class Actor {
  private abilities = new Map<Function, Ability>();

  private constructor(private readonly actorName: string) {}

  static named(name: string) {
    return new Actor(name);
  }

  whoCan(...abilities: Ability[]) {
    abilities.forEach((ability) => {
      this.abilities.set(ability.constructor, ability);
    });
    return this;
  }

  abilityTo<T extends Ability>(abilityType: AbilityCtor<T>): T {
    const ability = this.abilities.get(abilityType);
    if (!ability) {
      throw new Error(
        `Actor ${this.actorName} lacks ability ${abilityType.name}`,
      );
    }
    return ability as T;
  }

  async attemptsTo(...tasks: Task[]) {
    for (const task of tasks) {
      await task.performAs(this);
    }
  }

  async asks<T>(question: Question<T>): Promise<T> {
    return question.answeredBy(this);
  }
}
