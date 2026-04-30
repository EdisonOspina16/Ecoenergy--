Feature: Listar dispositivos
  Scenario: Listar dispositivos correctamente
    Given existen dispositivos registrados globales
    When lista los dispositivos
    Then la respuesta es exitosa con codigo 200
    And se listan al menos 1 dispositivos
