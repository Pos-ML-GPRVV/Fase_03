from fastapi import APIRouter, File, UploadFile, HTTPException
import pandas as pd
from io import BytesIO
from app.services.ipca_service import IpcaService
from app.DAO.ipca_dao import IpcaDAO

router = APIRouter()


@router.get("/prevision-ipca/")
async def privision():

    df = IpcaDAO().get()
    df = df[['D4N','D2C','D3N','V']]
    df = df.rename(columns={
        'D4N':'category',
        'D3N':'type',
        'D2C': 'month',
        'V': 'value'
    })
    print(df)
    
    
    return 200
