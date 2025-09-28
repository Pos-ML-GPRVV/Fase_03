from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.model.predictions import Predictions
from sqlalchemy import exc
from sqlalchemy.dialects.postgresql import insert

class PredictionsRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_ipca_record(self, record: Dict[str, Any]) -> Predictions | None:
        try:
            db_ipca = Predictions(**record)
            self.db.add(db_ipca)
            self.db.commit()
            self.db.refresh(db_ipca)
            return db_ipca
        except exc.SQLAlchemyError as e:
            self.db.rollback()
            print(f"Erro ao inserir registro IPCA: {e}")
            return None

    def create_multiple_ipca_records(self, records: List[Dict[str, Any]]) -> List[Predictions]:
        PredictionTable = Predictions.__table__

        try:
            insert_stmt = insert(PredictionTable).values(records)
            
            do_update_stmt = insert_stmt.on_conflict_do_update(
                constraint='uix_month_key',
                set_={
                    'value': insert_stmt.excluded.value,
                }
            )
            
            self.db.execute(do_update_stmt)
            self.db.commit()
            print(f"Inseridos {len(records)} novos registros de predições.")
                
        except exc.SQLAlchemyError as e:
            self.db.rollback()
            print(f"Erro ao realizar upsert em massa de registros: {e}")
 