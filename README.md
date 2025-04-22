# Weather API

Este projeto é uma API REST para consulta e armazenamento de previsões do tempo utilizando a API OpenWeatherMap.

## Funcionalidades

- Buscar previsão do tempo e armazenar no banco de dados
- Listar todas as previsões armazenadas
- Buscar previsões filtrando por cidade e data
- Excluir uma previsão armazenada

## Stack

- Python 3.10+
- FastAPI
- SQLAlchemy
- SQLite
- OpenWeatherMap API
- pytest para testes

## Configuração do Ambiente

1. Clone este repositório:
```
git clone https://github.com/seu-usuario/weather-api.git
cd weather-api
```

2. Crie e ative um ambiente virtual:
```
python -m venv venv
# No Windows
venv\Scripts\activate
# No Linux/MacOS
source venv/bin/activate
```

3. Instale as dependências:
```
pip install -r requirements.txt
```

4. Crie um arquivo `.env` na raiz do projeto com sua chave da API OpenWeatherMap:
```
OPENWEATHERMAP_API_KEY=sua_chave_api
```

## Executando a Aplicação

Para iniciar o servidor:

```
uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`

## Documentação da API

A documentação interativa está disponível em:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints

### Buscar previsão do tempo e armazenar no banco

```
POST /previsao/
{
  "cidade": "São Paulo"
}
```

### Listar todas as previsões armazenadas

```
GET /previsao/
```

### Buscar previsões filtrando por cidade e data

```
GET /previsao?cidade=São Paulo&data=2023-11-20
```

### Excluir uma previsão armazenada

```
DELETE /previsao/{id}
```

## Executando os Testes

```
pytest
```

Para verificar a cobertura de testes:

```
pytest --cov=app tests/
```