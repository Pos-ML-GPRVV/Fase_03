from app.DAO.sidrapy_dao import SidrapyDAO
from app.utils.train_test_split import TrainTestSplit
from app.utils.linear_regression import SklearnLienarRegression
from app.repository.ipca_repository import IpcaRepository
from app.database import SessionLocal
from app.DAO.ipca_dao import IpcaDAO
from app.repository.predictions_repository import PredictionsRepository
from app.repository.error_metrics_repository import ErrorMetricsRepository


class IpcaService:
    def __init__(self):
        self.sidrapy_dao = SidrapyDAO()
        self.ipca_dao = IpcaDAO()
        pass

    def __target(self):
        df_target = self.ipca_dao.get_target()
        df_target = df_target.set_index('month')
        df_target = df_target['value']
        return df_target
        

    def __feature(self):
        df_features = self.ipca_dao.get_features()
        df_pivot = df_features.pivot(
            index='month', 
            columns='category', 
            values='value'
        )
        return df_pivot
    
    def save_ipca_data_in_database(self):
        df = self.sidrapy_dao.get()
        df = df[['D4N','D2C','D3N','V']]
        df = df.rename(columns={
            'D4N':'category',
            'D3N':'type',
            'D2C': 'month',
            'V': 'value'
        })
        df['category'] = df['category'].str.strip()
        df = df[df['category'] != '']
        
        records = []
        
        db = SessionLocal() 
        
        repository = IpcaRepository(db)

        for _, row in df.iterrows():
            ipca_record = {
                "category": row['category'],
                "month": row['month'],
                "type": row['type'],
                "value": float(row['value']) if row['value'] != '...' else 0,
            }
            
            records.append(ipca_record)
            
        print(f"Inserindo {len(records)} novos registros do Ipca no banco de dados.")
        repository.create_multiple_ipca_records(records)

    def training_model(self):
        target = self.__target()
        feature = self.__feature()
        test = TrainTestSplit()
        test.train_test_split(feature, target, test_size=0.3) 
        linear_regression = SklearnLienarRegression(test)
        linear_regression.model_trained()
        
        return linear_regression
    
    def save_predictions(self):
        df_predictions = self.training_model().predictions()
        db = SessionLocal() 
        records = []
        repository = PredictionsRepository(db)
        
        for _, row in df_predictions.iterrows():
            prediction_record = {
                "month": row['month'],
                "value": float(row['prediction']) if row['prediction'] != '...' else 0,
            }
            
            records.append(prediction_record)
            
        repository.create_multiple_ipca_records(records)
        
    def save_error_metrics(self):
        records_errors = self.training_model().errors()
        db = SessionLocal() 
        repository = ErrorMetricsRepository(db)
        
        repository.drop_all_error_metrics()
        
        repository.create_multiple_error_metrics([records_errors])
        
    def make_predictions(self, feature_predictions: list[list[float]]):
        return self.training_model().make_prediction(feature_predictions)
