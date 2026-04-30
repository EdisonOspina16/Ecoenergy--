Feature: Cambiar contraseña
  Scenario: Cambio de contraseña exitoso
    Given el usuario esta registrado con correo "usuario@ejemplo.com"
    When intenta recuperar contrasena con correo "usuario@ejemplo.com" y nueva contrasena "NuevaPass123!"
    Then la respuesta es exitosa con codigo 200
    And el mensaje de respuesta indica contrasena actualizada
