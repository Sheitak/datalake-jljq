from pyspark.sql import SparkSession

# Initialisation
spark = SparkSession.builder.appName("IngestionSpark").getOrCreate()

# Lire des données à partir de S3
s3_bucket = 'bigdata-jljq'
s3_key = 'chemin/dans/S3/vers/le/fichier.json'
data = spark.read.json(f"s3a://{s3_bucket}/{s3_key}")

# Effectuer des transformations ou des opérations Spark
result = data.select("colonne1", "colonne2").groupBy("colonne1").count()

# Écrire les résultats dans un autre emplacement S3
output_s3_key = 'chemin/dans/S3/vers/les/resultats'
result.write.mode('overwrite').json(f"s3a://{s3_bucket}/{output_s3_key}")

# Arrêter Spark
spark.stop()
