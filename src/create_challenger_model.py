import mlflow
import os
import numpy as np

from dotenv import load_dotenv
load_dotenv()

from utils import load_data, train_and_log_model
data = load_data("./src/data")

remote_server_uri = os.getenv("MLFLOW_LOCAL_TRACKING_URI","file://src/mlruns")
print("mlflow use remote uri",remote_server_uri)
mlflow.set_tracking_uri(remote_server_uri)
mlflow.set_experiment("script_training_challenger")
mlflow.autolog()

train_and_log_model(data, "Challenger_model" ,n_iter = 10, random_state = 42)

