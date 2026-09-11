# Projet Big Data — Marché de l'emploi en IA 2025-2026

## Objectif double

Ce projet a deux finalités qui coexistent et ne doivent jamais être sacrifiées
l'une pour l'autre :

1. **Projet académique noté** (ESIEA, sujet de M. Touati Zouhaier) — barème /20,
   deadline **lundi 21 septembre 2026, 23:59**.
2. **Démonstrateur DevSecOps/Cloud personnel** — infra k3d, best practices,
   interface web, à but de portfolio/apprentissage.

Quand un choix technique doit trancher entre "plus simple pour la note" et
"plus proche des best practices pro", privilégier la solution pragmatique qui
satisfait les deux, jamais sacrifier le premier point pour le second.

## Contraintes académiques non négociables

Le rapport final doit suivre la trame imposée (15 sections, voir
`docs/trame-rapport.md` si présent) et les livrables suivants sont **requis
pour la note**, quelle que soit l'infra choisie :

- Arborescence HDFS : `/projet_ia/raw`, `/processed/{offres,metiers,competences}`,
  `/output`
- Table Hive externe RAW (`CREATE EXTERNAL TABLE`, TEXTFILE, header skip)
- Chargement + nettoyage du DataFrame Spark (NULL, doublons, types) avec règles
  de nettoyage documentées et justifiées
- 3 tables construites : **offres** (grain = 1 ligne/offre), **metiers**
  (référentiel, `metier_id` stable), **competences** (1 ligne par
  offre×compétence, via `split()` + `explode()` sur `required_skills`)
- Requêtes obligatoires Jour 1 (5 requêtes), Jour 2 (requêtes 6 à 13, incluant
  2 jointures + 1 GROUP BY/HAVING), Jour 3 (KPI 14 à 23)
- Au moins 4 analyses supplémentaires au choix (Jour 3)
- **Dashboard Zeppelin et/ou Data Analytics Studio** : minimum 6
  visualisations, chacune avec titre, requête identifiable, interprétation
  chiffrée — **non négociable, explicitement demandé par le sujet, ne pas
  remplacer par Jupyter/Voilà**
- Rapport final structuré suivant la trame officielle (15 sections exactes,
  voir `docs/sujet-synthese.md` et `report/rapport.tex` qui l'implémente
  déjà) — volume conseillé **12 à 18 pages hors annexes** (trame docx,
  fait foi sur le chiffre du PDF sujet qui indiquait 10-15)

Distinguer systématiquement, dans toute analyse : ce que montre le dataset, ce
qui relève de l'interprétation, et ce que le dataset ne permet pas d'affirmer.

## Stack technique arrêté

| Couche | Choix | Non-goals explicites |
|---|---|---|
| Cluster | k3d (Docker), local, jetable | Pas de VPS, pas d'infra permanente |
| Stockage | HDFS (NameNode/DataNode StatefulSet + PVC) | — |
| Métastore | Hive Metastore + HiveServer2 (Postgres backend) | — |
| Traitement | Spark on k8s (Spark Operator), **PySpark** | Pas de Scala |
| Dev interactif | Jupyter (kernel PySpark connecté au cluster) pour l'exploration | — |
| Prod pipeline | Scripts PySpark versionnés (repo Git) — version finale propre à partir de l'exploration Jupyter | — |
| Dashboard académique | Zeppelin (+ DAS si le temps le permet) | Obligatoire, ne pas retirer |
| Interface perso | Notebook Jupyter → **Voilà** → app web conteneurisée, derrière ingress k3s | Pas de Go, pas de Streamlit/Dash (tranché) |
| Sécu | NetworkPolicies namespace `bigdata`, secrets via Sealed Secrets/SOPS, scan Trivy en CI, RBAC minimal | Pas de Vault, pas d'ArgoCD, pas de stack sécu complet — pragmatique assumé |
| CI | GitHub Actions : `pre-commit` rejoué, tests unitaires, scan manifests, scan images | — |
| Tests | Voir `docs/TESTING.md` — unitaires (obligatoire, CI), qualité données (manuel), pas d'intégration cluster en CI | — |
| Rapport | **LaTeX**, multi-fichiers (`report/rapport.tex` = squelette +
`\input`, contenu réel dans `report/sections/`), compilé avec `tectonic`
(`task report:build`) | Pas de Word/docx, pas un seul fichier monolithique
(conflits de merge à 5) |

