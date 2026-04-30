export type Credentials = {
  email: string;
  password: string;
};

export const getBaseUrl = (): string =>
  process.env.E2E_BASE_URL ?? "http://localhost:3000";

export const getCredentials = (): Credentials => ({
  email: process.env.E2E_EMAIL ?? "tomasra@gmail.com",
  password: process.env.E2E_PASSWORD ?? "Contrasena123.",
});

export const getBrowserName = (): string =>
  (process.env.E2E_BROWSER ?? "chromium").toLowerCase();

export const isHeadless = (): boolean => process.env.HEADLESS !== "false";

export const buildUrl = (baseUrl: string, pathOrUrl: string): string => {
  if (pathOrUrl.startsWith("http://") || pathOrUrl.startsWith("https://")) {
    return pathOrUrl;
  }
  const path = pathOrUrl.startsWith("/") ? pathOrUrl : `/${pathOrUrl}`;
  return `${baseUrl}${path}`;
};

export const uniqueEmail = (): string => {
  const stamp = Date.now().toString(36);
  const rand = Math.floor(Math.random() * 10000).toString(36);
  return `e2e_${stamp}_${rand}@example.com`;
};

export const uniquePassword = (): string => `Pass${Date.now().toString(36)}A1!`;

export const uniqueDeviceId = (): string =>
  `TOM${Date.now().toString().slice(-6)}`;

export const uniqueDeviceName = (): string =>
  `Tomacorriente-${Date.now().toString().slice(-4)}`;

export const uniqueHomeName = (): string =>
  `Hogar-${Date.now().toString().slice(-4)}`;

export const uniqueAddress = (): string => {
  const street = Math.floor(Math.random() * 80) + 1;
  const num1 = Math.floor(Math.random() * 50) + 1;
  const num2 = Math.floor(Math.random() * 90) + 1;
  return `Calle ${street} #${num1}-${num2}`;
};
