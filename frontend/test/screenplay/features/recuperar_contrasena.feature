Feature: Cambiar contrasena

  Scenario: Cambio de contrasena exitoso
    Given existe un usuario registrado
    When solicita cambio de contrasena
    Then deberia ver confirmacion de contrasena
