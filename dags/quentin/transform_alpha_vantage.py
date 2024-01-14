from pyspark.sql import SparkSession

# Configuration
# os.environ["HADOOP_HOME"] = os.environ.get('HADOOP_HOME')
# os.environ["HADOOP_CONF_DIR"] = os.path.join(os.environ["HADOOP_HOME"], "etc/hadoop")

# Initialisation
spark = SparkSession.builder.appName("TransformAlphaVantageSpark").getOrCreate()

# Configuration
s3_bucket_name = 'datalake-3il-jljq'
input_s3_object_key = 'quentin/alpha-vantage/data/news-sentiment.csv'
data = spark.read.json(f"s3a://{s3_bucket_name}/{input_s3_object_key}")

# Afficher quelques lignes des données pour vérification
data.show()

# Comprendre la structure des données
data.printSchema()

# Effectuer des transformations ou des opérations Spark
result = data.select("colonne1", "colonne2").groupBy("colonne1").count()

# Afficher les résultats
result.show()

# Écrire les résultats dans un autre emplacement S3
output_s3_object_key = 'quentin/alpha-vantage/transform/news-sentiment.csv'
result.write.mode('overwrite').json(f"s3a://{s3_bucket_name}/{output_s3_object_key}")

# Arrêter Spark
spark.stop()
