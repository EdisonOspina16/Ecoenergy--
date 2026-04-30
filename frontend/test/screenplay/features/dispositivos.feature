Feature: Gestion de dispositivos del hogar

  Background:
    Given el usuario esta autenticado y en perfil

  Scenario: Registrar tomacorriente
    When registra un tomacorriente nuevo
    Then deberia ver el tomacorriente en la lista

  Scenario: Listar tomacorrientes del hogar
    When registra un tomacorriente nuevo
    Then deberia ver el tomacorriente en la lista

  Scenario: Mostrar estado de dispositivo
    When registra un tomacorriente nuevo
    Then el dispositivo muestra estado valido

  Scenario: Listar dispositivos conectados
    When registra un tomacorriente nuevo
    And cambia el estado del dispositivo
    Then el dispositivo aparece como conectado
    And existen dispositivos conectados

  Scenario: Eliminar dispositivo del hogar
    When registra un tomacorriente nuevo
    And elimina el tomacorriente
    Then el tomacorriente ya no aparece en la lista
