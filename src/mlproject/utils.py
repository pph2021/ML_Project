import os
import sys
from src.mlproject.exception import CustomException
from src.mlproject.logger import logging
import pandas as pd 
from dotenv import load_dotenv
from sklearn.model_selection import GridSearchCV
import pymysql
import pickle  
from sklearn.metrics import r2_score




load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", 3306))  # default to 3306 if not set
DB_USER = os.getenv("DB_USER")
DB_PASSWORD=os.getenv('DB_PASSWORD')
DB_NAME = os.getenv("DB_NAME")

def read_sql_data():
    logging.info("Reading sql database started")
    try:
        mydb = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
        )
        logging.info("Connection established",mydb)
        df=pd.read_sql_query('Select * from students',mydb)
        print(df.head())
        return df

    except Exception as e:
        raise CustomException(e,sys)
    
def save_object(file_path, obj):
    """Save an object to the specified file path using pickle."""
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            pickle.dump(obj, file_obj)
    except Exception as e:
        raise Exception(f"Error saving object: {e}")
    

def evaluate_models(X_train, y_train,X_test,y_test,models,param):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            para=param[list(models.keys())[i]]

            gs = GridSearchCV(model,para,cv=3)
            gs.fit(X_train,y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)

            #model.fit(X_train, y_train)  # Train model

            y_train_pred = model.predict(X_train)

            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_pred)

            test_model_score = r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score

        return report
    
    except Exception as e:
        raise CustomException(e, sys)
