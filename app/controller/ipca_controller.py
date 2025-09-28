from fastapi import APIRouter, HTTPException
from app.services.ipca_service import IpcaService
from app.DAO.ipca_dao import IpcaDAO
from app.schemas import PredictionInput, PredictionOutput

router = APIRouter()


@router.post("/prevision-ipca/", response_model=PredictionOutput)
async def prevision_ipca(input_data: PredictionInput):
    try:
        input_for_model = input_data.data 
        
        if(len(input_for_model) != 8):
            raise ValueError("Deve ser informado o valor de 8 categorias para realizar predição")
        
        predictions_array = IpcaService().make_predictions([input_for_model])
        
        if not predictions_array or not isinstance(predictions_array[0], (int, float)):
             raise ValueError("O serviço de previsão não retornou o formato esperado.")
             
        prediction_value = predictions_array[0]

        return {"prediction": prediction_value}

    except Exception as e:
        print(f"Erro ao gerar a previsão do IPCA: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor ao calcular a previsão: {e}")
    
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

