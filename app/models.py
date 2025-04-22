from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .database import Base

class Previsao(Base):
    __tablename__ = "previsoes"

    id = Column(Integer, primary_key=True, index=True)
    cidade = Column(String, index=True)
    temperatura = Column(Float)
    sensacao_termica = Column(Float)
    temperatura_min = Column(Float)
    temperatura_max = Column(Float)
    pressao = Column(Integer)
    umidade = Column(Integer)
    descricao = Column(String)
    velocidade_vento = Column(Float)
    direcao_vento = Column(Integer)
    data_consulta = Column(DateTime, default=datetime.now)