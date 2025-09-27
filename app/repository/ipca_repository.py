from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.model.ipca import Ipca # Presumindo que o modelo está aqui
from sqlalchemy import exc
from sqlalchemy.dialects.postgresql import insert

class IpcaRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_ipca_record(self, record: Dict[str, Any]) -> Ipca | None:
        try:
            db_ipca = Ipca(**record)
            self.db.add(db_ipca)
            self.db.commit()
            self.db.refresh(db_ipca)
            return db_ipca
        except exc.SQLAlchemyError as e:
            self.db.rollback()
            print(f"Erro ao inserir registro IPCA: {e}")
            return None

    def create_multiple_ipca_records(self, records: List[Dict[str, Any]]) -> List[Ipca]:
        IpcaTable = Ipca.__table__
        CONSTRAINT_NAME = 'uix_ipca_key'

        try:
            insert_stmt = insert(IpcaTable).values(records)
            do_update_stmt = insert_stmt.on_conflict_do_update(
                constraint=CONSTRAINT_NAME, 
                set_={
                    'value': insert_stmt.excluded.value,
                }
            )
            self.db.execute(do_update_stmt)
            self.db.commit()
            
        except exc.SQLAlchemyError as e:
            self.db.rollback()
            print(f"Erro ao realizar upsert em massa de registros IPCA: {e}")
            
    def get(self): 
        pass #TODO criar o get