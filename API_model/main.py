from fastapi import FastAPI
import pickle
from pydantic import BaseModel
import logging

logging.basicConfig(level=logging.INFO)

# Load model once at startup
with open("./model/logistic_regression_model.pkl", "rb") as f:
    model = pickle.load(f)

# initialize app    
app = FastAPI()

class PredictRequest(BaseModel):
    data: list

class BatchPredictRequest(BaseModel):
    data: list[list[float]]



@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(request: PredictRequest):
    logging.info(f"Prediction request: {request.data}")

    try:
        prediction = model.predict([request.data])
        logging.info(f"Prediction result: {prediction}")
        return {"prediction": prediction.tolist()}

    except:
        logging.info(f"Prediction Failed")
        return {"prediction": "failed to predict"}
        
    


