import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

class TrainTestSplit:
    def __init__(self):
        self.data = None
        self.min_max_scaler = StandardScaler()
        pass

    def train_test_split(self, x: pd.DataFrame, y: pd.DataFrame, test_size: float):
        x_values = self.min_max_scaler.fit_transform(x)
        y_values = y.values

        x_training, x_testing, y_training, y_testing = train_test_split(
            x_values, y_values, test_size=test_size, shuffle=False, random_state=23
        )

        self.data = {
            "x_training": x_training,
            "x_testing": x_testing,
            "y_training": y_training,
            "y_testing": y_testing,
        }
