import os
import boto3
import requests

from datetime import datetime, timedelta
from io import StringIO
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from dotenv import load_dotenv

load_dotenv()

# Configuration
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_ACCESS_SECRET_KEY')
s3_bucket_name = 'datalake-3il-jljq'

api_key_alpha_vantage = os.environ.get('API_KEY_ALPHA_VANTAGE')
owner = os.environ.get('OWNER')

# Configuration Spark
spark_config = {
    'appName': 'TransformDataSpark',
    'conn_id': 'spark_default',
    'spark.master': 'spark://spark-master:7077',

    # Ajoutez d'autres configurations Spark si nécessaire
    # 'spark.executor.memory': '4 g', # Mémoire par exécuteur
    # 'spark.executor.cores': 3, # Cœurs par exécuteur
    # 'spark.driver.memory': '2g', # Mémoire pour le driver (votre application principale)
    # 'spark.driver.cores': 2,  # Cœurs pour le driver
    # 'spark.default.parallelism' : 10, # Nombre de partitions par défaut
    # 'spark.sql.shuffle.partitions': 10, # Partitions pour les opérations de shuffle
    # 'spark.dynamicAllocation.enabled' : 'false' # Désactiver l'allocation dynamique pour un mode local

    # 'spark.yarn.appMasterEnv.SPARK_HOME': '/usr/local/spark',  # Remplacez par le chemin correct
    # 'spark.yarn.appMasterEnv.HADOOP_CONF_DIR': '/usr/local/hadoop/etc/hadoop',  # Remplacez par le chemin correct
    # 'spark.yarn.appMasterEnv': '/conf/spark-env.sh',
}

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


# https://www.alphavantage.co/documentation/
# Obtenir les nouveaux sentiments du marché boursier ainsi que quelques métrics.
def extract_sentiment_news_data():
    s3_path = 'quentin/alpha-vantage/data/news-sentiment.csv'
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
    s3_client.put_object(Body=csv_data.getvalue(), Bucket=s3_bucket_name, Key=s3_path)

    print(f"Données stockées avec succès dans S3 : {s3_bucket_name}/{s3_path}")


# Opérateur pour exécuter la fonction d'extraction et de téléchargement
ingest_data_task = PythonOperator(
    task_id='ingest_data_task',
    python_callable=extract_sentiment_news_data,
    dag=dag,
)

# Transformation avec Apache Spark
transform_data_task = SparkSubmitOperator(
    task_id='transform_data_task',
    application='transform_alpha_vantage.py',
    verbose=True,
    conf=spark_config,
    dag=dag,
)

# Définir l'ordre des tâches
test_env_task >> ingest_data_task >> transform_data_task
