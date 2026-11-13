-- Requête dédiée : jointure offres <-> competences (Jour 2, requête 12).
-- Top 10 compétences par nombre d'offres distinctes + salaire moyen associé.
SELECT
    c.competence,
    COUNT(DISTINCT o.job_id) AS nb_offres,
    ROUND(AVG(o.annual_salary_usd), 0) AS salaire_moyen
FROM processed.offres AS o
INNER JOIN processed.competences AS c ON o.job_id = c.job_id
GROUP BY c.competence
ORDER BY nb_offres DESC, c.competence ASC
LIMIT 10;

-- Requête GROUP BY + HAVING (Jour 2, requête 13).
-- Pays avec plus de 50 offres ET un salaire moyen supérieur à 150 000$.
SELECT
    country,
    COUNT(*) AS nb_offres,
    ROUND(AVG(annual_salary_usd), 0) AS salaire_moyen
FROM processed.offres
GROUP BY country
HAVING COUNT(*) > 50 AND AVG(annual_salary_usd) > 150000
ORDER BY salaire_moyen DESC;

-- Comparaison Hive SQL vs Spark SQL (chapitre 8) : même requête, deux moteurs.
-- Exécutée ici via Beeline (Hive-on-MR) ; l'équivalent Spark SQL est
-- `spark.sql(...)` sur la même table Hive, voir src/etl/spark_session.py.
SELECT
    experience_level,
    COUNT(*) AS nb_offres,
    ROUND(AVG(annual_salary_usd), 0) AS salaire_moyen
FROM processed.offres
GROUP BY experience_level
ORDER BY salaire_moyen DESC;
