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
- Cloud deployment
- Basic monitoring and logging

## Quick Start

### 1. Train Model
```bash
python src/train.py
```

### 2. Run API Locally
```bash
pip install -r requirements.txt
uvicorn src.app:app --reload
```
Test at `http://localhost:8000/docs`

### 3. Docker Deployment
```bash
docker build -t ml-pipeline .
docker run -p 8000:8000 ml-pipeline
```

### 4. Make Predictions
```bash
curl -X POST "http://localhost:8000/predict" \
-H "Content-Type: application/json" \
-d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```

## API Endpoints
- `GET /` - Health check
- `GET /health` - Service status
- `POST /predict` - Make predictions
- `GET /metrics` - Basic metrics

## Deployment
Deployed on [Heroku/Railway/AWS] at: `https://your-app-url.com`

## Model Performance
- Accuracy: 95%+
- ROC-AUC: 99%+
- Dataset: Breast Cancer
- Algorithm: Logistic Regression

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

## Next Steps
- Add model versioning
- Implement A/B testing
- Add more sophisticated monitoring
- Set up CI/CD pipeline