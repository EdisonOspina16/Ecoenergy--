Feature: Registro de usuario
  Como usuario nuevo quiero registrarme en el sistema
  para poder acceder a las funcionalidades de EcoEnergy

  Scenario: Registro exitoso de un nuevo usuario
    Given el usuario no esta registrado en el sistema
    When registra una cuenta con nombre "Carlos" apellidos "Gomez" correo "carlos@eco.com" y contrasena "Segura123!"
    Then la respuesta es exitosa con codigo 200
    And el mensaje de respuesta indica registro exitoso

  Scenario: Registro fallido por campos faltantes
    Given el usuario no esta registrado en el sistema
    When intenta registrarse sin proporcionar todos los campos requeridos
    Then la respuesta falla con codigo 400
