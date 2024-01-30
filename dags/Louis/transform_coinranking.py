from pyspark.sql import SparkSession

# Initialisation
spark = SparkSession.builder.appName("TransformAlphaVantageSpark").getOrCreate()

# Configuration
s3_bucket_name = 'datalake-3il-jljq'
input_s3_object_key = 'louis/coinranking/data/test.csv'
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
output_s3_object_key = 'louis/coinranking/transform/test.csv'
result.write.mode('overwrite').json(f"s3a://{s3_bucket_name}/{output_s3_object_key}")

# Arrêter Spark
spark.stop()