## Équipe (5 personnes)

Répartition par rôle/label plutôt que nominative pour l'instant (pseudos
GitHub à assigner plus tard) — voir `docs/team-roles.md` pour le détail
complet des responsabilités de chaque rôle :

- `team:infra` — k3d, HDFS, Hive, Spark Operator, sécurité, CI infra
- `team:data-eng` — nettoyage Spark, construction des 3 tables, scripts
  PySpark, tests unitaires
- `team:analytics` — requêtes Hive/Spark SQL, KPI, dashboard Zeppelin, Voilà
- `team:insights` — analyses au choix, LLM/GenAI, synthèse, recommandations
- `team:docs-qa` — rédaction des sections du rapport, captures d'écran,
  tests de qualité de données, matrice de vérification finale

## Workflow issue → branche → PR

Chaque tâche = une issue (granularité fine, voir `docs/issues-seed.yml`).
Pour chaque issue : brancher via `gh issue develop <numéro> --checkout`
(lie automatiquement la branche à l'issue côté GitHub), nommer la branche
selon `docs/CONTRIBUTING.md`, ouvrir une PR qui `Closes #<numéro>`. Pas de
push direct sur `main` — protection de branche à activer (PR obligatoire +
checks CI verts) dès le repo GitHub en place.

## Idées et notes en cours de route

Si une idée/point à creuser surgit pendant le travail sur une issue et
qu'elle ne rentre pas dans le rapport tout de suite : créer un fichier dans
`docs/notes/` (convention : `docs/notes/<slug>.md`) plutôt que la perdre ou
la caser de force ailleurs. Ces notes sont la matière brute qui alimente
ensuite `report/sections/`, elles ne remplacent pas le rapport.

## Autonomie sur les skills

Claude Code est autonome sur le choix et l'usage des skills/outils
disponibles (graphify inclus) — pas besoin de demander confirmation avant
d'utiliser un skill pertinent. La confirmation explicite de Paul reste
requise uniquement pour les actions qui modifient l'état du cluster k3d
(règle d'or ci-dessous), pas pour l'usage d'un skill.

## Captures d'écran (annexes du rapport)

Le cluster k3d est jetable — les captures doivent être prises **au fur et à
mesure de chaque jour**, pas reconstituées à la fin. Convention :
`docs/screenshots/J<N>-<slug>.png` (ex. `J2-hdfs-ls.png`,
`J6-zeppelin-dashboard.png`). Inclut aussi des captures GitHub (Project
board, issues, CI verte, scan Trivy) pour la partie DevSecOps du portfolio.

## Structure de repo (proposition)

```
.
├── CLAUDE.md
├── docs/
│   ├── trame-rapport.md
│   ├── dataset-schema.md
│   └── architecture.md
├── infra/
│   ├── k3d/              # config cluster
│   ├── manifests/        # HDFS, Hive, Spark Operator, Zeppelin, ingress
│   └── security/         # NetworkPolicies, secrets templates
├── spark-jobs/
│   ├── notebooks/        # exploration Jupyter
│   └── scripts/          # PySpark versionné (version finale)
├── voila-app/
│   └── dashboard.ipynb
└── report/
    ├── rapport.tex        # squelette + \input, compilé via `task report:build`
    └── sections/          # une section = un fichier .tex (voir docs/sujet-synthese.md)
```

## Planning (12 jours restants au 09/09/2026)

| Jour | Notation | Infra / Web |
|---|---|---|
| J1 | — | Repo Git, scaffolding k3d, structure du projet |
| J2 | HDFS raw/processed/output + table Hive RAW | Déploiement HDFS + Hive Metastore sur k3d |
| J3 | Spark : chargement, nettoyage, contrôle qualité | Spark Operator déployé ; exploration Jupyter démarrée |
| J4-J5 | 3 tables offres/metiers/competences + requêtes Jour 2 | Scripts PySpark finaux versionnés à partir de l'exploration Jupyter |
| J6 | Démarrage Zeppelin | Zeppelin déployé (Spark+Hive) ; notebook Voilà démarré |
| J7 | KPI Jour 3 obligatoires (14-23) | Voilà branché aux résultats Hive, ingress k3s |
| J8 | 4 analyses au choix, dashboard 6+ visualisations | Finalisation Voilà |
| J9 | — | Durcissement sécu (NetworkPolicies, secrets, scan CI) |
| J10 | Rédaction rapport sections 9-14 | README technique du repo |
| J11 | Polish rapport, annexes | Polish Voilà, captures |
| J12 | Relecture vs matrice de vérification | Buffer |
| J13 (dépôt) | Soumission | — |

## Dataset — `ai_jobs_market_2025_2026.csv`

1500 lignes, 25 colonnes. Colonnes principales :

`job_id, job_title, job_category, experience_level, years_of_experience,
education_required, annual_salary_usd, salary_min_usd, salary_max_usd, city,
country, remote_work, company_size, industry, required_skills,
ai_salary_premium_pct, demand_score, demand_growth_yoy_pct, benefits_score_10,
posting_year, posting_month, is_senior, is_remote_friendly, is_llm_role,
salary_tier`

- `required_skills` : liste de compétences séparées par `|` → source pour
  `split()`/`explode()` de la table `competences`
- `posting_year`/`posting_month` : permet l'analyse d'évolution 2025→2026
- `is_llm_role` : flag dédié pour l'analyse métiers LLM/GenAI demandée par le
  sujet
- 25 métiers distincts, 14 pays distincts (annoncés dans la description du
  jeu de données)

## Conventions

- Code (Python, YAML, noms de variables, commits) : anglais
- Rapport, documentation projet, commentaires métier : français
- Pas de credentials en clair dans les manifests, même en local/jetable

## Outillage déjà en place (ne pas recréer)

- `.pre-commit-config.yaml`, `.editorconfig`, `.gitattributes`, `.gitignore`
  (distinction fine JetBrains — voir historique)
- `Taskfile.yml` (`task setup|lint|test|test:data|format|report:build|k3d:up|k3d:down`)
- `.github/workflows/ci.yml` (branch-name-check, pr-title-check, pre-commit,
  test, scan-images, manifest-lint)
- `.github/ISSUE_TEMPLATE/` (academic-deliverable, infra-task, bug),
  `PULL_REQUEST_TEMPLATE.md`
- `docs/CONTRIBUTING.md` (conventions branches/commits/labels)
- `docs/TESTING.md` (politique de tests, 3 niveaux)
- `docs/sujet-synthese.md` (synthèse complète du PDF sujet — ne jamais
  rouvrir le PDF original, tout est ici)
- `report/rapport.tex` (structure exacte de la trame docx officielle, déjà
  implémentée avec tous les tableaux à remplir — ne pas réordonner/modifier
  la structure des sections) + `report/sections/*.tex` (16 fichiers, un par
  section, `\input`és depuis rapport.tex)
- `docs/team-roles.md` (les 5 rôles et leurs responsabilités)
- `docs/notes/` (convention pour capturer les idées en cours de route)
- `docs/issues-seed.yml` (issues à créer, granularité fine, prêtes à scripter)
- `docs/project-board.md` (spec du GitHub Project)
- `docs/prompts/` (prompts Claude Code séquencés : 01-github-setup,
  02-report-check, 03-j1-infra-bootstrap)
- `docs/sujet/` (originaux PDF/docx volontairement non committés — voir son
  README)
- `data/ai_jobs_market_2025_2026.csv` (dataset, committé — petit fichier,
  public, nécessaire à la reproductibilité)
- `LICENSE` (MIT), `SECURITY.md`, `README.md`
- `graphify` installé (knowledge graph du repo, se met à jour tout seul via
  hook post-commit)

## Règle d'or

Ne rien exécuter/déployer sans validation explicite de Paul au préalable pour
chaque étape structurante du planning.
