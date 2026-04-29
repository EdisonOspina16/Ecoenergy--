Feature: Inicio de sesion
  Scenario: Login exitoso
    Given el actor tiene credenciales validas
    When inicia sesion con correo "usuario@ejemplo.com" y contrasena "ValidPass1!"
    Then la respuesta es exitosa con codigo 200
    And el correo del usuario en respuesta es "usuario@ejemplo.com"
