# main.py
from __future__ import annotations

from fastapi import FastAPI, Security
from fastapi.responses import RedirectResponse

from app.database import Base, engine
from app.controller.ipca_controller import router as ipca_router
from app.auth.api_key import require_api_key
from app.services.ipca_service import IpcaService
ipca_service = IpcaService()

# IMPORTANTE: importar os modelos para registrar as tabelas na Base
# (o “import” já registra na metadados do SQLAlchemy)
from app.model.ipca import Ipca      # tabela ipca
import app.model.predictions   # tabela predictions
import app.model.error_metrics # tabela error_metrics


app = FastAPI(title="IPCA API")

def create_database_tables():
    print("[POSTGRESQL]: Creating tables to Database...")
    Base.metadata.create_all(engine)
    print("[POSTGRESQL]: Tables created.")

# 🔐 aplica API Key em TODAS as rotas do controller (faz o cadeado aparecer no /docs)
app.include_router(ipca_router, dependencies=[Security(require_api_key)])

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return RedirectResponse("/docs")

if __name__ == "__main__":
    import uvicorn
    create_database_tables()
    ipca_service.save_ipca_data_in_database()
    ipca_service.save_predictions()
    ipca_service.save_error_metrics()
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
