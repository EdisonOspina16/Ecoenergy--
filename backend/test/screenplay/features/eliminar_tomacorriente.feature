Feature: Eliminar tomacorriente
  Scenario: Eliminacion exitosa
    Given el actor tiene una sesion activa
    And existe el tomacorriente con id 1
    When elimina el tomacorriente con id 1
    Then la respuesta es exitosa con codigo 200
