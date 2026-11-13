from pyspark.sql import DataFrame, SparkSession

_SPARK_TO_HIVE_TYPE = {
    "string": "STRING",
    "int": "INT",
    "integer": "INT",
    "bigint": "BIGINT",
    "long": "BIGINT",
    "double": "DOUBLE",
    "float": "FLOAT",
    "boolean": "BOOLEAN",
}


def _hive_columns_ddl(df: DataFrame) -> str:
    columns = []
    for field in df.schema.fields:
        hive_type = _SPARK_TO_HIVE_TYPE.get(field.dataType.typeName(), "STRING")
        columns.append(f"{field.name} {hive_type}")
    return ",\n    ".join(columns)


def write_processed_table(
    spark: SparkSession,
    df: DataFrame,
    database: str,
    table: str,
    hdfs_location: str,
) -> None:
    """Écrit `df` en Parquet sur HDFS puis (re)crée la table Hive externe
    correspondante, en dérivant le DDL depuis le schéma Spark."""
    df.write.mode("overwrite").parquet(hdfs_location)

    spark.sql(f"CREATE DATABASE IF NOT EXISTS {database}")
    spark.sql(f"DROP TABLE IF EXISTS {database}.{table}")
    ddl = f"""
        CREATE EXTERNAL TABLE {database}.{table} (
            {_hive_columns_ddl(df)}
        )
        STORED AS PARQUET
        LOCATION '{hdfs_location}'
    """
    spark.sql(ddl)
