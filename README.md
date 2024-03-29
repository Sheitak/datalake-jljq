# Data Lake Project - JLJQ

This project is part of a study into the creation of a Data Lake, and focuses on the field of finance. It gathers different data sources to be formatted to obtain the final visualization of a trend in this field.

**Maintainers**

- [Johan Vertut](https://github.com/Nanificateur)
- [Louis Bayle](https://github.com/LouisBDev19)
- [Jules Mekontso](https://github.com/julesauffred)
- [Quentin Moreau](https://github.com/Sheitak)

### Starting Project

Clone this repository and place yourself inside it.

You can copy ``.env.example`` file to ``.env`` and replace the essential information.

### Apache-Airflow Docker

Refer to the [Airflow With Docker](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html) on the official airflow website for a clean installation with Docker.

Refer to the [Airflow Package In Docker](https://airflow.apache.org/docs/docker-stack/build.html#example-of-adding-airflow-provider-package-and-apt-package) For creating Docker File with packages.

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

Run Airflow Set-Up
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

### API Used

- [CoinMarketCap]()
- [Coinranking]()
- [CoinGecko]()
- [Alpha Vantage](https://www.alphavantage.co/documentation/)

### Resources

- [Airflow Documentation](https://airflow.apache.org/docs/apache-airflow/stable/index.html)
- [Apache Spark Documentation](https://spark.apache.org/docs/latest/)

Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>