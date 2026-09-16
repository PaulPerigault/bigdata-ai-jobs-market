-- 4 analyses au choix (issue #95).

-- Analyse 1 : prime salariale IA — top 5 métiers par premium moyen.
SELECT
    m.job_title,
    ROUND(AVG(o.ai_salary_premium_pct), 2) AS premium_moyen_pct,
    ROUND(AVG(o.annual_salary_usd), 0) AS salaire_moyen
FROM processed.offres AS o
INNER JOIN processed.metiers AS m ON o.metier_id = m.metier_id
GROUP BY m.job_title
ORDER BY premium_moyen_pct DESC
LIMIT 5;

-- Analyse 2 : LLM/GenAI vs autres métiers, comparaison enrichie
-- (au-delà de la moyenne simple du KPI 9 : médiane + demande + volume).
SELECT
    is_llm_role,
    COUNT(*) AS nb_offres,
    ROUND(AVG(annual_salary_usd), 0) AS salaire_moyen,
    ROUND(PERCENTILE_APPROX(annual_salary_usd, 0.5), 0) AS salaire_median,
    ROUND(AVG(demand_score), 1) AS demand_score_moyen
FROM projet_ia.ai_jobs_raw
GROUP BY is_llm_role;

-- Analyse 3 : expérience-salaire, avec une matrice de corrélation
-- (Pearson, via CORR() — descriptif, aucun modèle entraîné) entre
-- salaire, expérience, demande et premium IA.
SELECT
    ROUND(CORR(annual_salary_usd, years_of_experience), 3)
    AS corr_sal_exp,
    ROUND(CORR(annual_salary_usd, demand_score), 3)
    AS corr_sal_demande,
    ROUND(CORR(annual_salary_usd, ai_salary_premium_pct), 3)
    AS corr_sal_premium,
    ROUND(CORR(years_of_experience, demand_score), 3)
    AS corr_exp_demande
FROM projet_ia.ai_jobs_raw;

-- Analyse 4 : pays et compétences — compétence n°1 par pays (top 5
-- paires pays/compétence par volume), via fonction fenêtre.
SELECT
    country,
    competence AS top_competence,
    nb_offres
FROM (
    SELECT
        country,
        competence,
        nb_offres,
        ROW_NUMBER() OVER (PARTITION BY country ORDER BY nb_offres DESC) AS rnk
    FROM (
        SELECT
            o.country,
            c.competence,
            COUNT(DISTINCT o.job_id) AS nb_offres
        FROM processed.offres AS o
        INNER JOIN processed.competences AS c ON o.job_id = c.job_id
        GROUP BY o.country, c.competence
    ) AS t
) AS r
WHERE rnk = 1
ORDER BY nb_offres DESC
LIMIT 5;
