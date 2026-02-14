# BASES DE DATOS - POSTGRESQL
import os

if os.getenv("DOCKER") == "1":
    PGHOST='db'
    PGDATABASE='ecoenergydb'
    PGUSER='ecoenergy'
    PGPASSWORD='ecoenergy123'
else:
    PGHOST='localhost'
    PGDATABASE='ecoenergy'
    PGUSER='postgres'
    PGPASSWORD='Edison#101'

EMAIL_CONFIG = {
    "HOST": "smtp.gmail.com",
    "PORT": 587,
    "USER": "ecoenergy.subscription@gmail.com",
    "PASSWORD": "gitygifbieuuhkow"
}

# GEMINI - LLM
GEMINI_API_KEY = "AIzaSyBM7PJOFT6G57Mr4jAcD_gAio7EPUESHGc"
GEMINI_MODEL = "gemini-2.0-flash"
PROMT_BASE =  """
Eres un asistente energético inteligente. Analiza el consumo de los dispositivos eléctricos.
Usa un lenguaje claro y breve para dar recomendaciones o alertas.
"""


