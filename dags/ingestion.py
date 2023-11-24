from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
import requests
import json
# boto3
# TODO : Exporter variables d'environnement avant lancement Airflow et remplacer dans .cfg

# Définition des paramètres
default_args = {
    'owner': 'Sheitak',
    'start_date': datetime(2023, 11, 21),
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'ingestion',
    default_args=default_args,
    description='DAG pour l\'ingestion de données',
    schedule=timedelta(days=1),
)


# Fonction pour récupérer les données de l'API et les stocker dans S3
def extract_and_upload_data():
    api_url = 'URL_de_votre_API'
    s3_bucket = 'bigdata-jljq'
    s3_key = 'chemin/dans/S3/vers/le/fichier.json'

    # Récupérer les données de l'API
    response = requests.get(api_url)
    data = response.json()

    # Stocker les données dans S3
    hook = S3Hook(aws_conn_id='aws_default')
    hook.load_string(json.dumps(data), key=s3_key, bucket_name=s3_bucket)


# Opérateur pour exécuter la fonction d'extraction et de téléchargement
ingest_data_task = PythonOperator(
    task_id='ingest_data_task',
    python_callable=extract_and_upload_data,
    dag=dag,
)

# Tâche Spark
ingest_spark_task = SparkSubmitOperator(
    task_id='spark_task',
    application='../spark/spark_ingest.py',
    conn_id='spark_default',
    verbose=True,
    dag=dag,
)

# Définir l'ordre des tâches
ingest_data_task >> ingest_spark_task
