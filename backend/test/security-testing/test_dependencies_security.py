import subprocess
import pytest
import sys

@pytest.mark.security
def test_dependencies_security_scan():
    """
    Prueba de seguridad de dependencias (SCA) usando pip-audit.
    Escanea el archivo requirements.txt contrastándolo contra una base de datos global 
    de CVEs (Common Vulnerabilities and Exposures) para asegurar que ninguna librería 
    tenga brechas de seguridad públicas.
    """
    import os
    # Ejecutamos pip-audit para revisar el requirements.txt
    comando = [sys.executable, "-m", "pip_audit", "-r", "requirements.txt"]
    
    # Prevenimos el error 'charmap' de Windows forzando utf-8
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    
    resultado = subprocess.run(comando, capture_output=True, text=True, env=env)
    
    # Si returncode es distinto de 0, pip-audit encontró dependencias vulnerables
    mensaje_error = f"¡pip-audit encontró dependencias con vulnerabilidades conocidas (CVEs)!\n\n{resultado.stdout}"
    
    # NOTA: En proyectos reales a veces esto falla por librerías antiguas. 
    # El assert obliga a actualizar las versiones en el requirements.txt
    assert resultado.returncode == 0, mensaje_error
