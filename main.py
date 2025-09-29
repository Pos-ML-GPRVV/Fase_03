# main.py
from __future__ import annotations

from fastapi import FastAPI, Security
from fastapi.responses import RedirectResponse

from app.database import Base, engine
from app.controller.ipca_controller import router as ipca_router
from app.auth.api_key import require_api_key

# IMPORTANTE: importar os modelos para registrar as tabelas na Base
# (o “import” já registra na metadados do SQLAlchemy)
import app.model.ipca          # tabela ipca
import app.model.predictions   # tabela predictions
import app.model.error_metrics # tabela error_metrics


app = FastAPI(title="IPCA API")

def create_database_tables():
    print("[POSTGRESQL]: Creating tables to Database...")
    Base.metadata.create_all(engine)
    print("[POSTGRESQL]: Tables created.")

@app.on_event("startup")
def on_startup():
    create_database_tables()
    # Se quiser automatizar ETL/treino no startup, descomente:
    # from app.services.ipca_service import IpcaService
    # svc = IpcaService()
    # svc.save_ipca_data_in_database()
    # svc.save_predictions()
    # svc.save_error_metrics()

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
    uvicorn.run(app, host="127.0.0.1", port=8000)
