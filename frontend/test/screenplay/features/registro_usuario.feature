Feature: Registro de usuario

  Scenario: Registro exitoso
    Given el usuario esta en la pagina "registro"
    When registra un usuario nuevo
    Then deberia ver la pagina de login
