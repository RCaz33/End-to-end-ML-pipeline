
import pickle
import mlflow



def load_pickle_model(path="../src/model/logistic_regression_model.pkl"):

    # Load model once at startup
    with open(path, "rb") as f:
        model = pickle.load(f)

    return model

# load model from mlflow
# try:  model = mlflow.sklearn.load_model("runs:/<run_id>/model")  # Replace <run_id> or use experiment
# except : "cannot get model from mlflow"


# loggign API predictions on MLFLOW

from queue import Queue
import logging
logging.basicConfig(level=logging.INFO)

log_queue = Queue()

def batch_logger():
    batch = []
    while True:
        item = log_queue.get()
        batch.append(item)
        if len(batch) >= 10:  # batch size
            logging.info("Running MLflow batch logging...")
            mlflow.set_experiment("Tracking predictions")
            with mlflow.start_run():
                for log_item in batch:
                    mlflow.log_param("version", log_item["version"])
                    mlflow.log_metric("prediction", log_item["prediction"][0])
            batch.clear()
            logging.info("Batch logged to MLflow")