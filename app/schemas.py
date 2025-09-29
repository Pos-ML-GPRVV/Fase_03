from pydantic import BaseModel, conlist

class PredictionInput(BaseModel):
    # exatamente 8 números (v2 usa min_length/max_length)
    data: conlist(float, min_length=8, max_length=8)

class PredictionOutput(BaseModel):
    prediction: float
