import requests
import os
from dotenv import load_dotenv
from typing import Dict, Any, Optional

load_dotenv()

class WeatherService:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHERMAP_API_KEY", "sua_chave_api")
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        
    def get_weather_data(self, cidade: str) -> Dict[str, Any]: # Busca dados de previsão do tempo para uma cidade específica
        params = {
            'q': cidade,
            'appid': self.api_key,
            'units': 'metric',
            'lang': 'pt_br'     
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()  # Levanta exceção para códigos de erro HTTP
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Erro ao buscar previsão do tempo: {str(e)}")
    
    def parse_weather_data(self, data: Dict[str, Any]) -> Dict[str, Any]: #Parsing dos dados da API para o formato que será armazenado no banco
        try:
            return {
                "cidade": data["name"],
                "temperatura": data["main"]["temp"],
                "sensacao_termica": data["main"]["feels_like"],
                "temperatura_min": data["main"]["temp_min"],
                "temperatura_max": data["main"]["temp_max"],
                "pressao": data["main"]["pressure"],
                "umidade": data["main"]["humidity"],
                "descricao": data["weather"][0]["description"],
                "velocidade_vento": data["wind"]["speed"],
                "direcao_vento": data["wind"]["deg"]
            }
        except KeyError as e:
            raise Exception(f"Erro ao processar dados da previsão: {str(e)}")