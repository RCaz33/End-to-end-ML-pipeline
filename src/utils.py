
import numpy as np
import mlflow
from scipy.stats import loguniform, uniform
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler




def load_data(path=""):
    # Load files
    print("Loading files...")
    X_train = np.loadtxt(f"{path}/X_train.csv", delimiter=",")
    X_test = np.loadtxt(f"{path}/X_test.csv", delimiter=",")
    y_train = np.loadtxt(f"{path}/y_train.csv", delimiter=",")
    y_test = np.loadtxt(f"{path}/y_test.csv", delimiter=",")

    data = dict({"X_train":X_train,
             "X_test":X_test,
             "y_train":y_train,
             "y_test":y_test})
    
    return data



def train_and_log_model(data, run_name, n_iter = 5, random_state = 42):

    with mlflow.start_run(run_name=run_name):
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
        mlflow.log_params({
            "n_iter": n_iter,
            "random_state": random_state,
        })
        
        print(f"Running RandomizedSearchCV with n_iter={n_iter}...")
        random_search = RandomizedSearchCV( estimator=pipeline,
                                            param_distributions=param_distributions,
                                            n_iter=n_iter,
                                            cv=8,  # 8-fold cross-validation
                                            scoring='roc_auc',  # Use ROC AUC score for evaluation
                                            random_state=random_state,
                                            n_jobs=-1,  # Use all available CPU cores
                                            )

        random_search.fit(data['X_train'], data['y_train'])

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
            name=run_name,
            input_example=data['X_train'],
            registered_model_name="Best-logreg-from-RandomSearch", # mandatory if wants to save model as .pkl
            tags={"Training Info": "model for A/B testing",
                  "random_state":random_state}
        )

        # --- 5. Evaluate the Best Model on the Test Set ---
        print("Evaluating the best model on the test set...")
        y_pred = best_estimator.predict(data['X_test'])
        y_pred_proba = best_estimator.predict_proba(data['X_test'])[:, 1]

        test_accuracy = accuracy_score(data['y_test'], y_pred)
        test_roc_auc = roc_auc_score(data['y_test'], y_pred_proba)

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
