import subprocess
import pytest
import sys

@pytest.mark.security
def test_bandit_security_scan():
    """
    Prueba de seguridad estática (SAST) usando Bandit.
    Escanea el código fuente de la carpeta 'src' para encontrar malas prácticas
    de seguridad (inyección SQL, contraseñas hardcodeadas, uso de criptografía débil, etc).
    """
    # Ejecutamos bandit como un subproceso
    # -r: escaneo recursivo en la carpeta src/
    # -ll: solo fallar si hay vulnerabilidades de severidad Media o Alta
    # -ii: solo fallar si hay confianza Media o Alta en el hallazgo
    comando = [sys.executable, "-m", "bandit", "-r", "src/", "-ll", "-ii"]
    
    resultado = subprocess.run(comando, capture_output=True, text=True)
    
    # Si returncode es distinto de 0, Bandit encontró problemas de seguridad
    mensaje_error = f"¡Bandit encontró vulnerabilidades de seguridad en el código!\n\n{resultado.stdout}"
    assert resultado.returncode == 0, mensaje_error
