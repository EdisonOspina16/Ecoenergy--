Feature: Crear perfil de hogar

  Scenario: Guardar perfil del hogar
    Given el usuario esta autenticado y en perfil
    When crea o actualiza el perfil del hogar
    Then deberia ver confirmacion del perfil
