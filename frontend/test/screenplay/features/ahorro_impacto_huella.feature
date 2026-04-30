Feature: Ahorro, impacto ambiental y huella

  Scenario: Mostrar ahorro economico e impacto ambiental
    Given el usuario inicia sesion y abre home
    Then deberia ver la tarjeta de ahorro financiero
    And deberia ver la tarjeta de impacto ambiental
    And deberia ver la tarjeta de indicador didactico
