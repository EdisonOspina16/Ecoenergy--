Feature: Registro de tomacorriente
  Scenario: Registro exitoso
    Given el actor tiene una sesion activa
    And el hogar existe y el dispositivo no esta registrado
    When registra tomacorriente con id "TOM001" y apodo "Nevera"
    Then la respuesta es exitosa con codigo 201
    And el tomacorriente registrado tiene apodo "Nevera"
