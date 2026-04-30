Feature: Crear perfil de hogar
  Scenario: Creacion exitosa de perfil de hogar
    Given el actor tiene una sesion activa
    When guarda su perfil de hogar con direccion "Calle 123" y nombre "Mi Casa Inteligente"
    Then la respuesta es exitosa con codigo 200
    And la respuesta indica perfil creado o actualizado
