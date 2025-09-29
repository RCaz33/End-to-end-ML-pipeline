

from fastapi import APIRouter, Depends, HTTPException

import logging
from datetime import datetime
import mlflow

from security import create_access_token, verify_token
from schemas import PredictRequest, LoginRequest
from utils import load_pickle_model



root_router = APIRouter(tags=["Logging & Health check"])

ml_model_router = APIRouter(
    prefix="/ML",
    tags=["API Prediction"],)
#     user=[Depends(verify_token)],  # use for security
# )
dev_router = APIRouter(
    prefix="/dev",
    tags=["For testing route locally"],)




@root_router.get("/health")
def health():
    return {"status": "ok"}

@root_router.post("/login")
def login(request: LoginRequest):
    logging.info(f"Login from: {request.username} on {datetime.now()}")
    # Simple auth - replace with real user verification with API database or env vile
    if request.username == "admin" and request.password == "password":
        access_token = create_access_token(data={"sub": request.username})
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")


## get drift from mlflow

## post train a new model (changing train test split) and register with mlflow

# load once at startup
# model = model_V1 = load_pickle_model("../src/model/logistic_regression_model.pkl")
# model_V2 = load_pickle_model("../src/model/logistic_regression_model_challenger.pkl")

# for test production 
model = model_v1 = load_pickle_model("./model/logistic_regression_model.pkl")
model_v2 = load_pickle_model("./model/logistic_regression_model.pkl")


@ml_model_router.post("/predict")
def predict(request: PredictRequest, user=Depends(verify_token)):
    logging.info(f"Prediction request from {user}: {request.data}")

    prediction = model.predict([request.data])
    # use mlflow to track model drift
    with mlflow.start_run():
        mlflow.log_param("input", request.data)
        mlflow.log_metric("prediction", prediction)
    return {"prediction": prediction.tolist()}


@dev_router.post("/predict")
def predict(request: PredictRequest):

    prediction = model.predict([request.data])
    # use mlflow to track model drift
    with mlflow.start_run():
        mlflow.log_param("input", request.data)
        mlflow.log_metric("prediction", prediction)
    return {"prediction": prediction.tolist()}
        

# A/B testing of model 
@dev_router.post("/AB_tests_predict")
def predict(request: PredictRequest):
    import random
    version = "Best_model" if random.random() < 0.5 else "Challenger_model"
    model = model_v1 if version == "Best_model" else model_v2
    prediction = model.predict([request.data])
    from utils import log_queue
    log_data = {"version": version, "data": request.data, "prediction": prediction.tolist()}
    log_queue.put(log_data)
    return {"prediction": prediction.tolist(), "model_version": version}