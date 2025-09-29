# MLOps End-to-End Pipeline

A complete machine learning pipeline with training, containerization, deployment, and monitoring.

## Project Structure
```
mlops-pipeline/
├── data/
│   ├── train.csv
│   └── test.csv
├── models/
│   └── model.pkl
├── src/
│   ├── train.py
│   └── app.py
├── Dockerfile
├── requirements.txt
└── README.md
```

## Features
- Model training with scikit-learn
- REST API with FastAPI
- Docker containerization
- Cloud deployment (using Minio to mimick AWS S3 Bucket)
- Basic monitoring and logging
- Model versioning using mlflow


## Quick Start

### 0. Get data
```bash
python src/create_data.py
```

### 1. Start a mlflow server
```bash
mlflow server --backend-store-uri sqlite:///src/mlruns.db --host 0.0.0.0 --port 5001
```

### 2. Train Models
```bash
python src/create_base_model.py
python src/create_challenger_model.py
```


### 3. Docker Deployment
```bash
docker build -t model_api .
docker run -p 4000:8000 model_api
```

### 4. Make 10 Predictions to upload to mlflow server
```bash
python src/predict_dummy.py
```

### 5. Deploy with CD/CI on docker



## API Endpoints
- `GET /` - Health check
- `GET /health` - Service status
- `POST /predict` - Make predictions
- `GET /metrics` - Basic metrics


## Monitoring
- Request logging
- Prediction tracking
- Health checks
- Error handling

## Technologies Used
- **ML**: scikit-learn, pandas, numpy
- **API**: FastAPI, uvicorn
- **Containerization**: Docker
- **Deployment**: Heroku/Railway
- **Monitoring**: Python logging
