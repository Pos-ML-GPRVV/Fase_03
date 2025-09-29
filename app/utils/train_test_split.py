from __future__ import annotations

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


class TrainTestSplit:
    def __init__(self):
        self.data = None
        self.min_max_scaler = StandardScaler()

    def train_test_split(self, x: pd.DataFrame, y: pd.DataFrame, test_size: float):
        """
        - Aplica StandardScaler em X (features)
        - Mantém a ordem temporal
        - Armazena arrays/índices para consumo pelo modelo
        """
        x_values = self.min_max_scaler.fit_transform(x)
        y_values = y.values

        # meses correspondentes ao conjunto de TESTE (última janela)
        quantity_test = int(len(x) * test_size)
        months_trained = x[(len(x) - quantity_test) : len(x)].index

        x_training, x_testing, y_training, y_testing = train_test_split(
            x_values, y_values, test_size=test_size, shuffle=False, random_state=23
        )

        self.data = {
            "x_training": x_training,
            "x_testing": x_testing,
            "y_training": y_training,
            "y_testing": y_testing,
            "months_trained": months_trained,
        }
