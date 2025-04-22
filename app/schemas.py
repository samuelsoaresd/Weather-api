from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PrevisaoBase(BaseModel):
    cidade: str

class PrevisaoCreate(PrevisaoBase):
    pass

class PrevisaoResponse(PrevisaoBase):
    id: int
    temperatura: float
    sensacao_termica: float
    temperatura_min: float
    temperatura_max: float
    pressao: int
    umidade: int
    descricao: str
    velocidade_vento: float
    direcao_vento: int
    data_consulta: datetime

    class Config:
        orm_mode = True