from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.model.ipca import Ipca
from sqlalchemy import exc, text
from sqlalchemy.dialects.postgresql import insert
import pandas as pd

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
            
    def get_features(self): 
        df_feature = pd.read_sql_query(
            sql=text("""
                     select 
                        i.month,
                        i.category,
                        i.type,
                        (i.value * w.value) as "value"
                        from ipca as i 
                        left join (
                            select 
                                i.month,
                                i.category,
                                i.type,
                                i.value
                                from ipca as i 
                                where 1=1
                                and i.category <> 'Índice geral' 
                                and i.type = 'IPCA - Peso mensal'
                        ) as w on w.month = i.month and w.category = i.category
                        where 1=1
                        and i.category <> 'Índice geral' 
                        and i.type <> 'IPCA - Peso mensal'
                     """), 
            con=self.db.bind 
        )

        return df_feature
    
    def get_target(self):
        df_target = pd.read_sql_query(
            sql="""
            select 
                i.month,
                i.category,
                i.type,
                i.value
                from ipca as i 
                where 1=1
                and i.category = 'Índice geral' 
                and i.type <> 'IPCA - Peso mensal'
            """,
            con=self.db.bind
        )
        
        return df_target
    
    
    def get_general_index(self):
        df_general_index = pd.read_sql_query(
            sql="""
            select 
                i.month,
                i.type,
                i.value as "real_value",
                p.value as "prediction_value"
                from ipca as i
                left join predictions as p on p.month = i.month
                where 1=1
                and i.type = 'IPCA - Variação mensal'
                and i.category = 'Índice geral'
            """,
            con=self.db.bind
        )
        
        return df_general_index
    
    def get_errors(self):
        df_errors = pd.read_sql_query(
            sql="""
            select 
                em.mse,
                em.rmse,
                em.mape
            from error_metrics as em
            """,
            con=self.db.bind
        )
        
        return df_errors
    
    def get_features_with_weight(self):
        df_features_with_weight = pd.read_sql_query(
            sql="""
            select 
                i.month,
                i.category,
                i.type,
                i.value,
                w.value as "weight"
                from ipca as i 
                left join (
                    select 
                        i.month,
                        i.category,
                        i.type,
                        i.value
                        from ipca as i 
                        where 1=1
                        and i.category <> 'Índice geral' 
                        and i.type = 'IPCA - Peso mensal'
                ) as w on w.month = i.month and w.category = i.category
                where 1=1
                and i.category <> 'Índice geral' 
                and i.type <> 'IPCA - Peso mensal'
            """,
            con=self.db.bind
        )
        
        return df_features_with_weight
    