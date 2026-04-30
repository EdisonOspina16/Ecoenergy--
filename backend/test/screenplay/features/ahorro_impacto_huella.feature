Feature: Calcular ahorro economico impacto ambiental y huella de carbono
  Como usuario del sistema quiero calcular el ahorro economico estimado
  el impacto ambiental y la huella de carbono para tomar decisiones
  informadas sobre el uso de energia en mi hogar

  Scenario: Generar recomendacion diaria con ahorro impacto ambiental y huella de carbono exitosamente
    Given el actor tiene una sesion activa
    And existen dispositivos con consumo registrado para el usuario
    And la IA genera datos de ahorro estimado con impacto ambiental y huella de carbono
    When genera la recomendacion diaria del hogar
    Then la respuesta es exitosa con codigo 200
    And la respuesta contiene el campo "ahorro_financiero"
    And la respuesta contiene el campo "impacto_ambiental"
    And la respuesta contiene el campo "indicador_didactico"

  Scenario: Obtener recomendacion diaria ya existente
    Given el actor tiene una sesion activa
    And existe una recomendacion diaria guardada para el hogar del usuario
    When consulta la recomendacion diaria del hogar
    Then la respuesta es exitosa con codigo 200
    And la recomendacion diaria fue encontrada

  Scenario: Calcular ahorro estimado global con todos los dispositivos
    Given existen dispositivos globales con consumo registrado
    And la IA genera datos de ahorro estimado con impacto ambiental y huella de carbono
    When consulta el ahorro estimado global
    Then la respuesta es exitosa con codigo 200
    And el resultado de ahorro contiene "ahorro_financiero"
