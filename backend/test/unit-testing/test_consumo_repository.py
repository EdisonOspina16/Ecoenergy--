import pytest
import json
from unittest.mock import patch, MagicMock

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
        
        resultado = obtener_dispositivos_con_ultimo_consumo()
        
        assert len(resultado) == 2
        assert resultado[0]["nombre"] == "Nevera"
        assert resultado[0]["consumo_watts"] == pytest.approx(150.5)
        assert resultado[1]["nombre"] == "Aire"
        assert resultado[1]["consumo_watts"] == pytest.approx(0.0)

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
        
        resultado = obtener_dispositivos_por_usuario(1)
        assert len(resultado) == 1
        assert resultado[0]["nombre"] == "TV"
        assert resultado[0]["consumo_watts"] == pytest.approx(100.0)

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
        
        assert obtener_recomendacion_diaria(10) is None

    @patch('src.repositories.consumo_repository.obtener_conexion')
    def test_obtener_recomendacion_diaria_con_registro_json_str(self, mock_obtener_conexion):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_obtener_conexion.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Simula: (recomendaciones_str, ahorro, impacto, indicador)
        json_str = json.dumps([{"rec": "Haz algo"}])
        mock_cursor.fetchone.return_value = (json_str, "5000", "2kg", "1 auto")
        
        resultado = obtener_recomendacion_diaria(10)
        
        assert resultado["recomendaciones"][0]["rec"] == "Haz algo"
        assert resultado["ahorro_financiero"] == "5000"

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
        
        guardar_recomendacion_diaria(10, [{"rec": "Test"}], {"ahorro_financiero": "500 COP"})
        
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
