# Schéma du dataset — `ai_jobs_market_2025_2026.csv`

Inspection réelle du fichier (J1), pas les types annoncés dans la
description marketing du dataset. Source de vérité pour le `CREATE
EXTERNAL TABLE` Hive RAW (J2) et le nettoyage Spark (J3).

**Volumétrie** : 1500 lignes, 25 colonnes, aucune ligne dupliquée, aucun
`job_id` dupliqué, aucune valeur nulle détectée sur aucune colonne (à
revérifier au chargement Spark — `inferSchema` peut typer différemment de
pandas, voir règles de nettoyage documentées dans
`report/sections/06-spark-quality.tex`).

## Colonnes

| # | Colonne | Type observé | Nullable | Cardinalité / plage | Exemple |
|---|---|---|---|---|---|
| 1 | `job_id` | string | non | 1500 valeurs uniques | `AIJOB0001` |
| 2 | `job_title` | string | non | 25 valeurs distinctes | `AI Agent Developer` |
| 3 | `job_category` | string | non | 12 valeurs distinctes | `AI Engineering` |
| 4 | `experience_level` | string (catégorielle) | non | `Entry (0-2 yrs)`, `Mid (3-5 yrs)`, `Senior (6-9 yrs)`, `Lead (10+ yrs)` | `Senior (6-9 yrs)` |
| 5 | `years_of_experience` | int | non | 1 – 15 | `7` |
| 6 | `education_required` | string (catégorielle) | non | `Associate's`, `Bachelor's`, `Bootcamp/Self-taught`, `Master's`, `PhD` | `Master's` |
| 7 | `annual_salary_usd` | float | non | 90 000 – 384 000 | `239000.0` |
| 8 | `salary_min_usd` | int | non | 90 000 – 180 000 | `155000` |
| 9 | `salary_max_usd` | int | non | 180 000 – 320 000 | `290000` |
| 10 | `city` | string | non | 20 valeurs distinctes | `Boston` |
| 11 | `country` | string | non | 14 valeurs distinctes (voir liste ci-dessous) | `USA` |
| 12 | `remote_work` | string (catégorielle) | non | `On-site`, `Hybrid`, `Fully Remote` | `On-site` |
| 13 | `company_size` | string (catégorielle) | non | `Startup (1-50)`, `SME (51-500)`, `Mid-size (501-5000)`, `Enterprise (5000+)`, `Big Tech (FAANG+)` | `Startup (1-50)` |
| 14 | `industry` | string | non | 12 valeurs distinctes | `Finance` |
| 15 | `required_skills` | string | non | 1500 combinaisons (quasi uniques), séparateur `\|` | `APIs\|Planning Systems\|Python\|Cloud\|SQL\|Leadership` |
| 16 | `ai_salary_premium_pct` | float | non | 3.0 – 18.0 | `13.1` |
| 17 | `demand_score` | int | non | 68 – 98 | `96` |
| 18 | `demand_growth_yoy_pct` | float | non | 5.0 – 87.8 | `16.9` |
| 19 | `benefits_score_10` | float | non | 6.0 – 9.8 | `6.8` |
| 20 | `posting_year` | int | non | `2025`, `2026` | `2026` |
| 21 | `posting_month` | int | non | 1 – 12 | `3` |
| 22 | `is_senior` | int (booléen 0/1) | non | `0`, `1` | `1` |
| 23 | `is_remote_friendly` | int (booléen 0/1) | non | `0`, `1` | `0` |
| 24 | `is_llm_role` | int (booléen 0/1) | non | `0`, `1` | `1` |
| 25 | `salary_tier` | string (catégorielle) | non | `Entry (<$100k)`, `Mid ($100-150k)`, `Upper-Mid ($150-200k)`, `Senior ($200-300k)`, `Elite (>$300k)` | `Senior ($200-300k)` |

## `country` — les 14 valeurs

`Australia, Canada, China, France, Germany, Global, India, Japan,
Netherlands, Singapore, Switzerland, UAE, UK, USA`

Note : `Global` n'est pas un pays — probablement des postes remote sans
localisation précise. À documenter comme cas particulier dans les règles
de nettoyage (J3) plutôt qu'à corriger silencieusement (le dataset ne
permet pas de savoir ce que "Global" recouvre exactement).

## Contrôles de qualité effectués à l'inspection (pandas, hors Spark)

- `salary_min_usd <= salary_max_usd` : vérifié sur les 1500 lignes, 0
  violation
- `job_id` unique : vérifié, 0 doublon
- Lignes entièrement dupliquées : 0
- `required_skills` : aucun segment vide détecté après split sur `\|`
  (heuristique : pas de `||`, pas de `\|` en début/fin de chaîne)

Ces constats sont ceux d'un premier passage pandas sur le CSV brut — les
règles de nettoyage Spark définitives (J3,
`report/sections/06-spark-quality.tex`) doivent être revérifiées
indépendamment, `inferSchema` de Spark pouvant typer différemment.

## Colonnes utiles pour le modèle logique (offres / metiers / competences)

- **offres** (grain = 1 ligne/offre) : `job_id`, `job_title` (→
  `metier_id` par jointure), `experience_level`, `years_of_experience`,
  `education_required`, `annual_salary_usd`, `salary_min_usd`,
  `salary_max_usd`, `city`, `country`, `remote_work`, `company_size`,
  `industry`, `posting_year`, `posting_month`, `is_senior`,
  `is_remote_friendly`, `is_llm_role`, `salary_tier`,
  `ai_salary_premium_pct`, `demand_growth_yoy_pct`, `benefits_score_10`
  (ces 3 dernières varient par offre, voir plus bas)
- **metiers** (référentiel) : `job_title`, `job_category`,
  `demand_score` — **vérifié constant par `job_title`** (0 exception sur
  les 1500 lignes), donc légitimement des attributs du métier
- **restent dans `offres`, pas dans `metiers`** : `ai_salary_premium_pct`,
  `demand_growth_yoy_pct`, `benefits_score_10` — **vérifiés non constants
  par `job_title`** (jusqu'à 72 valeurs distinctes pour un même métier),
  donc des attributs propres à chaque offre malgré des noms qui pourraient
  suggérer un agrégat métier
- **competences** : `job_id` + `required_skills` (après `split('\|')` +
  `explode()`)
