import pytest
import json
from unittest.mock import patch, MagicMock
from hamcrest import assert_that, is_, equal_to, has_length, close_to, none, not_none

from src.repositories.consumo_repository import (
    obtener_dispositivos_con_ultimo_consumo,
    obtener_dispositivos_por_usuario,
    obtener_recomendacion_diaria,
    guardar_recomendacion_diaria
)
from src.domain.errors import ConexionError


class TestConsumoRepository:

    # ---------------------------------------------------------
    # Test: obtener_dispositivos_con_ultimo_consumo
    # ---------------------------------------------------------
    @patch('src.repositories.consumo_repository.obtener_conexion')
    def test_obtener_dispositivos_con_ultimo_consumo_exitoso(self, mock_obtener_conexion):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_obtener_conexion.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Simula return de fetchall: (alias, watts, estado_activo, tipo_dispositivo_ia)
        mock_cursor.fetchall.return_value = [
            ("Nevera", 150.5, True, None),
            (None, None, True, "Aire")
        ]
        
        # Act
        resultado = obtener_dispositivos_con_ultimo_consumo()
        
        # Assert
        assert_that(resultado, has_length(2))
        assert_that(resultado[0]["nombre"], is_(equal_to("Nevera")))
        assert_that(resultado[0]["consumo_watts"], is_(close_to(150.5, 0.001)))
        assert_that(resultado[1]["nombre"], is_(equal_to("Aire")))
        assert_that(resultado[1]["consumo_watts"], is_(close_to(0.0, 0.001)))

    # ---------------------------------------------------------
    # Test: obtener_dispositivos_por_usuario
    # ---------------------------------------------------------
    @patch('src.repositories.consumo_repository.obtener_conexion')
    def test_obtener_dispositivos_por_usuario_error_conn(self, mock_obtener_conexion):
        mock_obtener_conexion.return_value = None
        with pytest.raises(ConexionError, match="No se pudo establecer conexión"):
            obtener_dispositivos_por_usuario(1)

    @patch('src.repositories.consumo_repository.obtener_conexion')
    def test_obtener_dispositivos_por_usuario_exitoso(self, mock_obtener_conexion):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_obtener_conexion.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        mock_cursor.fetchall.return_value = [
            ("TV", 100.0)
        ]
        
        # Act
        resultado = obtener_dispositivos_por_usuario(1)

        # Assert
        assert_that(resultado, has_length(1))
        assert_that(resultado[0]["nombre"], is_(equal_to("TV")))
        assert_that(resultado[0]["consumo_watts"], is_(close_to(100.0, 0.001)))

    # ---------------------------------------------------------
    # Test: obtener_recomendacion_diaria
    # ---------------------------------------------------------
    @patch('src.repositories.consumo_repository.obtener_conexion')
    def test_obtener_recomendacion_diaria_error_conn(self, mock_obtener_conexion):
        mock_obtener_conexion.return_value = None
        with pytest.raises(ConexionError):
            obtener_recomendacion_diaria(10)

    @patch('src.repositories.consumo_repository.obtener_conexion')
    def test_obtener_recomendacion_diaria_sin_registro(self, mock_obtener_conexion):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_obtener_conexion.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        mock_cursor.fetchone.return_value = None
        
        # Act
        resultado = obtener_recomendacion_diaria(10)

        # Assert
        assert_that(resultado, is_(none()))

    @patch('src.repositories.consumo_repository.obtener_conexion')
    def test_obtener_recomendacion_diaria_con_registro_json_str(self, mock_obtener_conexion):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_obtener_conexion.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Simula: (recomendaciones_str, ahorro, impacto, indicador)
        json_str = json.dumps([{"rec": "Haz algo"}])
        mock_cursor.fetchone.return_value = (json_str, "5000", "2kg", "1 auto")
        
        # Act
        resultado = obtener_recomendacion_diaria(10)
        
        # Assert
        assert_that(resultado["recomendaciones"][0]["rec"], is_(equal_to("Haz algo")))
        assert_that(resultado["ahorro_financiero"], is_(equal_to("5000")))

    # ---------------------------------------------------------
    # Test: guardar_recomendacion_diaria
    # ---------------------------------------------------------
    @patch('src.repositories.consumo_repository.obtener_conexion')
    def test_guardar_recomendacion_diaria_error_conn(self, mock_obtener_conexion):
        mock_obtener_conexion.return_value = None
        with pytest.raises(ConexionError):
            guardar_recomendacion_diaria(10, [], {})

    @patch('src.repositories.consumo_repository.obtener_conexion')
    def test_guardar_recomendacion_diaria_exitoso(self, mock_obtener_conexion):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_obtener_conexion.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Act
        guardar_recomendacion_diaria(10, [{"rec": "Test"}], {"ahorro_financiero": "500 COP"})
        
        # Assert
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
