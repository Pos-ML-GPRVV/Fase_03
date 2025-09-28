# app/main.py
from fastapi import FastAPI, Depends
from app.controller.ipca_controller import router as ipca_router
from app.auth.api_key import api_key_auth
from app.database import Base, engine
from app.model.ipca import Ipca
from app.services.ipca_service import IpcaService

app = FastAPI(dependencies=[Depends(api_key_auth)])

app.include_router(ipca_router)

def create_database_tables():
    print("[POSTGRESQL]: Creating tables to Database...")
    Base.metadata.create_all(engine)
    print("[POSTGRESQL]: Tables created.")

ipca_service = IpcaService()

if __name__ == "__main__":
    import uvicorn
    create_database_tables()
    ipca_service.save_ipca_data_in_database()
    ipca_service.save_predictions()
    ipca_service.save_error_metrics()
    
    uvicorn.run(app, host="127.0.0.1", port=8000)
    
