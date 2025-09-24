
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
