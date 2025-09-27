import pandas as pd
from app.DAO.ipca_dao import IpcaDAO
from app.utils.train_test_split import TrainTestSplit
from app.utils.linear_regression import SklearnLienarRegression
from app.repository.ipca_repository import IpcaRepository
from app.database import SessionLocal


class IpcaService:
    def __init__(self):
        self.dao = IpcaDAO()
        pass

    def __target(self):
        ipca = self.df_ipca[self.df_ipca["D3C"] == "63"].copy()
        general_index = ipca[ipca["D4C"] == "7169"].copy()
        general_index.loc[:, "value"] = general_index["V"].astype(float)
        general_index.loc[:, "date"] = pd.to_datetime(
            general_index["D2C"], format="%Y%m"
        )
        general_index = general_index.sort_values(by="date", ascending=True)
        general_index = general_index.set_index("date")
        general_index = general_index["value"]
        
        return general_index

    def __feature(self):
        ipca_category = self.df_ipca[self.df_ipca["D4C"] != "7169"].copy()

        weight = ipca_category[ipca_category["D3C"] == "66"].copy()
        weight["id"] = weight["D4C"] + "-" + weight["D2C"]
        weight.loc[:, "value"] = pd.to_numeric(weight["V"], errors='coerce')
        weight['value'] = weight['value'].fillna(weight['value'].median())

        values = ipca_category[ipca_category["D3C"] == "63"].copy()
        values["id"] = values["D4C"] + "-" + values["D2C"]
        values.loc[:, "value"] = pd.to_numeric(values["V"], errors='coerce')
        values['value'] = values['value'].fillna(values['value'].median())
        
        merged_df = pd.merge(values, weight, on="id")
        merged_df["result"] = (merged_df["value_x"] / 100) * (
            merged_df["value_y"] / 100
        )
        merged_df.loc[:, "date"] = pd.to_datetime(merged_df["D2C_y"], format="%Y%m")
        merged_df = merged_df.set_index("date")
        merged_df = merged_df.pivot(columns="D4N_y", values="result")
        
        merged_df = merged_df.drop([''], axis=1)
        

        return merged_df
    
    def save_ipca_data_in_database(self):
        df = self.dao.get()
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
            
        
        repository.create_multiple_ipca_records(records)
        

    def ipca_predictions(self):
        self.df_ipca = self.dao.get()
        print(self.df_ipca)
        target = self.__target()
        feature = self.__feature()
        test = TrainTestSplit()
        test.train_test_split(feature, target, test_size=0.3)
        linear_regression = SklearnLienarRegression(test)
        prediction = linear_regression.pred()  
        errors = linear_regression.errors()
        # print(errors)
        
        return prediction
