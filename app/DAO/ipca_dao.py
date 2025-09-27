import sidrapy
from app.enums.tables_ipca import tables
import pandas as pd


class IpcaDAO:
    def __init__(self) -> None:
        pass

    def get(self):
        results = []
        # categories_str = ",".join(map(str, categories))
        for table_code, table_data in tables.items():
            get_ipca = sidrapy.get_table(
                table_code=table_code,
                territorial_level="1",
                ibge_territorial_code="all",
                variable=table_data["variable"],
                period="all",
                # categories=f"7169,{categories_str}",
                categories=f"7169,7170,7222,7445,7486,7558,7625,7660,7712,7766",
                classification=table_data["classification"],
                header="n",
            )
            results.append(pd.DataFrame(get_ipca))
            ipca = pd.concat(results, ignore_index=True)
            
        return ipca
