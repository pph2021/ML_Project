import os
import sys
from src.mlproject.exception import CustomException
from src.mlproject.logger import logging
import pandas as pd 
from dotenv import load_dotenv
import pymysql


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