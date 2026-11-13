from pyspark.sql import SparkSession

HIVE_METASTORE_URI = "thrift://hive-metastore:9083"
HDFS_DEFAULT_FS = "hdfs://namenode:8020"


def get_spark(app_name: str) -> SparkSession:
    return (
        SparkSession.builder.appName(app_name)
        .config("spark.hadoop.fs.defaultFS", HDFS_DEFAULT_FS)
        .config("hive.metastore.uris", HIVE_METASTORE_URI)
        .enableHiveSupport()
        .getOrCreate()
    )
