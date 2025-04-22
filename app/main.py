from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from . import models
from .database import engine
from .routers import previsao

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Weather API",
    description="API para buscar e armazenar previsões do tempo",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(previsao.router)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Previsão do Tempo"}