from pyspark.sql.types import DoubleType, IntegerType, StringType, StructField, StructType

RAW_SCHEMA = StructType(
    [
        StructField("job_id", StringType(), True),
        StructField("job_title", StringType(), True),
        StructField("job_category", StringType(), True),
        StructField("experience_level", StringType(), True),
        StructField("years_of_experience", IntegerType(), True),
        StructField("education_required", StringType(), True),
        StructField("annual_salary_usd", DoubleType(), True),
        StructField("salary_min_usd", DoubleType(), True),
        StructField("salary_max_usd", DoubleType(), True),
        StructField("city", StringType(), True),
        StructField("country", StringType(), True),
        StructField("remote_work", StringType(), True),
        StructField("company_size", StringType(), True),
        StructField("industry", StringType(), True),
        StructField("required_skills", StringType(), True),
        StructField("ai_salary_premium_pct", DoubleType(), True),
        StructField("demand_score", IntegerType(), True),
        StructField("demand_growth_yoy_pct", DoubleType(), True),
        StructField("benefits_score_10", DoubleType(), True),
        StructField("posting_year", IntegerType(), True),
        StructField("posting_month", IntegerType(), True),
        StructField("is_senior", IntegerType(), True),
        StructField("is_remote_friendly", IntegerType(), True),
        StructField("is_llm_role", IntegerType(), True),
        StructField("salary_tier", StringType(), True),
    ]
)
