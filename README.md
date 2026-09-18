# Marché de l'emploi en IA 2025-2026 — Projet Big Data ESIEA

Projet pédagogique ESIEA (module Fondamentaux du Big Data, sujet
proposé par M. Touati Zouhaier) : construire une chaîne Big Data
complète pour analyser le marché de l'emploi en IA 2025-2026 à partir
du dataset `ai_jobs_market_2025_2026.csv` (1500 lignes, 25 colonnes).

- **Équipe** : 5 personnes, travail en parallèle sur ce dépôt.
- **Deadline** : 21/09/2026.
- **Suivi** : [`STATUS.md`](STATUS.md) (état réel du projet),
  [`JOURNAL.md`](JOURNAL.md) (journal d'exécution append-only),
  [`CLAUDE.md`](CLAUDE.md) (règles et décisions techniques détaillées),
  [Project board GitHub](https://github.com/users/PaulPerigault/projects/9).

## Architecture

```
CSV (data/raw/) → HDFS /projet_ia/raw
                 → Spark : contrôle, nettoyage, transformation
                 → HDFS /projet_ia/processed/{offres,metiers,competences}
                 → Hive (tables externes RAW + processed)
                 → Jupyter/PySpark (exploration, requêtes Hive SQL/Spark SQL, dashboard)
```

Stack orchestrée via Docker Compose (`compose.yaml` +
`compose.override.yaml`) : HDFS (namenode/datanode), Hive (metastore +
server, Postgres), Jupyter/PySpark. Détails et justification de chaque
choix d'image dans `CLAUDE.md`.

## Prérequis (versions vérifiées, pas génériques)

**Docker seul suffit.** Toutes les commandes (`up`, `ingest`, `etl`,
`test`, `report`, ...) passent par `./run` (voir plus bas), un wrapper
qui exécute `task` dans un conteneur jetable — pas besoin d'installer
go-task, Python ou Java sur la machine hôte pour suivre ce README.

- **Docker + Docker Compose v2** (le plugin intégré `docker compose`,
  pas l'outil autonome `docker-compose` v1) — vérifié avec Docker
  Engine 29.8.1 / Compose plugin v5.5.1. Sur Apple Silicon, la stack a
  été validée via [colima](https://github.com/abiosoft/colima)
  (`brew install colima docker-compose`) plutôt que Docker Desktop —
  voir `CLAUDE.md` pour le détail (Docker Desktop peut fonctionner
  aussi, non testé spécifiquement sur ce projet).
- **RAM allouée au moteur Docker : 8 Go minimum**, validée réellement
  via `colima start --cpu 4 --memory 8 --disk 60`. À titre indicatif,
  la somme des `deploy.resources.limits.memory` des 6 services
  (`compose.yaml`) représente **~10,6 Go** (namenode 1,5 + datanode 1,5
  + hive-metastore-postgresql 0,5 + hive-metastore 1,5 + hive-server
  1,5 + jupyter 4) : ce sont des plafonds par conteneur, pas la RAM
  réellement consommée en simultané (d'où le fait que 8 Go suffisent en
  pratique), mais ne descendez pas en dessous sans marge si votre
  machine tourne d'autres services lourds en parallèle.

Si vous avez déjà [`go-task`](https://taskfile.dev/) installé
nativement (`brew install go-task`), `task X` fonctionne directement en
plus de `./run X` — les deux sont strictement équivalents, `./run` est
juste ce qui marche pour tout le monde sans installation préalable.
`task setup` et `task lint` (hooks git / pre-commit) restent une
exception : ce sont des opérations qui configurent votre dépôt Git
local, elles doivent tourner nativement (Python + `pip install
pre-commit`), containeriser n'aurait pas de sens ici.

## Démarrage — de zéro à ça marche

Parcours testé dans cet ordre exact. Ne sautez pas d'étape : chacune
dépend de la précédente.

**1. Cloner le dépôt**

```bash
git clone https://github.com/PaulPerigault/bigdata-ai-jobs-market.git
cd bigdata-ai-jobs-market
```

**2. Récupérer le dataset (non fourni dans le dépôt)**

Le CSV `ai_jobs_market_2025_2026.csv` est **volontairement absent du
dépôt** (`data/raw/` est gitignored, voir `.gitignore` et
`SECURITY.md`). Sans cette étape, `./run ingest` échouera avec un
fichier introuvable.

- Télécharger le dataset **AI Jobs Market 2025-2026 | Salaries** sur
  Kaggle : <https://www.kaggle.com/datasets/alitaqishah/ai-jobs-market-2025-2026-salaries>
  (compte Kaggle gratuit requis pour télécharger).
- Placer le fichier CSV extrait à l'emplacement exact attendu :

  ```bash
  mkdir -p data/raw
  mv ~/Downloads/ai_jobs_market_2025_2026.csv data/raw/ai_jobs_market_2025_2026.csv
  ```

  Le nom de fichier doit être exactement `ai_jobs_market_2025_2026.csv`
  (c'est le nom que `scripts/01_ingest_hdfs.sh` référence directement) —
  renommez-le si l'archive Kaggle le nomme différemment.

**3. Configurer l'environnement**

`./run up` copie automatiquement `.env.example` vers `.env` s'il est
absent (voir la recette `up` dans `Taskfile.yml`) — vous n'êtes donc
**pas bloqué** si vous oubliez cette étape. Mais si vous voulez
personnaliser un identifiant avant le premier démarrage (rare, les
valeurs par défaut suffisent pour un usage local), faites-le vous-même
avant `./run up` :

```bash
cp .env.example .env
```

**4. Démarrer la stack**

```bash
./run up
```

Démarre HDFS (namenode/datanode), Hive (metastore + server, Postgres)
et Jupyter/PySpark via Docker Compose. Premier démarrage lent (images à
télécharger, plusieurs Go — `./run` construit aussi sa propre petite
image la première fois, quelques secondes) ; les démarrages suivants
sont rapides (images/volumes déjà en cache). Vérifiez que les 6
services sont `healthy` :

```bash
docker compose ps
```

Sous émulation (Apple Silicon via colima/QEMU), il arrive que
`datanode` crashe au tout premier démarrage (`exited (139)`,
segfault JVM pendant le JIT — voir `JAVA_TOOL_OPTIONS=-Xint` dans
`CLAUDE.md`) : relancez simplement `./run up`, ça repart sans
intervention. Si `./run up` remonte une erreur de dépendance
(`dependency datanode failed to start`), c'est ce cas.

**5. Ingérer le CSV dans HDFS**

```bash
./run ingest
```

Dépose le CSV dans `/projet_ia/raw` sur HDFS et vérifie le dépôt
(`ls`/`du`/`wc -l`, 1500 lignes de données + 1 en-tête attendues).

**6. Lancer le pipeline ETL Spark**

```bash
./run etl
```

Nettoie, transforme et écrit les tables `offres`/`metiers`/`competences`
sur HDFS (`/projet_ia/processed/`) puis les expose comme tables Hive
externes (base `processed`).

**7. Lancer les tests**

```bash
./run test
```

Tests unitaires (`tests/unit/`, Spark local `local[2]`), exécutés dans
un conteneur `jupyter/pyspark-notebook` jetable — aucun Python/Java
local requis, aucun risque de version incompatible. Ne nécessite pas la
stack Docker démarrée, peut être lancé indépendamment des étapes 4-6.

**8. Compiler le rapport**

```bash
./run report
```

Compile `report/main.tex` en PDF via un conteneur XeLaTeX pinné —
aucune installation LaTeX locale requise. Résultat dans
`report/main.pdf`.

## Le wrapper `./run`

`./run` (script POSIX à la racine, exécutable) construit une image
Docker minimale (`Dockerfile.runner` : go-task + CLI Docker, rien
d'autre — pas un service qui tourne en fond, un conteneur jetable par
appel) et y exécute `task "$@"`, en montant le dépôt et le socket
Docker de l'hôte. Résultat : personne n'a besoin d'installer go-task
pour utiliser ce projet, seul Docker est requis. `./run X` et `task X`
sont équivalents — utilisez celui que vous avez.

Voir `SECURITY.md` pour le compromis de sécurité assumé du montage du
socket Docker (usage local uniquement, jamais à reproduire dans un
contexte qui exécute du code non maîtrisé).

## Utilisation — Taskfile (référence complète)

Toutes les commandes passent par `./run` (ou `task` en local) :

| Commande | Rôle |
|---|---|
| `./run setup` \* | Installe les dépendances locales (pre-commit). |
| `./run up` | Démarre la stack Docker Compose (HDFS, Hive, Jupyter) — copie `.env.example` en `.env` si absent. |
| `./run down` | Arrête la stack. |
| `./run ingest` | Dépose le CSV brut dans HDFS (`/projet_ia/raw`). |
| `./run etl` | Lance le pipeline Spark : nettoyage + écriture des tables `offres`/`metiers`/`competences` sur HDFS et Hive. |
| `./run test` | Exécute les tests unitaires (`tests/unit/`, Spark local, conteneur jetable). |
| `./run hive-shell` | Ouvre un shell Beeline connecté à HiveServer2. |
| `./run jupyter` | Affiche l'URL du notebook Jupyter/PySpark. |
| `./run report` | Compile le rapport LaTeX (`report/main.tex`) via Docker, sans dépendance LaTeX locale. |
| `./run screenshots-cli` | Régénère les captures de commandes CLI (Hive/Spark) pour le rapport. |
| `./run screenshots-web` | Régénère les captures d'interfaces web (HDFS NameNode, Jupyter) pour le rapport. |
| `./run lint` \* | Lance `pre-commit run --all-files` (ruff, sqlfluff, gitleaks). |

\* `setup` et `lint` configurent des hooks Git sur votre dépôt local —
ils ont besoin de Python/`pip` nativement (`pip install pre-commit`),
containeriser n'aurait pas de sens pour une opération qui modifie
`.git/hooks`. Toutes les autres commandes ne nécessitent que Docker.

## Structure du dépôt

```
compose.yaml, compose.override.yaml   # stack Docker (services de base + overrides dev)
Taskfile.yml                          # point d'entrée des commandes
run, Dockerfile.runner                # wrapper Docker pour task (aucune install go-task requise)
scripts/                              # ingestion HDFS, captures d'écran
sql/hive/                             # DDL RAW, requêtes d'analyse, KPI
src/etl/                              # schéma, nettoyage, construction des tables (Spark)
src/etl_pipeline.py                   # point d'entrée task etl (spark-submit)
src/*.ipynb                           # notebook Jupyter/PySpark (exploration, dashboard)
tests/unit/                           # sanity checks Spark local (pytest)
report/                               # rapport LaTeX modulaire (main.tex + preamble/ + chapters/)
data/raw/                             # CSV brut (gitignored, jamais commité)
```

## Modèle de données

Trois tables construites par le pipeline ETL et exposées dans Hive
(base `processed`) :

- **`offres`** : une ligne par offre d'emploi (`job_id`, `metier_id`
  FK, salaire, expérience, localisation, etc.).
- **`metiers`** : une ligne par `job_title` distinct (`metier_id` en
  hash déterministe `sha2(job_title, 256)`, pas d'ID auto-incrémenté
  instable).
- **`competences`** : une ligne par couple `job_id`/compétence, issue
  de l'explosion de `required_skills`.

Détails et chiffres réels dans `report/chapters/07_construction_tables.tex`.

## Rapport

Le rapport final (LaTeX, couleurs ESIEA) vit dans `report/` :
`main.tex` + `preamble/` (charte graphique) + `chapters/` (un fichier
par chapitre). Compilation via `./run report` (XeLaTeX dans un
conteneur Docker pinné, aucune dépendance LaTeX locale requise).

## Conventions de contribution

- Commits [Conventional Commits](https://www.conventionalcommits.org/)
  (`feat:`, `fix:`, `docs:`, `test:`, `chore:`).
- `pre-commit run --all-files` obligatoire avant tout push (ruff,
  sqlfluff, gitleaks) — jamais un run scopé aux fichiers touchés.
- Transformations Spark versionnées en scripts `.py` dans `src/etl/`,
  pas seulement écrites dans le notebook.
- Voir `CLAUDE.md` pour l'ensemble des règles et décisions techniques
  détaillées (images Docker pinnées, choix d'architecture, bugs
  rencontrés et corrigés).
