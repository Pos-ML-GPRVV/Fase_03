from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.model.error_metrics import ErrorMetrics
from sqlalchemy import exc, delete


class ErrorMetricsRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def drop_all_error_metrics(self) -> None:
        ErrorMetricsTable = ErrorMetrics.__table__

        try:
            delete_stmt = delete(ErrorMetricsTable)
            
            self.db.execute(delete_stmt)
            self.db.commit()
            print("Todos os registros da tabela 'error_metrics' foram excluídos com sucesso.")

        except exc.SQLAlchemyError as e:
            self.db.rollback()
            print(f"Erro ao deletar registros da tabela 'error_metrics': {e}")
            
    def create_multiple_error_metrics(self, records: List[Dict[str, Any]]) -> None:
        ErrorMetricsTable = ErrorMetrics.__table__

        try:
            insert_stmt = ErrorMetricsTable.insert().values(records)
            self.db.execute(insert_stmt)
            self.db.commit()
            print(f"Inseridos {len(records)} novos registros de métricas.")
        
        except exc.SQLAlchemyError as e:
            self.db.rollback()
            print(f"Erro ao realizar inserção em massa de métricas de erro: {e}")