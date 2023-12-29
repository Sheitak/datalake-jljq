import os
from datetime import datetime, timedelta
from io import StringIO

import boto3
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
import requests
from dotenv import load_dotenv

load_dotenv()

# Configuration
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_ACCESS_SECRET_KEY')
s3_bucket_name = 'datalake-3il-jljq'

api_key_alpha_vantage = os.environ.get('API_KEY_ALPHA_VANTAGE')
owner = os.environ.get('OWNER')

# Définition des paramètres
default_args = {
    'owner': owner,
    'start_date': datetime(2023, 11, 21),
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'ingestion_alpha_vantage',
    default_args=default_args,
    description='DAG pour l\'ingestion de données Alpha Vantage',
    schedule=timedelta(days=1),
)


def print_env_variables():
    print(f"OWNER: {owner}")
    print(f"API_KEY_ALPHA_VANTAGE: {api_key_alpha_vantage}")
    print(f"AWS_ACCESS_KEY_ID: {aws_access_key_id}")
    print(f"AWS_ACCESS_SECRET_KEY: {aws_secret_access_key}")


# Test Environment variable Python
test_env_task = PythonOperator(
    task_id='test_env_task',
    python_callable=print_env_variables,
    dag=dag,
)


def extract_stock_data():
    s3_object_key = 'quentin/alpha-vantage/data/stock.csv'
    alpha_vintage_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAA&apikey={api_key_alpha_vantage}'


# https://www.alphavantage.co/documentation/
# Obtenir les nouveaux sentiments du marché boursier ainsi que quelques métrics.
def extract_sentiment_news_data():
    s3_object_key = 'quentin/alpha-vantage/data/news-sentiment.csv'
    alpha_vintage_url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&apikey={api_key_alpha_vantage}'
    response = requests.get(alpha_vintage_url)
    data = response.text

    # Transformation des données CSV en StringIO
    csv_data = StringIO(data)

    # Initialisation de la session boto3 avec les informations d'identification de Quentin
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    # Utilisation de la session pour le client S3
    s3_client = session.client('s3')

    # Chargement des données dans le bucket S3
    s3_client.put_object(Body=csv_data.getvalue(), Bucket=s3_bucket_name, Key=s3_object_key)

    print(f"Données stockées avec succès dans S3 : {s3_bucket_name}/{s3_object_key}")


# Opérateur pour exécuter la fonction d'extraction et de téléchargement
ingest_data_task = PythonOperator(
    task_id='ingest_data_task',
    python_callable=extract_sentiment_news_data,
    dag=dag,
)

# Transformation avec Apache Spark
transform_spark_task = SparkSubmitOperator(
    task_id='transform_spark_task',
    application='transform_alpha_vantage.py',
    conn_id='spark_default',
    verbose=True,
    dag=dag,
)

# Définir l'ordre des tâches
test_env_task >> ingest_data_task >> transform_spark_task
