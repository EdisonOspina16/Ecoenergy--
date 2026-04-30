Feature: Suscripcion a correo
  Scenario: Suscribirse con un correo valido
    Given el sistema de correos esta disponible
    When el usuario se suscribe con el correo "newsletter@ejemplo.com"
    Then la respuesta es exitosa con codigo 200
    And el mensaje indica correo enviado correctamente
