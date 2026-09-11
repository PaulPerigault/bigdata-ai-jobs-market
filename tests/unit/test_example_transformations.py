"""
Exemple illustrant le pattern attendu pour les tests unitaires PySpark
(voir docs/TESTING.md, niveau 1). À remplacer par les vrais tests une fois
les fonctions de transformation écrites dans spark-jobs/scripts/.

Ce fichier est volontairement autonome (ne dépend d'aucun module du projet)
pour servir de gabarit copiable.
"""

from pyspark.sql import functions as F


def explode_skills(df, skills_col="required_skills", sep="|"):
    """Transformation de référence pour la table `competences` :
    une ligne par offre x compétence."""
    return (
        df.withColumn("competence", F.explode(F.split(F.col(skills_col), r"\|")))
        .withColumn("competence", F.trim(F.col("competence")))
        .filter(F.col("competence") != "")
        .drop(skills_col)
    )


def test_explode_skills_row_count(spark):
    data = [("JOB001", "Python|Spark|SQL"), ("JOB002", "Go")]
    df = spark.createDataFrame(data, ["job_id", "required_skills"])

    result = explode_skills(df)

    assert result.count() == 4  # 3 + 1


def test_explode_skills_no_empty_values(spark):
    data = [("JOB001", "Python||SQL")]  # double séparateur -> valeur vide
    df = spark.createDataFrame(data, ["job_id", "required_skills"])

    result = explode_skills(df)

    assert result.filter(F.col("competence") == "").count() == 0
