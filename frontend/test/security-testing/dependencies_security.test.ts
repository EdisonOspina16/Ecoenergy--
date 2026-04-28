import { execSync } from "child_process";
import { describe, it } from "vitest";
import { expect } from "chai";

describe("Frontend Security | Análisis de Dependencias (SCA)", () => {
  it("npm audit no debe encontrar vulnerabilidades críticas o altas en las dependencias", () => {
    try {
      // Ejecutamos npm audit para escanear las dependencias listadas en package.json.
      // Puedes ajustar el --audit-level a 'moderate', 'high' o 'critical' según tu política de seguridad.
      const stdout = execSync("npm audit --audit-level=high", { 
        encoding: "utf8",
        stdio: "pipe" 
      });
      
      // Si execSync no lanza una excepción, significa que el comando terminó con código 0
      // lo cual indica que no se encontraron vulnerabilidades en ese nivel o superior.
      expect(true).to.be.true;

    } catch (error: any) {
      // Si npm audit detecta vulnerabilidades, sale con un código de error > 0, lo que hace que execSync lance una excepción.
      const output = error.stdout || error.message;
      throw new Error(`¡npm audit encontró dependencias con vulnerabilidades de seguridad!\n\n${output}`);
    }
  });
});
