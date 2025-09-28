from app.repository.ipca_repository import IpcaRepository
from app.database import SessionLocal
import numpy as np

class IpcaDAO:
    def __init__(self):
        pass
    
    def get_features(self):
        db = SessionLocal()
        repository = IpcaRepository(db)
        features = repository.get_features()
        return features
    
    def get_target(self):
        db = SessionLocal()
        repository = IpcaRepository(db)
        target = repository.get_target()
        return target
    
    def get_general_index(self):
        db = SessionLocal()
        repoistory = IpcaRepository(db)
        general_index = repoistory.get_general_index()
        general_index['prediction_value'] = general_index['prediction_value'].replace({np.nan: None})
        return general_index

    def get_errors(self):
        db = SessionLocal()
        repository = IpcaRepository(db)
        errors = repository.get_errors()
        return errors
    
    def get_features_with_weight(self):
        db = SessionLocal()
        repository = IpcaRepository(db)
        features_with_weight = repository.get_features_with_weight()
        return features_with_weight