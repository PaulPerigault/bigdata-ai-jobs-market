-- KPI obligatoires Jour 3 (10 KPI) — issue #94.

-- KPI 1 : total offres / métiers.
-- Hive 2.3.2 ne supporte pas les sous-requêtes scalaires dans SELECT, et
-- les produits cartésiens sont désactivés par sécurité (CROSS JOIN
-- rejeté) : UNION ALL avec un discriminant plutôt qu'une seule ligne.
SELECT
    'offres' AS metrique,
    COUNT(*) AS total
FROM processed.offres
UNION ALL
SELECT
    'metiers' AS metrique,
    COUNT(*) AS total
FROM processed.metiers;

-- KPI 2 : salaire moyen ET médian.
SELECT
    ROUND(AVG(annual_salary_usd), 0) AS salaire_moyen,
    ROUND(PERCENTILE_APPROX(annual_salary_usd, 0.5), 0) AS salaire_median
FROM processed.offres;

-- KPI 3 : top 5 métiers les mieux rémunérés.
SELECT
    m.job_title,
    ROUND(AVG(o.annual_salary_usd), 0) AS salaire_moyen
FROM processed.offres AS o
INNER JOIN processed.metiers AS m ON o.metier_id = m.metier_id
GROUP BY m.job_title
ORDER BY salaire_moyen DESC
LIMIT 5;

-- KPI 4 : top 5 métiers les plus demandés.
SELECT
    m.job_title,
    COUNT(*) AS nb_offres
FROM processed.offres AS o
INNER JOIN processed.metiers AS m ON o.metier_id = m.metier_id
GROUP BY m.job_title
ORDER BY nb_offres DESC
LIMIT 5;

-- KPI 5 : top 5 compétences.
SELECT
    competence,
    COUNT(DISTINCT job_id) AS nb_offres
FROM processed.competences
GROUP BY competence
ORDER BY nb_offres DESC
LIMIT 5;

-- KPI 6 : salaire moyen par pays (top 5).
SELECT
    country,
    ROUND(AVG(annual_salary_usd), 0) AS salaire_moyen
FROM processed.offres
GROUP BY country
ORDER BY salaire_moyen DESC
LIMIT 5;

-- KPI 7 : salaire par niveau d'expérience.
SELECT
    experience_level,
    ROUND(AVG(annual_salary_usd), 0) AS salaire_moyen
FROM processed.offres
GROUP BY experience_level
ORDER BY salaire_moyen DESC;

-- KPI 8 : répartition télétravail / présentiel.
SELECT
    remote_work,
    COUNT(*) AS nb_offres,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct
FROM processed.offres
GROUP BY remote_work
ORDER BY nb_offres DESC;

-- KPI 9 : analyse LLM/GenAI (is_llm_role vient de la table RAW, pas processed).
SELECT
    is_llm_role,
    COUNT(*) AS nb_offres,
    ROUND(AVG(annual_salary_usd), 0) AS salaire_moyen,
    ROUND(AVG(ai_salary_premium_pct), 2) AS premium_moyen_pct
FROM projet_ia.ai_jobs_raw
GROUP BY is_llm_role;

-- KPI 10 : évolution 2025-2026 par période.
SELECT
    posting_year,
    posting_month,
    COUNT(*) AS nb_offres,
    ROUND(AVG(annual_salary_usd), 0) AS salaire_moyen
FROM processed.offres
GROUP BY posting_year, posting_month
ORDER BY posting_year, posting_month;
