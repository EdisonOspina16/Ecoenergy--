# BASES DE DATOS - POSTGRESQL
import os

if os.getenv("DOCKER") == "1":
    PGHOST='db'
    PGDATABASE='ecoenergydb'
    PGUSER='ecoenergy'
    PGPASSWORD='ecoenergy123'
else:
    PGHOST='ep-sparkling-bar-aigb3jxq-pooler.c-4.us-east-1.aws.neon.tech'
    PGDATABASE='neondb'
    PGUSER='neondb_owner'
    PGPASSWORD='npg_jMz0EQcP2aHA'

EMAIL_CONFIG = {
    "HOST": "smtp.gmail.com",
    "PORT": 587,
    "USER": "ecoenergy.subscription@gmail.com",
    "PASSWORD": "gitygifbieuuhkow"
}

# GEMINI - LLM
GEMINI_API_KEY = "Uy blanquita"
GEMINI_MODEL = "gemini-3-flash-preview"
PROMT_BASE =  """
Eres un asistente energético inteligente. Analiza el consumo de los dispositivos eléctricos.
Usa un lenguaje claro y breve para dar recomendaciones o alertas.
"""


