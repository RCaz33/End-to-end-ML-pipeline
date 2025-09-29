# End-to-End ML Pipeline

This repository contains an end-to-end machine learning pipeline, covering all stages from data ingestion to model deployment.

## Features

- Data collection and preprocessing
<!-- - Exploratory data analysis (EDA)
- Feature engineering -->
- Model training and evaluation
- Model deployment

## Project Structure

```
.
├── API_Model           # FastAPI app to expose model prediction whilst A/B testing
├── cloud               # Dummy folder to Mock a cloud hosted mlserver
├── src/                # Source code for pipeline components
├   ├── notebooks/      # Jupyter notebooks for EDA and prototyping
├   ├── data/           # Raw and processed data
├   ├── models/         # Saved models
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## Features
- Model training with scikit-learn
- REST API with FastAPI
- Docker containerization
- Cloud deployment (using Minio to mimick AWS S3 Bucket)
- Basic monitoring and logging
- Model versioning using mlflow


## Getting Started

### 1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/End-to-end-ML-pipeline.git
    cd End-to-end-ML-pipeline
    ```

### 2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### 3. Run the pipeline:

0. Get data
```bash
python src/create_data.py
```

1. Start a mlflow server
```bash
mlflow server --backend-store-uri sqlite:///src/mlruns.db --host 0.0.0.0 --port 5001
```

2. Train Models
```bash
python src/create_base_model.py
python src/create_challenger_model.py
```


3. Docker Deployment
```bash
docker build -t model_api .
docker run -p 4000:8000 model_api
```

4. Make 10 Predictions to upload to mlflow server
```bash
python src/predict_dummy.py
```


## API Endpoints
- `GET /health` - Health check
- `POST ML/predict` - Make predictions and log to mlflow
- `POST dev/predict` - To debug
- `POST dev/AB_tests_predict` - In developement, log 2 models to compare

## Contributing

Contributions are welcome! Please open issues or submit pull requests.

## License

This project is licensed under the MIT License.