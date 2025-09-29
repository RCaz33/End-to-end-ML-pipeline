# Monitor ML model drift with evidently

1. Sign up for a free Evidently Cloud account

2. Create project
```python
from evidently.ui.workspace import CloudWorkspace
ws = CloudWorkspace(token="YOUR_API_TOKEN", url="https://app.evidently.cloud")
project = ws.create_project("My project name", org_id="YOUR_ORG_ID")
project.description = "My project description"
project.save()
```

3. Create Evidently dataset
```python
# Get Dataset
from sklearn import datasets
d = datasets.load_breast_cancer()

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(d.data, d.target, test_size=0.2, random_state=42, stratify=d.target)

# induce bias
df_eval_1 = X_train[:,X_train[4] < 1000]
df_eval_2 = X_train[:,X_train[4] > 1000]


# map columns type for evidently
from evidently import DataDefinition
schema = DataDefinition(
    numerical_columns=data.feature_names,
    # categorical_columns=["education", "occupation", "native-country", "workclass", "marital-status", "relationship", "race", "sex", "class"],
    )

# create 2 datasets to compare
from evidently import Dataset
eval_data_1 = Dataset.from_pandas(
    pd.DataFrame(df_eval_1, columns=data.feature_names),
    data_definition=schema
)
eval_data_2 = Dataset.from_pandas(
    pd.DataFrame(df_eval_2, columns=data.feature_names),
    data_definition=schema
)
```

4. Evaluate Drift & upload to UI
```python
from evidently import Report
from evidently.presets import DataDriftPreset, DataSummaryPreset 
report = Report([DataDriftPreset() , DataSummaryPreset() ], include_tests="True")

my_eval = report.run(eval_data_1, eval_data_2)

ws.add_run(project.id, my_eval, include_data=False)
```


