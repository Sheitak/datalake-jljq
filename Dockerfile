ARG SPARK_VERSION="3.5.0"
ARG HADOOP_VERSION="3"

FROM apache/airflow:2.7.3
LABEL authors="JLJQ"
USER root

# Setup Command
RUN apt-get update \
  && apt-get install -y --no-install-recommends wget \
  && apt-get install -y procps \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Créez le répertoire Spark avec les autorisations appropriées
RUN mkdir -p /usr/local/spark \
  && chown -R airflow: /usr/local/spark

COPY requirements.txt /

# Setup Java
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         openjdk-11-jre-headless \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
USER airflow
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

# Setup Spark
ENV SPARK_VERSION="3.5.0"
ENV HADOOP_VERSION="3"
ENV SPARK_HOME /usr/local/spark
ENV HADOOP_CONF_DIR /usr/local/hadoop/etc/hadoop
ENV YARN_CONF_DIR /usr/local/hadoop/etc/hadoop
RUN cd "/tmp" && \
    wget --no-verbose "https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" && \
    tar -xvzf "spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" && \
    mkdir -p "${SPARK_HOME}/bin" && \
    mkdir -p "${SPARK_HOME}/assembly/target/scala-2.12/jars" && \
    cp -a "spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}/bin/." "${SPARK_HOME}/bin/" && \
    cp -a "spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}/jars/." "${SPARK_HOME}/assembly/target/scala-2.12/jars/" && \
    rm "spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" && \
    rm -rf "/tmp/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}"

RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt
