# Data Lake Project - JLJQ

This project is part of a study into the creation of a Data Lake, and focuses on the field of finance. It gathers different data sources to be formatted to obtain the final visualization of a trend in this field.

**Maintainers**

- [Johan Vertut](https://github.com/)
- [Louis Bayle](https://github.com/LouisBDev19)
- [Jules Mekontso](https://github.com/julesauffred)
- [Quentin Moreau](https://github.com/Sheitak)

### Apache-Airflow Docker

Refer to the source on the official airflow website for a clean installation with Docker

Source : https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html

**1. Initializing Environment**

Generate Folders And Define Airflow User If Necessary
```
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

Initialize Database
```
docker compose up airflow-init
```

Run Airflow
```
docker compose up -d
```

**2. Accessing the environment**

Running the CLI commands
```
docker compose run airflow-worker airflow info
```

***OR***

Open in browser
```
localhost:8080 or IP:8080
```

**Defaults Information**

Airflow Credentials
```
username: airflow
password: airflow
```