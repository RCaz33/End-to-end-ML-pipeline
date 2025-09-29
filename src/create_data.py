
# In a real project, this is replace by an ETL pipeline
from sklearn import datasets
X,y = datasets.load_breast_cancer(return_X_y=True)

# In a real project, this includes an EDA sent to a dashboard
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# In a cloud project, data is stored as blob (AZURE) or in s3 bucket
import os
import numpy as np
os.makedirs('src/data', exist_ok=True)

# In a mlops project, these are stored with mlflow tracking server
np.savetxt("src/data/X_train.csv", X_train, delimiter=",")
np.savetxt("src/data/X_test.csv", X_test, delimiter=",")
np.savetxt("src/data/y_train.csv", y_train, delimiter=",")
np.savetxt("src/data/y_test.csv", y_test, delimiter=",")

# This can be used as backbone to develop supervized task
# NLP project can segment texts with t-SNE and train a supervized k-means algorithm