# app/utils/linear_regression.py
from __future__ import annotations

from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_percentage_error,
)
import numpy as np
import pandas as pd


class SklearnLienarRegression:
    def __init__(self, train_test_split):
        self._train_test_split = train_test_split
        self._model = None

    def model_trained(self):
        if self._model is not None:
            return self._model
            
        lr = LinearRegression()
        self._model = lr.fit(
            self._train_test_split.data["x_training"],
            self._train_test_split.data["y_training"],
        )
        return self._model

    def predictions(self) -> pd.DataFrame:
        x_test = self._train_test_split.data["x_testing"]
        months_trained = self._train_test_split.data["months_trained"]
        y_pred = self.model_trained().predict(x_test)
        df_pred = pd.DataFrame(
            {"month": months_trained, "prediction": y_pred},
            index=months_trained,
        )
        return df_pred

    def errors(self) -> dict:
        """
        Corrigido:
        - MSE 
        - RMSE
        - MAPE 
        """
        y_test = self._train_test_split.data["y_testing"]
        y_pred = self.predictions()["prediction"].values

        mse = mean_squared_error(y_test, y_pred, squared=True)
        rmse = float(np.sqrt(mse))
        mape = mean_absolute_percentage_error(y_test, y_pred)

        return {"mse": float(mse), "rmse": rmse, "mape": float(mape)}

    def make_prediction(self, features_predict: list[list[float]]):
        prediction = self.model_trained().predict(features_predict)
        return prediction
