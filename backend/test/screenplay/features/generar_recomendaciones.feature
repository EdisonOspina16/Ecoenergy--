Feature: Generar recomendaciones de ahorro
  Como usuario del sistema quiero obtener recomendaciones de ahorro energetico personalizadas
  para optimizar el consumo de mis dispositivos

  Scenario: Generar recomendacion para un dispositivo con consumo dado
    Given el actor tiene una sesion activa
    When solicita recomendacion para el dispositivo "Nevera" con consumo de 150 watts
    Then la respuesta es exitosa con codigo 200
    And la respuesta contiene una recomendacion para el dispositivo "Nevera"

  Scenario: Solicitud de recomendacion sin datos del dispositivo
    Given el actor tiene una sesion activa
    When solicita recomendacion sin datos del dispositivo
    Then la respuesta falla con codigo 500
