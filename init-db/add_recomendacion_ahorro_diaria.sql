-- Migración: tabla recomendación y ahorro diario (una por hogar por día)
-- Ejecutar si la tabla no existe: psql -U usuario -d ecoenergy -f add_recomendacion_ahorro_diaria.sql

CREATE TABLE IF NOT EXISTS recomendacion_ahorro_diaria (
    id SERIAL PRIMARY KEY,
    id_hogar INT NOT NULL,
    fecha DATE NOT NULL,
    recomendaciones JSONB NOT NULL DEFAULT '[]',
    ahorro_financiero VARCHAR(255),
    impacto_ambiental VARCHAR(255),
    indicador_didactico VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_recomendacion_diaria_hogar FOREIGN KEY (id_hogar)
        REFERENCES hogares (id_hogar) ON DELETE CASCADE,
    CONSTRAINT uq_hogar_fecha UNIQUE (id_hogar, fecha)
);
