Feature: Cierre de sesion
  Scenario: Logout exitoso
    Given el actor tiene una sesion activa
    When cierra sesion
    Then la respuesta es exitosa con codigo 200
