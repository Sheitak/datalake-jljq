#FROM apache/airflow:2.7.3
#LABEL authors="Sheitak"
#ADD requirements.txt .
#RUN pip install --upgrade pip
#RUN pip install apache-airflow==${AIRFLOW_VERSION} -r requirements.txt
#RUN pip install apache-airflow-providers-apache-spark
#RUN pip install pyspark

FROM apache/airflow:2.7.3
LABEL authors="JLJQ"
USER root
COPY requirements.txt /
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         openjdk-11-jre-headless \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
USER airflow
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt
