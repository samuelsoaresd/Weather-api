from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import logging

from .. import models, schemas, database
from ..services.weather_service import WeatherService

router = APIRouter(
    prefix="/previsao",
    tags=["previsao"],
)

weather_service = WeatherService()

DATE_FORMAT = "%Y-%m-%d"

@router.post("/", response_model=schemas.PrevisaoResponse)
def criar_previsao(
    previsao: schemas.PrevisaoCreate, 
    db: Session = Depends(database.get_db)
):
    try:
        # Busca dados da API externa
        weather_data = weather_service.get_weather_data(previsao.cidade)
        parsed_data = weather_service.parse_weather_data(weather_data)
        
        # Cria registro no banco de dados
        db_previsao = models.Previsao(**parsed_data)
        db.add(db_previsao)
        db.commit()
        db.refresh(db_previsao)
        
        return db_previsao
    except Exception as e:
        logging.error(f"Erro ao criar previsão: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[schemas.PrevisaoResponse])
def listar_previsoes(
    cidade: Optional[str] = None,
    data: Optional[str] = None,
    db: Session = Depends(database.get_db)
):
    query = db.query(models.Previsao)
    
    # Filtro por cidade
    if cidade:
        query = query.filter(models.Previsao.cidade == cidade)
    
    # Filtro por data
    if data:
        try:
            data_obj = datetime.strptime(data, DATE_FORMAT)
            # Filtra registros do mesmo dia (ignorando hora)
            query = query.filter(
                models.Previsao.data_consulta >= data_obj.replace(hour=0, minute=0, second=0),
                models.Previsao.data_consulta < data_obj.replace(hour=23, minute=59, second=59)
            )
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de data inválido. Use YYYY-MM-DD")
    
    return query.all()

@router.delete("/{previsao_id}", status_code=204)
def deletar_previsao(previsao_id: int, db: Session = Depends(database.get_db)):
    previsao = db.query(models.Previsao).filter(models.Previsao.id == previsao_id).first()
    if not previsao:
        raise HTTPException(status_code=404, detail="Previsão não encontrada")
    
    db.delete(previsao)
    db.commit()
    return None