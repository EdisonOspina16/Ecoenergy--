Feature: Inicio de sesion y cierre de sesion

  Scenario: Iniciar sesion correctamente
    Given el usuario esta en la pagina "login"
    When inicia sesion con credenciales validas
    Then deberia ver el dashboard principal

  Scenario: Cerrar sesion desde dashboard
    Given el usuario inicia sesion y abre el dashboard
    When cierra sesion desde el dashboard
    Then deberia estar en la ruta "/login"
