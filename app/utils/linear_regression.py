from sklearn.linear_model import LinearRegression
from app.utils.train_test_split import TrainTestSplit
from sklearn.metrics import root_mean_squared_error, mean_absolute_percentage_error
import numpy as np

class SklearnLienarRegression:
    def __init__(self, train_test_split: TrainTestSplit):
        self._train_test_split = train_test_split
        self._linear_regression = LinearRegression()
        self.fit = self._linear_regression.fit(
            self._train_test_split.data["x_training"],
            self._train_test_split.data["y_training"],
        )
        pass

    #TODO como prever mais de um mês
    def pred(self):
        x_test = self._train_test_split.data['x_testing']
        y_pred = self._linear_regression.predict(x_test)
        return y_pred
    
    def errors(self):
        y_test, y_pred = [self._train_test_split.data['y_testing'], self.pred()]
        mse = root_mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        mape = mean_absolute_percentage_error(y_test, y_pred)
        return {
            "mse":mse,
            "rmse":rmse,
            "mape":mape
        }
