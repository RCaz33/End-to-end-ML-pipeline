import mlflow
import os
import numpy as np
from scipy.stats import loguniform, uniform
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from dotenv import load_dotenv

load_dotenv()

# Load files
X_train = np.loadtxt("src/data/X_train.csv", delimiter=",")
X_test = np.loadtxt("src/data/X_test.csv", delimiter=",")
y_train = np.loadtxt("src/data/y_train.csv", delimiter=",")
y_test = np.loadtxt("src/data/y_test.csv", delimiter=",")


remote_server_uri = os.getenv("MLFLOW_REMOTE_TRACKING_URI","file://src/mlruns")
print("mlflow use remote uri",remote_server_uri)
mlflow.set_tracking_uri(remote_server_uri)
mlflow.set_experiment("script_training_best_rdm_search")
mlflow.autolog()


with mlflow.start_run():
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', LogisticRegression(solver='saga', penalty='elasticnet'))
            ])
    
    param_distributions = {
            'classifier__C': loguniform(1e-5, 100),
            'classifier__l1_ratio': uniform(0, 1),
            'classifier__max_iter': np.arange(100, 1000, 100)
        }
    mlflow.log_params({
            "search_space_C": f"loguniform({1e-5}, {100})",
            "search_space_l1_ratio": f"uniform(0, 1)",
            "search_space_max_iter": f"arange(100, 1000, 100)"
        })
    
    n_iter = 50  
    print(f"Running RandomizedSearchCV with n_iter={n_iter}...")
    random_search = RandomizedSearchCV( estimator=pipeline,
                                        param_distributions=param_distributions,
                                        n_iter=n_iter,
                                        cv=8,  # 8-fold cross-validation
                                        scoring='roc_auc',  # Use ROC AUC score for evaluation
                                        random_state=42,
                                        n_jobs=-1,  # Use all available CPU cores
                                        )

    random_search.fit(X_train, y_train)

    # --- 4. Log Best Results to MLflow ---
    # Get the best parameters and score from the search
    best_params = random_search.best_params_
    best_score = random_search.best_score_
    best_estimator = random_search.best_estimator_

    # MLflow will log these as a single set of parameters for this run.
    print("Logging best parameters and cross-validation score...")
    mlflow.log_params(best_params)
    mlflow.log_metric("best_cv_roc_auc", best_score)

    # Log the best estimator's details
    print("Logging best estimator model...")
    model_info = mlflow.sklearn.log_model(
        sk_model=best_estimator,
        artifact_path="best_model",
        input_example=X_train,
        registered_model_name="Best-logreg-from-RandomSearch", # mandatory if wants to save model as .pkl
    )

    # --- 5. Evaluate the Best Model on the Test Set ---
    print("Evaluating the best model on the test set...")
    y_pred = best_estimator.predict(X_test)
    y_pred_proba = best_estimator.predict_proba(X_test)[:, 1]

    test_accuracy = accuracy_score(y_test, y_pred)
    test_roc_auc = roc_auc_score(y_test, y_pred_proba)

    # Log final metrics on the test set
    print("Logging final test metrics...")
    mlflow.log_metric("test_accuracy", test_accuracy)
    mlflow.log_metric("test_roc_auc", test_roc_auc)

    print("\nRun finished successfully!")
    print(f"Best cross-validation ROC AUC score: {best_score:.4f}")
    print(f"Test Accuracy: {test_accuracy:.4f}")
    print(f"Test ROC AUC: {test_roc_auc:.4f}")
    print("\nView run details by running 'mlflow ui' in your terminal.")

print("\nMLflow run ended.")
print("model info", model_info)