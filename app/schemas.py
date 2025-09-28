from pydantic import BaseModel
from typing import List

class PredictionInput(BaseModel):
    data: List[float]

class PredictionOutput(BaseModel):
    prediction: float