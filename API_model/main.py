from fastapi import FastAPI
import pickle
from pydantic import BaseModel

# Load model once at startup
with open("../src/model/logistic_regression_model.pkl", "rb") as f:
    model = pickle.load(f)

# initialize app    
app = FastAPI()

class PredictRequest(BaseModel):
    data: list

class BatchPredictRequest(BaseModel):
    data: list[list[float]]


@app.post("/predict")
def predict(request: PredictRequest):
    prediction = model.predict([request.data])
    return {"prediction": prediction.tolist()}

@app.post("/batch_predict")
def batch_predict(request: BatchPredictRequest):
    print(request.data)
    prediction = model.predict(request.data)
    print(request.data)
    return {"prediction": prediction.tolist()}
