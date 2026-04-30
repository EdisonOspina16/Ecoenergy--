import type { Page } from "playwright";

const escapeCssString = (value: string) =>
  value.replace(/\\/g, "\\\\").replace(/"/g, '\\"');

export const inputWithValue = (page: Page, value: string) => {
  const escapedValue = escapeCssString(value);
  return page.locator(
    `input[value="${escapedValue}"], textarea:text-is("${escapedValue}")`,
  );
};
