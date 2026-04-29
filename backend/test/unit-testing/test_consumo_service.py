import pytest
from unittest.mock import patch, MagicMock
from hamcrest import assert_that, is_, equal_to, has_length

from src.aplication.service.consumo_service import (
    _obtener_hogar,
    _construir_item_recomendacion,
    procesar_recomendacion,
    procesar_ahorro_estimado,
    obtener_recomendacion_diaria_hogar_por_usuario,
    generar_y_guardar_recomendacion_diaria
)

class TestConsumoService:
    # ---------------------------------------------------------
    # Test: _obtener_hogar
    # ---------------------------------------------------------
    @patch('src.aplication.service.consumo_service.obtener_conexion')
    @patch('src.aplication.service.consumo_service.UsuarioRepository')
    def test_obtener_hogar(self, mock_repo_class, mock_obtener_conexion):
        mock_conn = MagicMock()
        mock_obtener_conexion.return_value = mock_conn
        
        mock_repo_instance = MagicMock()
        mock_repo_instance.obtener_hogar_por_usuario.return_value = "Hogar_Dummy"
        mock_repo_class.return_value = mock_repo_instance
        
        # Act
        resultado = _obtener_hogar(1)
        
        # Assert
        mock_repo_class.assert_called_once_with(mock_conn)
        mock_repo_instance.obtener_hogar_por_usuario.assert_called_once_with(1)
        assert_that(resultado, is_(equal_to("Hogar_Dummy")))


    # ---------------------------------------------------------
    # Test: _construir_item_recomendacion & procesar_recomendacion
    # ---------------------------------------------------------
    @patch('src.aplication.service.consumo_service.llamar_recomendacion')
    def test_procesar_recomendacion_alerta(self, mock_llamar_recomendacion):
        mock_llamar_recomendacion.return_value = "Cuidado, hay un pico de consumo ⚠️"
        
        resultado = procesar_recomendacion(1500, "Aire Acondicionado")
        
        # Assert
        assert_that(resultado["recomendacion"], is_(equal_to("Cuidado, hay un pico de consumo ⚠️")))
        assert_that(resultado["esAlerta"], is_(True))
        assert_that(resultado["dispositivo"], is_(equal_to("Aire Acondicionado")))

    @patch('src.aplication.service.consumo_service.llamar_recomendacion')
    def test_procesar_recomendacion_normal(self, mock_llamar_recomendacion):
        mock_llamar_recomendacion.return_value = "Consumo estable, bien hecho."
        
        resultado = procesar_recomendacion(100, "TV")
        
        # Assert
        assert_that(resultado["esAlerta"], is_(False))


    # ---------------------------------------------------------
    # Test: procesar_ahorro_estimado
    # ---------------------------------------------------------
    @patch('src.aplication.service.consumo_service.obtener_dispositivos_con_ultimo_consumo')
    @patch('src.aplication.service.consumo_service.llamar_ahorro_estimado')
    def test_procesar_ahorro_estimado_exitoso(self, mock_llamar, mock_obtener_disp):
        mock_obtener_disp.return_value = [{"nombre": "Nevera", "consumo_watts": 400}]
        mock_llamar.return_value = {"ahorro": "1000 COP"}
        
        # Act
        res = procesar_ahorro_estimado()

        # Assert
        assert_that(res, is_(equal_to({"ahorro": "1000 COP"})))

    @patch('src.aplication.service.consumo_service.obtener_dispositivos_con_ultimo_consumo')
    def test_procesar_ahorro_estimado_error_sin_dispositivos(self, mock_obtener_disp):
        mock_obtener_disp.return_value = []
        with pytest.raises(ValueError, match="No hay dispositivos registrados"):
            procesar_ahorro_estimado()


    # ---------------------------------------------------------
    # Test: obtener_recomendacion_diaria_hogar_por_usuario
    # ---------------------------------------------------------
    @patch('src.aplication.service.consumo_service._obtener_hogar')
    def test_obtener_recomendacion_diaria_sin_hogar(self, mock_obtener_hogar):
        mock_obtener_hogar.return_value = None
        
        # Act
        res = obtener_recomendacion_diaria_hogar_por_usuario(1)

        # Assert
        assert_that(res["encontrado"], is_(False))

    @patch('src.aplication.service.consumo_service.obtener_recomendacion_diaria')
    @patch('src.aplication.service.consumo_service._obtener_hogar')
    def test_obtener_recomendacion_diaria_con_registro(self, mock_obtener_hogar, mock_obtener_rec):
        mock_hogar = MagicMock()
        mock_hogar.id_hogar = 10
        mock_obtener_hogar.return_value = mock_hogar
        mock_obtener_rec.return_value = {"datos": "existen"}
        
        # Act
        res = obtener_recomendacion_diaria_hogar_por_usuario(1)

        # Assert
        assert_that(res["encontrado"], is_(True))
        assert_that(res["datos"], is_(equal_to("existen")))

    @patch('src.aplication.service.consumo_service.obtener_recomendacion_diaria')
    @patch('src.aplication.service.consumo_service._obtener_hogar')
    def test_obtener_recomendacion_diaria_sin_registro(self, mock_obtener_hogar, mock_obtener_rec):
        mock_hogar = MagicMock()
        mock_hogar.id_hogar = 10
        mock_obtener_hogar.return_value = mock_hogar
        mock_obtener_rec.return_value = None
        
        # Act
        res = obtener_recomendacion_diaria_hogar_por_usuario(1)

        # Assert
        assert_that(res["encontrado"], is_(True))
        assert_that(res["recomendaciones"], is_(equal_to([])))


    # ---------------------------------------------------------
    # Test: generar_y_guardar_recomendacion_diaria
    # ---------------------------------------------------------
    @patch('src.aplication.service.consumo_service._obtener_hogar')
    def test_generar_y_guardar_sin_hogar(self, mock_obtener_hogar):
        mock_obtener_hogar.return_value = None
        with pytest.raises(ValueError, match="No tienes un hogar registrado"):
            generar_y_guardar_recomendacion_diaria(1)

    @patch('src.aplication.service.consumo_service._obtener_hogar')
    @patch('src.aplication.service.consumo_service.obtener_recomendacion_diaria')
    def test_generar_y_guardar_registro_ya_existe(self, mock_obtener_rec, mock_obtener_hogar):
        mock_hogar = MagicMock()
        mock_hogar.id_hogar = 10
        mock_obtener_hogar.return_value = mock_hogar
        mock_obtener_rec.return_value = {"ya_existe": True}
        
        # Act
        res = generar_y_guardar_recomendacion_diaria(1)

        # Assert
        assert_that(res["generada"], is_(True))
        assert_that(res["ya_existe"], is_(True))

    @patch('src.aplication.service.consumo_service._obtener_hogar')
    @patch('src.aplication.service.consumo_service.obtener_recomendacion_diaria')
    @patch('src.aplication.service.consumo_service.obtener_dispositivos_por_usuario')
    def test_generar_y_guardar_sin_dispositivos(self, mock_obtener_disp, mock_obtener_rec, mock_obtener_hogar):
        mock_hogar = MagicMock()
        mock_obtener_hogar.return_value = mock_hogar
        mock_obtener_rec.return_value = None
        mock_obtener_disp.return_value = []
        
        with pytest.raises(ValueError, match="No hay dispositivos registrados"):
            generar_y_guardar_recomendacion_diaria(1)

    @patch('src.aplication.service.consumo_service._obtener_hogar')
    @patch('src.aplication.service.consumo_service.obtener_recomendacion_diaria')
    @patch('src.aplication.service.consumo_service.obtener_dispositivos_por_usuario')
    @patch('src.aplication.service.consumo_service._construir_item_recomendacion')
    @patch('src.aplication.service.consumo_service.llamar_ahorro_estimado')
    @patch('src.aplication.service.consumo_service.guardar_recomendacion_diaria')
    def test_generar_y_guardar_exitoso(self, mock_guardar, mock_llamar_ahorro, mock_construir_item, mock_obtener_disp, mock_obtener_rec, mock_obtener_hogar):
        mock_hogar = MagicMock()
        mock_hogar.id_hogar = 10
        mock_obtener_hogar.return_value = mock_hogar
        mock_obtener_rec.return_value = None
        mock_obtener_disp.return_value = [{"nombre": "Ventilador", "consumo_watts": 50}]
        
        mock_construir_item.return_value = {"recomendacion": "Ok"}
        mock_llamar_ahorro.return_value = {
            "ahorro_financiero": "1000",
            "impacto_ambiental": "1kg",
            "indicador_didactico": "1 arbol"
        }
        
        # Act
        res = generar_y_guardar_recomendacion_diaria(1)

        # Assert
        assert_that(res["generada"], is_(True))
        assert_that(res["recomendaciones"], is_(equal_to([{"recomendacion": "Ok"}])))
        mock_guardar.assert_called_once()
