Feature: Generar recomendaciones de ahorro

  Scenario: Generar recomendacion del dia
    Given el usuario inicia sesion y abre home
    When genera la recomendacion del dia si es necesario
    Then deberia ver recomendaciones del dia
