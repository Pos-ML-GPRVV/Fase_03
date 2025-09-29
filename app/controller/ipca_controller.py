from fastapi import APIRouter, HTTPException
from app.services.ipca_service import IpcaService
from app.DAO.ipca_dao import IpcaDAO
from app.schemas import PredictionInput, PredictionOutput
from fastapi import APIRouter, HTTPException, status, Body


router = APIRouter()
service = IpcaService()


@router.post("/prevision-ipca/", summary="Previsão online com 8 categorias")
def prevision_ipca(body: dict = Body(..., example={"data": [0.12, 0.05, 0.08, 0.03, 0.10, 0.02, 0.01, 0.04]})):
    """
    Espera um JSON: {"data": [n1,n2,n3,n4,n5,n6,n7,n8]}
    - Se a lista não tiver exatamente 8 números, responde 422 (erro claro de validação).
    """
    if "data" not in body or not isinstance(body["data"], list):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Corpo inválido. Envie {'data': [8 números]}.")

    data = body["data"]
    if len(data) != 8:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Deve ser informado exatamente 8 valores em 'data'.")

    try:
        y_pred = service.make_predictions([data])   # shape (1, 8)
        value = float(y_pred[0]) if hasattr(y_pred, "__len__") else float(y_pred)
        return {"prediction": value}
    except Exception as e:
        # se algo inesperado acontecer dentro do service, aí sim 500
        raise HTTPException(status_code=500, detail=f"Erro ao gerar a previsão do IPCA: {e}")
       
@router.get('/general-index-ipca')
def get_general_index_ipca():
    try:
        dao = IpcaDAO()
        general_index = dao.get_general_index()
        json_data = general_index.to_dict(orient='records')
        return json_data
    except Exception as e:
        print(f"Erro ao pegar indices gerais: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor ao buscar informações: {e}")

@router.get('/target-ipca')
def get_target_ipca():
    try:
        dao = IpcaDAO()
        target = dao.get_target()
        target =target.sort_values(by=['month'],ascending=True)
        json_data = target.to_dict(orient='records')
        return json_data
    except Exception as e:
        print(f"Erro ao pegar indices gerais: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor ao buscar informações: {e}")

@router.get('/feature-ipca')
def get_feature_ipca():
    try:
        dao = IpcaDAO()
        feature = dao.get_features_with_weight()
        json_data = feature.to_dict(orient='records')
        return json_data
    except Exception as e:
        print(f"Erro ao pegar categorias: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor ao buscar informações: {e}")

@router.get('/errors-metrics')
def get_errors_ipca():
    try:
        dao = IpcaDAO()
        errors = dao.get_errors()
        json_data = errors.to_dict(orient='records')
        return json_data
    except Exception as e:
        print(f"Erro ao pegar métricas de erro: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor ao buscar informações: {e}")
    
@router.post('/training-model')
def training_model():
    try:
        ipca_service = IpcaService()
        ipca_service.training_model()
        ipca_service.save_predictions()
        ipca_service.save_error_metrics()
        
        return {"message": "Modelo treinado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Erro ao treinar modelo: {e}')

