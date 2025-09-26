FROM eclipse-mosquitto:latest

# Copiar configuración personalizada
COPY config/mosquitto.conf /mosquitto/config/mosquitto.conf

# Exponer puertos
EXPOSE 1883 9001

# Comando por defecto
CMD ["/usr/sbin/mosquitto", "-c", "/mosquitto/config/mosquitto.conf"]