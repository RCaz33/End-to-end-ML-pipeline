# API structure
from fastapi import FastAPI

# API internal logic
from routes import root_router, ml_model_router, dev_router

# initialize logging
import logging
logging.basicConfig(level=logging.INFO)

# initialize app    
# app = FastAPI()

app = FastAPI(
    title="API_prediction",
    description="API for serving classification model",
    version="1.0.0",
)

# Register routers
app.include_router(root_router)
app.include_router(ml_model_router)
app.include_router(dev_router)

