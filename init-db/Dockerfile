FROM postgres:latest

# Orden explícito para evitar fallos por FK en migraciones.
COPY tablas.sql /docker-entrypoint-initdb.d/01_tablas.sql
COPY add_recomendacion_ahorro_diaria.sql /docker-entrypoint-initdb.d/02_add_recomendacion_ahorro_diaria.sql
