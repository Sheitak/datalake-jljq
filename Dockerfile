FROM apache/airflow:2.7.3
LABEL authors="Sheitak"
ADD requirements.txt .
RUN pip install apache-airflow==${AIRFLOW_VERSION} -r requirements.txt
RUN pip install --upgrade pip
RUN pip install apache-airflow-providers-apache-spark