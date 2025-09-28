from sklearn.linear_model import LinearRegression
from app.utils.train_test_split import TrainTestSplit
from sklearn.metrics import root_mean_squared_error, mean_absolute_percentage_error
import numpy as np
import pandas as pd

class SklearnLienarRegression:
    def __init__(self, train_test_split: TrainTestSplit):
        self._train_test_split = train_test_split
        pass
    
    def model_trained(self):
        linear_regression = LinearRegression()
        model = linear_regression.fit(
            self._train_test_split.data["x_training"],
            self._train_test_split.data["y_training"],
        )
        return model

    def predictions(self):
        x_test = self._train_test_split.data['x_testing']
        months_trained = self._train_test_split.data['months_trained']
        y_pred = self.model_trained().predict(x_test)
        df_pred = pd.DataFrame({"month": months_trained, "prediction": y_pred}, index=months_trained)
        return df_pred
    
    def errors(self):
        y_test, y_pred = [self._train_test_split.data['y_testing'], self.predictions()['prediction'].values]
        mse = root_mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        mape = mean_absolute_percentage_error(y_test, y_pred)
        return {
            "mse":float(mse),
            "rmse":float(rmse),
            "mape":float(mape)
        }
        
    def make_prediction(self, features_predict: list[list[float]]):
        prediction = self.model_trained().predict(features_predict)
        return prediction