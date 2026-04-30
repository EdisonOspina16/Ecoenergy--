Feature: Mostrar estado
  Scenario: Ver y cambiar el estado del dispositivo
    Given el actor tiene una sesion activa
    And existen tomacorrientes registrados
    When cambia el estado del dispositivo con id 1 a encendido
    Then la respuesta es exitosa con codigo 200
    And el mensaje indica dispositivo encendido o apagado
