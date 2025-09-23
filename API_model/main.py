from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import pickle
from pydantic import BaseModel
import logging
import jwt
from datetime import datetime, timedelta
import os

# SET SECURITY
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()


logging.basicConfig(level=logging.INFO)

# Load model once at startup
with open("./model/logistic_regression_model.pkl", "rb") as f:
    model = pickle.load(f)

# initialize app    
app = FastAPI()

class PredictRequest(BaseModel):
    data: list

class LoginRequest(BaseModel):
    username: str
    password: str



def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/login")
def login(request: LoginRequest):
    # Simple auth - replace with real user verification with API database or env vile
    if request.username == "admin" and request.password == "password":
        access_token = create_access_token(data={"sub": request.username})
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(request: PredictRequest):
    logging.info(f"Prediction with: {request.data}")

    try:
        prediction = model.predict([request.data])
        logging.info(f"Prediction result: {prediction}")
        return {"prediction": prediction.tolist()}

    except:
        logging.info(f"Prediction Failed")
        return {"prediction": "failed to predict"}
        
    

@app.post("/predict_token")
def predict(request: PredictRequest, user=Depends(verify_token)):
    logging.info(f"Prediction request from {user}: {request.data}")

    try:
        prediction = model.predict([request.data])
        logging.info(f"Prediction result: {prediction}")
        return {"prediction": prediction.tolist()}

    except:
        logging.info(f"Prediction Failed")
        return {"prediction": "failed to predict"}
        
    

