from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import pytest

from app.main import app
from app.services.weather_service import WeatherService

client = TestClient(app)

@pytest.fixture
def mock_weather_data():
    return {
        "name": "São Paulo",
        "main": {
            "temp": 22.5,
            "feels_like": 23.1,
            "temp_min": 21.0,
            "temp_max": 24.2,
            "pressure": 1012,
            "humidity": 65
        },
        "weather": [
            {
                "description": "céu limpo"
            }
        ],
        "wind": {
            "speed": 3.6,
            "deg": 150
        }
    }

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

@patch.object(WeatherService, 'get_weather_data')
def test_criar_previsao(mock_get_weather, mock_weather_data):
    mock_get_weather.return_value = mock_weather_data
    
    response = client.post(
        "/previsao/",
        json={"cidade": "São Paulo"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["cidade"] == "São Paulo"
    assert data["temperatura"] == 22.5
    assert "id" in data
    
    mock_get_weather.assert_called_once_with("São Paulo")

def test_listar_previsoes():
    response = client.get("/previsao/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_filtrar_previsoes_por_cidade():
    response = client.get("/previsao/?cidade=São Paulo")
    assert response.status_code == 200
    
    for previsao in response.json():
        assert previsao["cidade"] == "São Paulo"