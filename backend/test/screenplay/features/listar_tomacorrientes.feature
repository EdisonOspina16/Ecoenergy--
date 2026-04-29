Feature: Listar tomacorrientes
  Scenario: Listado exitoso
    Given el actor tiene una sesion activa
    And existen tomacorrientes registrados
    When lista tomacorrientes
    Then la respuesta es exitosa con codigo 200
    And se listan 2 tomacorrientes
