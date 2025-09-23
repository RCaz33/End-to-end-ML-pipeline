from sklearn import datasets

X,y = datasets.load_breast_cancer(return_X_y=True)


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

import os
import numpy as np
os.makedirs('src/data', exist_ok=True)

np.savetxt("src/data/X_train.csv", X_train, delimiter=",")
np.savetxt("src/data/X_test.csv", X_test, delimiter=",")
np.savetxt("src/data/y_train.csv", y_train, delimiter=",")
np.savetxt("src/data/y_test.csv", y_test, delimiter=",")
