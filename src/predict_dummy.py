from sklearn import datasets

X,y = datasets.load_breast_cancer(return_X_y=True)

import requests

url_predict = "http://127.0.0.1:4000/dev/AB_tests_predict" # use docker container expose port

# predict one
response = requests.post(url=url_predict,json={"data":list(X[0])})

print(response.status_code)
print(response.content)