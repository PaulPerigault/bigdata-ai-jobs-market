# STATUS.md — Suivi du projet

> Document vivant. Reflète l'état réel du repo, pas le plan initial.
> Mis à jour à chaque étape (voir règle de maintenance en bas de fichier).
> Dernière mise à jour : cf. dernier commit touchant ce fichier.

## Vue d'ensemble

- **Sujet** : Marché de l'emploi en IA 2025-2026 — HDFS/Hive/Spark/Jupyter
- **Barème** : /20 — HDFS (2) · Hive RAW+processed (3) · Spark nettoyage (4)
  · modèle offres-métiers-compétences (3) · Hive SQL/Spark SQL (3)
  · visualisations (3) · analyse et rapport (2)
- **Deadline** : 21/09/2026
- **Repo** : ~/PycharmProjects/bigdata-ai-jobs-market (branche main)
- **GitHub Project** : [Big Data AI Jobs — Roadmap](https://github.com/users/PaulPerigault/projects/9)
  (colonnes Backlog/Todo/In Progress/In Review/Done, existait déjà et
  s'alimente automatiquement via le workflow `project-status-sync.yml`
  — statuts alignés manuellement le 16/09/2026 sur les règles ci-dessous).

## État actuel — ce qui est FAIT et vérifié en conditions réelles

### Infra (Étape 1) ✅
- [x] `compose.yaml` + `compose.override.yaml` : HDFS (namenode/datanode
      bde2020 2.7.4), Hive (metastore+server bde2020 2.3.2, Postgres
      metastore), Jupyter/PySpark 3.5.0. Images pinnées, healthchecks,
      `depends_on: condition: service_healthy`.
- [x] Ports publiés sur `127.0.0.1` uniquement (corrigé suite scan
      sécurité automatique — étaient sur `0.0.0.0`).
- [x] `GRANT_SUDO` retiré du conteneur `jupyter` (inutile, surface
      d'attaque réduite — jamais appliqué aux conteneurs Hadoop).
- [x] `Taskfile.yml` : `up`, `down`, `ingest`, `etl`, `test`,
      `hive-shell`, `jupyter` — chacune loggue dans `JOURNAL.md`.
- [x] `.pre-commit-config.yaml` : gitleaks, sqlfluff (dialecte Hive),
      ruff (lint + format — pas de black, ruff fait les deux).
- [x] `.github/workflows/ci.yml` : job `lint` (pre-commit) + `test`
      (pytest, Spark local, sans dépendance à la stack Compose).
- [x] `CLAUDE.md` tenu à jour en continu (tags d'images, décisions,
      section "Definition of Done" ajoutée).
- [x] Stack vérifiée healthy 6/6 services en conditions réelles.

### Pipeline de données (Étape 2) ✅
- [x] Ingestion HDFS `/projet_ia/raw` (CSV, 1500 lignes confirmées).
- [x] Table Hive RAW `ai_jobs_raw` créée — **bug corrigé** :
      `spark.sql` sur la table Hive ignorait `skip.header.line.count`
      (1501 lignes au lieu de 1500) ; contournement par
      `spark.read.csv(header=True)` direct sur HDFS.
- [x] Table `offres` : 1500 lignes, 0 doublon `job_id`.
- [x] Table `metiers` : 25 métiers distincts, `metier_id` corrigé en
      hash déterministe (plus de `monotonically_increasing_id()`).
- [x] Table `competences` : 9548 liaisons job↔compétence (chiffre exact,
      pas une approximation).
- [x] Écriture HDFS `/projet_ia/processed/{offres,metiers,competences}`
      + tables Hive externes correspondantes.
- [x] Comptages NULLs/doublons avant-après nettoyage, chiffrés et
      documentés (chapitre 06 du rapport).
- [x] Jointure offres↔métiers vérifiée via Beeline (ex. LLM Engineer :
      75 offres, salaire moyen ~240 960$).

### Issues rétroactives (travail déjà fait, tracé après coup)
Créées et fermées le 16/09/2026 pour que l'historique complet du projet
soit visible dans les issues, pas seulement ce qu'il reste à faire —
chacune renvoie vers le commit exact qui la clôt :
- [x] [#105](https://github.com/PaulPerigault/bigdata-ai-jobs-market/issues/105)
      infra bootstrap Docker Compose — commit `80dd76a`.
- [x] [#106](https://github.com/PaulPerigault/bigdata-ai-jobs-market/issues/106)
      pipeline de données RAW → processed — commit `1737b51`.
- [x] [#107](https://github.com/PaulPerigault/bigdata-ai-jobs-market/issues/107)
      restructuration du rapport en fichiers séparés — commit `517fb9a`.
- [x] [#108](https://github.com/PaulPerigault/bigdata-ai-jobs-market/issues/108)
      mise en place de la CI — commit `80dd76a` (même commit que #105).
- [x] [#109](https://github.com/PaulPerigault/bigdata-ai-jobs-market/issues/109)
      corrections de sécurité (ports, GRANT_SUDO) — commit `1737b51`
      (même commit que #106).

### Requêtes Hive SQL / Spark SQL (Étape 3, partiel) ✅
- [x] **[#103](https://github.com/PaulPerigault/bigdata-ai-jobs-market/issues/103)**
      Jointure offres↔competences dédiée (`sql/hive/01_analyses.sql`) :
      top compétence = Python (942 offres, 63% du dataset).
- [x] Requête `GROUP BY` + `HAVING` : 12 pays avec >50 offres et salaire
      moyen >150 000$, USA en tête (515 offres, 226 190$).
- [x] Comparaison Hive SQL vs Spark SQL (même requête, salaire moyen par
      expérience) : résultats identiques, Spark SQL 3-4x plus rapide
      (chiffres exacts variables d'un run à l'autre sous émulation QEMU
      — 57s/15s et 33,0s/8,8s mesurés sur deux runs distincts) —
      chiffré et documenté (chapitre 08).

### Captures d'écran automatisées (Étape 3) ✅
- [x] **[#101](https://github.com/PaulPerigault/bigdata-ai-jobs-market/issues/101)**
      `task screenshots-cli` (freeze) et `task screenshots-web`
      (Playwright) régénèrent à la demande les 9 captures de
      `report/figures/` intégrées aux chapitres 03/05/08/09. Captures
      GitHub authentifiées volontairement laissées manuelles (voir note
      du ticket ci-dessous et CLAUDE.md).

### KPI obligatoires Jour 3 (Étape 3) ✅
- [x] **[#94](https://github.com/PaulPerigault/bigdata-ai-jobs-market/issues/94)**
      Les 10 KPI obligatoires calculés via `sql/hive/02_kpis.sql` et
      documentés au chapitre 09 : total 1500 offres/25 métiers, salaire
      moyen 194 892$/médian 179 421$, métier le mieux rémunéré AI
      Solutions Architect (251 577$), le plus demandé LLM Engineer (75
      offres), compétence la plus demandée Python (942 offres), pays le
      mieux rémunéré USA (226 190$), Hybrid dominant (45,7%), écart
      LLM/GenAI documenté sans sur-interprétation causale, pic d'activité
      février 2026 (306 offres, ~5x le volume mensuel 2025 — signalé
      comme constat descriptif, repris au chapitre 13 limites).

### Rapport LaTeX ✅ (partiel)
- [x] Restructuré en `report/main.tex` + `report/preamble/` +
      `report/chapters/*.tex` (15 chapitres), polices Roboto/Poppins
      versionnées (pas de dépendance système).
- [x] Compile réellement en XeLaTeX, 0 erreur, PDF 26 pages.
- [x] Chapitres rédigés avec résultats réels : **03** (architecture +
      3 corrections sécurité), **04** (ingestion, bug 1501 lignes),
      **05** (DDL Hive + bug header), **06** (nulls/doublons), **07**
      (fix metier_id + chiffres tables), **08** (jointures
      offres↔metiers/competences, GROUP BY+HAVING, comparaison
      Hive/Spark SQL), **09** (10 KPI obligatoires Jour 3, chiffres
      réels) — Étapes 2 et 3.
- [ ] Chapitres encore en placeholder : **01** (introduction), **02**
      (présentation dataset), **10** à **15** (4 analyses au choix,
      dashboard, synthèse, recommandations, limites, conclusion,
      annexes) — restent liés aux tickets
      [#95](https://github.com/PaulPerigault/bigdata-ai-jobs-market/issues/95),
      [#96](https://github.com/PaulPerigault/bigdata-ai-jobs-market/issues/96),
      [#97](https://github.com/PaulPerigault/bigdata-ai-jobs-market/issues/97),
      [#98](https://github.com/PaulPerigault/bigdata-ai-jobs-market/issues/98),
      [#99](https://github.com/PaulPerigault/bigdata-ai-jobs-market/issues/99).

## Ce qu'il reste à faire — prêt à découper en tickets

Chaque bloc ci-dessous correspond à un ticket GitHub/JIRA autonome :
titre, ce qu'il couvre, critères d'acceptation. Copiable tel quel.

---

**TICKET — Requêtes Hive SQL/Spark SQL manquantes (Jour 2)** — ✅ FAIT — [#103](https://github.com/PaulPerigault/bigdata-ai-jobs-market/issues/103) (fermée)
Label : `pipeline`
- [x] Jointure offres↔competences comme requête dédiée (pas seulement
  utilisée en interne pour construire la table).
- [x] Une requête `GROUP BY` + `HAVING`.
- [x] Comparaison explicite d'une requête en Hive SQL vs son équivalent
  Spark SQL (pour la section 8 du rapport).
Critère d'acceptation : requêtes exécutées, résultats capturés, chapitre
rapport correspondant mis à jour (DoD). Voir chapitre 08 et
`sql/hive/01_analyses.sql`.

---

**TICKET — KPI obligatoires Jour 3 (10 KPI)** — ✅ FAIT — [#94](https://github.com/PaulPerigault/bigdata-ai-jobs-market/issues/94) (fermée)
Label : `analytics`
- [x] Total offres/métiers en KPI de synthèse affiché.
- [x] Salaire médian (`percentile_approx`), pas seulement moyenne.
- [x] Top métiers les mieux rémunérés (classement dédié).
- [x] Top métiers les plus demandés, top compétences.
- [x] Salaire moyen par pays.
- [x] Salaire par niveau d'expérience.
- [x] Répartition télétravail/présentiel (`remote_work`).
- [x] Analyse LLM/GenAI (`is_llm_role`).
- [x] Évolution 2025-2026 par période (`posting_year`/`posting_month`).
Critère d'acceptation : les 10 KPI calculés et documentés, chapitre
rapport à jour. Voir chapitre 09 et `sql/hive/02_kpis.sql`.

---

**TICKET — 4 analyses au choix (minimum)** — [#95](https://github.com/PaulPerigault/bigdata-ai-jobs-market/issues/95)
Label : `analytics`
Choisir parmi : prime salariale IA, comparaison LLM vs autres métiers,
relation expérience-salaire, pays et compétences, secteur et salaire,
taille d'entreprise et salaire, métiers en forte croissance.
Critère d'acceptation : 4 analyses réalisées avec interprétation,
intégrées au rapport.

---

**TICKET — Dashboard : minimum 6 visualisations** — [#96](https://github.com/PaulPerigault/bigdata-ai-jobs-market/issues/96)
Label : `analytics` `dashboard`
Chaque visualisation : titre, requête source identifiable,
interprétation chiffrée affichée sous le graphique (pas juste le
graphique seul).
Critère d'acceptation : 6+ visualisations dans le notebook Jupyter,
exportées en figures pour le rapport.

---

**TICKET — Rapport : chapitres 01 (introduction) et 02 (dataset)** — [#97](https://github.com/PaulPerigault/bigdata-ai-jobs-market/issues/97)
Label : `rapport`
Rédaction du contexte, de la problématique, des objectifs, et de la
présentation du dataset (source, volumétrie, variables, premières
observations qualité).
Critère d'acceptation : chapitres rédigés, PDF recompile sans erreur.

---

**TICKET — Rapport : chapitres 09-10 (analyses/KPI/dashboard)** — [#98](https://github.com/PaulPerigault/bigdata-ai-jobs-market/issues/98)
Label : `rapport`
Dépend des tickets "KPI obligatoires", "4 analyses au choix",
"Dashboard". Intégrer résultats réels une fois ces tickets faits.
Critère d'acceptation : chapitres à jour avec les vrais chiffres, pas
de placeholder.

---

**TICKET — Rapport : chapitres 11-13 (synthèse, recommandations, limites)** — [#99](https://github.com/PaulPerigault/bigdata-ai-jobs-market/issues/99)
Label : `rapport`
- 6 à 10 constats reliés à un indicateur/requête précis chacun.
- 3 recommandations argumentées (résultat → interprétation →
  recommandation).
- Section limites de l'étude distincte (représentativité, volume,
  limites méthodologiques — ex. le dataset ne permet pas d'affirmer de
  causalité IA→emploi).
Critère d'acceptation : sections rédigées, distinctes les unes des
autres (ne pas mélanger constat et recommandation).

---

**TICKET — Schémas (architecture + modèle 3 tables)** — [#100](https://github.com/PaulPerigault/bigdata-ai-jobs-market/issues/100)
Label : `rapport` `figures`
- Diagramme d'architecture (HDFS→Hive→Spark→Jupyter) pour chapitre 03.
- Schéma relationnel des 3 tables (offres/metiers/competences, clés)
  pour chapitre 07.
Critère d'acceptation : figures dans `report/figures/`, référencées
dans les chapitres concernés (actuellement en commentaire placeholder).

---

**TICKET — Captures d'écran pour annexes** — ✅ FAIT (automatisé) — [#101](https://github.com/PaulPerigault/bigdata-ai-jobs-market/issues/101) (fermée)
Label : `rapport` `figures`
Convention de nommage : `etapeX_outil_contenu.png`.
Critère d'acceptation : captures dans `report/figures/`, intégrées aux
chapitres concernés du rapport.

> **Fait le 16/09/2026, automatisé plutôt que pris à la main** (demande
> explicite : reproductible si la stack change avant le rendu) :
> - `task screenshots-cli` (`scripts/screenshots_cli.sh`, freeze) :
>   `etape1_task_up_healthy.png`, `etape2_hive_raw_describe.png`,
>   `etape2_processed_tables_describe.png`,
>   `etape3_join_offres_competences.png`, `etape3_group_by_having.png`,
>   `etape3_hive_vs_spark_sql.png`, `etape3_kpis_1.png`/`_2.png`.
> - `task screenshots-web` (`scripts/screenshots_web.py`, Playwright) :
>   `etape2_hdfs_namenode_explorer.png`, `etape2_jupyter_notebook.png`.
> - Captures GitHub authentifiées (Project board, Issues, run CI vert) :
>   **volontairement non automatisées** — authentification Playwright
>   propre jugée disproportionnée pour 3-4 captures à ce stade du
>   projet, risque d'un secret bricodé en dur jugé pire que la capture
>   manuelle. `playwright/.auth/` ajouté à `.gitignore` par précaution.
>   **Restent à prendre à la main** : capture du Project board
>   (colonnes Backlog/Todo/In Progress/In Review/Done), de la liste des
>   issues, et d'un run CI vert sur GitHub Actions.
> - Toutes les captures régénérables à la demande via les deux recettes
>   Taskfile ci-dessus (utile si les chiffres/l'UI changent avant le
>   rendu) — voir CLAUDE.md section captures.

---

**TICKET — Relecture croisée finale** — [#102](https://github.com/PaulPerigault/bigdata-ai-jobs-market/issues/102)
Label : `qualité`
Chaque membre relit la section rédigée par un autre. Vérification de
la matrice de vérification en fin de trame docx du prof.
Critère d'acceptation : toutes les sections relues par une personne
différente de l'auteur, corrections appliquées.

---

**TICKET — Export final et vérification livrables** — [#104](https://github.com/PaulPerigault/bigdata-ai-jobs-market/issues/104)
Label : `livraison`
Vérifier : rapport PDF complet, notebook(s), scripts SQL/PySpark
versionnés, captures HDFS/Hive, schéma des 3 tables, dashboard,
conclusions — tout présent avant le 21/09.
Critère d'acceptation : checklist des livrables finaux (section 6 du
sujet PDF) cochée intégralement.

---

## Décisions techniques et bugs corrigés (log condensé)

Détail complet dans `CLAUDE.md` et `JOURNAL.md`. Résumé pour contexte
rapide :
1. Ports Docker : `0.0.0.0` → `127.0.0.1` (scan sécurité).
2. `GRANT_SUDO` retiré (scan sécurité).
3. `metier_id` : `monotonically_increasing_id()` → hash déterministe
   (instabilité découverte en testant réellement).
4. Table Hive RAW : `skip.header.line.count` ignoré par `spark.sql` →
   lecture directe `spark.read.csv(header=True)` sur HDFS.
5. Rapport : `rapport/rapport_esiea.tex` (monolithe, dérive d'un pivot
   précédent) → restructuré en `report/main.tex` + fichiers séparés,
   conforme à ce que `CLAUDE.md` décrivait déjà.
6. GitHub Issues : 87 issues préexistantes (toutes `CLOSED`, datant du
   09-16/09/2026, documentant l'ancienne architecture k3d/Zeppelin déjà
   abandonnée avant le début de ce suivi) supprimées après confirmation
   explicite, pour repartir d'un état propre aligné sur les tickets de
   ce fichier. Les 11 tickets ci-dessous recréés en #94-#104.
7. **CI cassée depuis le premier commit, jamais vérifiée en conditions
   réelles** (découvert lors de l'audit de cohérence du 16/09/2026) :
   le job `lint` échouait sur tous les runs GitHub Actions depuis
   `80dd76a` — `ruff` reformatait
   `src/Analyse_Marche_Emploi_IA_PySpark.ipynb` à chaque run (fichier
   jamais couvert par un `pre-commit run --all-files` local, seulement
   des runs scopés aux fichiers touchés à chaque commit). "CI en
   place" avait été déclaré sans jamais consulter le résultat réel sur
   GitHub. Corrigé : notebook reformaté, règle « toujours `--all-files`
   avant de commit/push » ajoutée à `CLAUDE.md`. Documenté au
   chapitre 03 du rapport comme exemple de recul critique.

## Règle de maintenance de ce fichier

Ce fichier fait partie de la **Definition of Done** définie dans
`CLAUDE.md` : aucune étape n'est terminée tant que la section "État
actuel" n'est pas mise à jour et que le ticket correspondant n'est pas
déplacé de "reste à faire" vers "fait". Ne pas laisser ce document
dériver du repo réel — il doit être aussi fiable que `CLAUDE.md`.
