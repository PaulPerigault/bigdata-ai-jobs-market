# Sujet officiel — synthèse complète

Source : `Projet_BigData_IA_Version_Etudiants_Marché de lemploi en IA
2025-2026.pdf`, M. Touati Zouhaier. Ce document remplace la lecture du PDF
— ne pas le rouvrir, tout le contenu utile est ici.

## Problématique

Quelles tendances du marché des emplois IA peut-on mettre en évidence à
partir des offres, des métiers, des compétences et des rémunérations ?

## Architecture attendue (imposée)

```
Dataset CSV
 -> HDFS /raw
 -> Spark : contrôle, nettoyage, transformation
 -> HDFS /processed { offres, metiers, competences }
 -> Hive / Spark SQL
 -> Zeppelin + Data Analytics Studio
 -> KPI, visualisations, conclusions métier
```

## Objectifs pédagogiques

- Organiser un espace HDFS en zones raw, processed et output
- Créer et vérifier des tables Hive externes
- Manipuler un DataFrame Spark et transformer des données
- Construire trois jeux de données : offres, metiers, competences
- Utiliser jointures et agrégations Hive SQL et Spark SQL
- Créer analyses et visualisations dans Zeppelin et Data Analytics Studio
- Interpréter les résultats sans généraliser au-delà du dataset

## Modèle logique cible

| Table | Rôle | Clé / liaison |
|---|---|---|
| offres | 1 ligne par offre d'emploi | job_id ; référence metier_id |
| metiers | Référentiel des métiers IA | metier_id |
| competences | Compétences demandées par offre | job_id + competence |

Les noms exacts de colonnes doivent être adaptés après inspection réelle du
CSV (voir `docs/dataset-schema.md`) — toute adaptation doit être documentée.

## JOUR 1 — Ingestion HDFS et première table Hive (très guidé)

**Exploration** : nom du fichier, lignes/colonnes, 10 premières lignes,
séparateur, en-tête, types probables, colonnes utiles, valeurs
manquantes/incohérentes.

**Arborescence HDFS** :
```
/projet_ia/
├── raw/
├── processed/{offres,metiers,competences}/
└── output/
```
Créée avec `hdfs dfs -mkdir -p`, CSV déposé dans `/projet_ia/raw`,
contrôlé (`-ls`, `-du`, `-cat`/`head`, `wc -l`).

**Table Hive RAW** — squelette imposé :
```sql
CREATE EXTERNAL TABLE ai_jobs_raw (
  -- colonnes à compléter
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/projet_ia/raw'
TBLPROPERTIES ('skip.header.line.count'='1');
```
Contrôles obligatoires : `SHOW TABLES`, `DESCRIBE ai_jobs_raw`,
`SELECT * ... LIMIT 10`, `COUNT(*)`.

**Mini-analyse Jour 1 (5 requêtes obligatoires)** :
1. Nombre d'offres
2. Nombre de métiers distincts
3. Nombre de pays distincts
4. Salaire annuel moyen, minimum et maximum
5. Répartition des offres par niveau d'expérience

**Livrable J1** : captures des étapes importantes + commandes HDFS +
CREATE TABLE + 5 requêtes + commentaire de 5 à 10 lignes.

## JOUR 2 — Spark, transformation, modèle analytique (semi-guidé)

**Chargement** :
```python
df = spark.read.option("header","true").option("inferSchema","true").csv("/projet_ia/raw/...csv")
df.printSchema()
df.show(10, truncate=False)
```

**Nettoyage** : compter lignes/doublons, contrôler NULL des colonnes
importantes, vérifier types (salaires, années), corriger seulement si
justifié, documenter toutes les règles appliquées.

**Construction des 3 tables** :
1. **offres** : 1 ligne/offre, job_id, metier_id + attributs (expérience,
   salaire, pays, ville, secteur, télétravail, taille entreprise, date...)
2. **metiers** : 1 ligne/métier distinct, metier_id stable, attributs
   métier pertinents
3. **competences** : `split()` + `explode()` de `required_skills`
   (exemple : `JOB001 | Python|Spark|SQL` -> 3 lignes)

Écriture dans `/processed`, création des tables Hive correspondantes,
vérification lignes/clés/exemples.

**Requêtes obligatoires Jour 2 (n°6 à 13)** :
6. Top 10 métiers par nombre d'offres
7. Salaire moyen par métier
8. Top 10 compétences les plus demandées
9. Salaire moyen par niveau d'expérience
10. Nombre d'offres par pays et secteur
11. Jointure offres ↔ metiers
12. Jointure offres ↔ competences
13. Requête GROUP BY + HAVING

**Livrable J2** : notebook Spark/Zeppelin, schéma des 3 tables, règles de
transformation, requêtes et résultats commentés.

## JOUR 3 — Analytics, Zeppelin, Data Analytics Studio (autonome)

**KPI obligatoires (n°14 à 23)** :
14. Nombre total d'offres et de métiers
15. Salaire moyen et médian (si l'environnement le permet)
16. Top métiers les mieux rémunérés
17. Top métiers les plus demandés
18. Top compétences demandées
19. Salaire moyen par pays
20. Salaire par niveau d'expérience
21. Répartition télétravail / présentiel (si disponible)
22. Analyse des métiers LLM/GenAI (si l'information existe)
23. Évolution 2025-2026 ou par période

**4 analyses au choix parmi** : compétences associées aux hauts salaires ;
différences par secteur ; entreprise/taille et salaire ; pays et
compétences ; métiers en forte croissance ; prime salariale IA ;
comparaison LLM vs autres métiers ; relation expérience-salaire.

**Dashboard** : minimum 6 visualisations (KPI synthétiques, bar chart,
répartition, évolution temporelle, + 2 au choix). Chaque graphique : titre,
requête identifiable, interprétation.

**Analyse finale** : 6 à 10 conclusions chiffrées + 3 recommandations.
Distinguer : ce que montre le dataset / interprétation / ce qui ne peut pas
être affirmé.

## Livrables finaux (rappel global)

- Rapport PDF structuré (12 à 18 pages hors annexes selon la trame
  officielle — voir `report/rapport.tex`)
- Notebook(s) Zeppelin exporté(s) ou captures lisibles
- Scripts/requêtes Hive SQL et Spark/PySpark
- Captures HDFS et tables Hive
- Schéma des trois tables
- Dashboard final et conclusions

## Barème /20

| Critère | Points |
|---|---|
| HDFS et organisation des données | 2 |
| Hive RAW + tables processed | 3 |
| Spark : contrôle/nettoyage/transformation | 4 |
| Modèle offres-métiers-compétences | 3 |
| Hive SQL / Spark SQL et jointures | 3 |
| Zeppelin / DAS et visualisations | 3 |
| Analyse, recul critique et qualité du rapport | 2 |
| **Total** | **20** |

## Dataset — description officielle

> Un ensemble de données complet de 1 500 offres d'emploi en IA et
> apprentissage automatique de 2025 à 2026, couvrant 25 postes répartis
> dans 14 pays. Conçu pour les data scientists, ingénieurs en apprentissage
> automatique, étudiants et chercheurs de carrière qui souhaitent
> comprendre le marché de l'emploi en IA en évolution rapide — salaires,
> compétences en demande, tendances du télétravail et répartition de la
> taille des entreprises.

Schéma technique exact (25 colonnes) : voir `CLAUDE.md` section Dataset, ou
`data/ai_jobs_market_2025_2026.csv` directement.
