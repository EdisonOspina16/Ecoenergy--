// frontend/config.ts
const DEFAULT_PROD = "http://backend-service:5000";
const DEFAULT_DEV = "http://localhost:5000";

export const API_URL = (() => {
  // Si estamos en el navegador (cliente)
  if (typeof window !== "undefined") {
    // En desarrollo local (npm run dev)
    if (process.env.NODE_ENV === "development") {
      return process.env.NEXT_PUBLIC_API_URL || DEFAULT_DEV;
    }
    // En producción
    return process.env.NEXT_PUBLIC_API_URL || DEFAULT_PROD;
  }

  // Si estamos en el servidor (build time)
  return process.env.NEXT_PUBLIC_API_URL || DEFAULT_PROD;
})();