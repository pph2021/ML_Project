#End to end data science project

MLFLOW_TRACKING_URI=https://dagshub.com/pph2021/ML_Project.mlflow /

MLFLOW_TRACKING_USERNAME=pph2021 /

MLFLOW_TRACKING_PASSWORD= import dagshub
dagshub.init(repo_owner='pph2021', repo_name='ML_Project', mlflow=True)

import mlflow
with mlflow.start_run():
  mlflow.log_param('parameter name', 'value')
  mlflow.log_metric('metric name', 1)

