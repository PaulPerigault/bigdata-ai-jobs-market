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

### 4 analyses au choix (Étape 3) ✅
- [x] **[#95](https://github.com/PaulPerigault/bigdata-ai-jobs-market/issues/95)**
      4 analyses réalisées et documentées au chapitre 09 §9.3
      (`sql/hive/03_analyses_choix.sql`), DoD appliquée par sous-étape :
      (1) prime salariale IA — Multimodal AI Engineer en tête (13,6%,
      221 791$) ; (2) LLM/GenAI vs autres métiers enrichie — LLM devance
      sur salaire moyen/médian et demand_score ; (3) matrice de
      corrélation salaire/expérience/demande/premium — résultat
      contre-intuitif documenté (corr salaire/expérience quasi nulle à
      0,079 malgré la progression par tranche du KPI 7) ; (4) pays et
      compétences — Python n°1 dans les 5 premiers pays sans exception.

### Dashboard : 6 visualisations (Étape 4) ✅
- [x] **[#96](https://github.com/PaulPerigault/bigdata-ai-jobs-market/issues/96)**
      6 visualisations réalisées dans le notebook (section 8) et
      documentées au chapitre 10, DoD appliquée par sous-étape : (1)
      distribution des salaires — moyenne 194\,892\$, médiane
      180\,000\$ ; (2) évolution mensuelle 2025-2026 — pic février 2026
      (306 offres, ~5,6x la moyenne 2025) ; (3) répartition
      télétravail/présentiel — Hybrid 45,7% ; (4) salaire moyen par
      pays — USA en tête (226\,190\$), écart limité au top 10 ; (5) top
      10 compétences — Python 62,8% ; (6) heatmap de corrélation —
      cohérence croisée confirmée avec l'analyse SQL de #95.

### Rapport LaTeX ✅ (partiel)
- [x] Restructuré en `report/main.tex` + `report/preamble/` +
      `report/chapters/*.tex` (15 chapitres), polices Roboto/Poppins
      versionnées (pas de dépendance système).
- [x] Compile réellement en XeLaTeX, 0 erreur, PDF 46 pages (chiffre du
      18/09/2026, après rédaction des chapitres 01/02/11/12/13 —
      remplace le chiffre de 26 pages resté obsolète depuis l'ajout des
      chapitres 09/10).
- [x] Chapitres rédigés avec résultats réels : **03** (architecture +
      3 corrections sécurité), **04** (ingestion, bug 1501 lignes),
      **05** (DDL Hive + bug header), **06** (nulls/doublons), **07**
      (fix metier_id + chiffres tables), **08** (jointures
      offres↔metiers/competences, GROUP BY+HAVING, comparaison
      Hive/Spark SQL), **09** (10 KPI obligatoires Jour 3 + 4 analyses
      au choix, chiffres réels), **10** (dashboard, 6 visualisations,
      chiffres réels) — Étapes 2, 3 et 4.
- [x] **01** (introduction) et **02** (présentation dataset) rédigés
      le 18/09/2026 — [#110](https://github.com/PaulPerigault/bigdata-ai-jobs-market/issues/110)
      et [#111](https://github.com/PaulPerigault/bigdata-ai-jobs-market/issues/111)
      (fermées) : contexte/problématique/objectifs, chiffres réels du
      dataset (1500 lignes, 25 colonnes — pas 26, écart avec le
      libellé initial de #111 documenté et corrigé au chapitre 02),
      14 pays distincts, aucune valeur manquante sur les 25 colonnes.
- [x] **11** (synthèse), **12** (recommandations) et **13** (limites)
      rédigés le 18/09/2026 — [#99](https://github.com/PaulPerigault/bigdata-ai-jobs-market/issues/99)
      (fermée) : 8 constats reliés aux KPI/analyses des chapitres 8-10,
      3 recommandations argumentées, section limites distincte de la
      synthèse.
- [ ] Chapitres encore en placeholder : **14** (conclusion —
      [#117](https://github.com/PaulPerigault/bigdata-ai-jobs-market/issues/117),
      trouvé vide sans ticket lors de la rédaction de #99), **15**
      (annexes — pas de ticket dédié, contenu prévu en fin de projet).

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

**TICKET — 4 analyses au choix (minimum)** — ✅ FAIT (4/4) — [#95](https://github.com/PaulPerigault/bigdata-ai-jobs-market/issues/95) (fermée)
Label : `analytics`
Choix retenu (4) : prime salariale IA, LLM vs autres métiers,
expérience-salaire (+ matrice de corrélation), pays et compétences.
Critère d'acceptation : 4 analyses réalisées avec interprétation,
intégrées au rapport. DoD appliquée par sous-étape (pas en rattrapage) :
- [x] **Analyse 1 : prime salariale IA par métier** — requête exécutée
      réellement (`sql/hive/03_analyses_choix.sql`), capture
      `etape3_analyse1_prime_ia.png`, chapitre 09 §9.3.1 rédigé. Top :
      Multimodal AI Engineer (premium 13,6\%, salaire 221\,791\$) —
      le premium le plus élevé ne coïncide pas avec le salaire le plus
      élevé (AI Compliance Manager, 3e du classement, salaire pourtant
      modeste à 155\,939\$).
- [x] **Analyse 2 : LLM vs autres métiers (enrichie vs KPI 9)** —
      requête exécutée réellement, capture
      `etape3_analyse2_llm_vs_autres.png`, chapitre 09 §9.3.2 rédigé.
      LLM/GenAI devance sur les 3 indicateurs : salaire moyen +8,6\%
      (207\,746\$ vs 191\,309\$), salaire médian +6,3\% (190\,500\$ vs
      179\,125\$ — écart plus resserré qu'en moyenne), demand\_score
      92,9 vs 86,0.
- [x] **Analyse 3 : expérience-salaire + matrice de corrélation** —
      requête exécutée réellement (`CORR()`, Pearson, aucun modèle
      entraîné), capture `etape3_analyse3_correlation.png`, chapitre 09
      §9.3.3 rédigé. Résultat contre-intuitif documenté avec précaution :
      corr(salaire, expérience continue) quasi nulle (0,079) malgré la
      progression claire par tranche catégorielle au KPI 7 — corr(salaire,
      demand\_score) la plus forte du tableau (0,292) mais reste modeste.
- [x] **Analyse 4 : pays et compétences** — requête exécutée réellement
      (fonction fenêtre `ROW_NUMBER()`), capture
      `etape3_analyse4_pays_competences.png`, chapitre 09 §9.3.4 rédigé.
      Python est la compétence n°1 dans les 5 premiers pays sans
      exception (USA, Chine, Allemagne, Canada, UK) — domination
      uniforme, aucune spécialisation nationale marquée.

Les 4 analyses sont rédigées dans le chapitre 09 (§9.3), avec requête +
capture + interprétation chacune. Voir `sql/hive/03_analyses_choix.sql`.

---

**TICKET — Dashboard : minimum 6 visualisations** — ✅ FAIT (6/6) — [#96](https://github.com/PaulPerigault/bigdata-ai-jobs-market/issues/96) (fermée)
Label : `analytics` `dashboard`
Chaque visualisation : titre, requête source identifiable,
interprétation chiffrée affichée sous le graphique (pas juste le
graphique seul).
Critère d'acceptation : 6+ visualisations dans le notebook Jupyter,
exportées en figures pour le rapport. DoD appliquée par visualisation
(pas en rattrapage) :
- [x] **Viz 1 : distribution des salaires annuels** — histogramme +
      KDE exécuté réellement dans le notebook (section 8.1, lecture
      HDFS directe pour contourner le bug `skip.header.line.count`),
      capture `etape4_dashboard_distribution_salaires.png`, chapitre 10
      rédigé. Moyenne 194\,892\$, médiane 180\,000\$, écart-type
      66\,507\$, 80% des salaires entre 120\,900\$ (p10) et
      297\,100\$ (p90).
- [x] **Viz 2 : évolution du volume d'offres par mois** — line chart
      exécuté réellement (section 8.2), capture
      `etape4_dashboard_evolution_mensuelle.png`, chapitre 10 rédigé.
      Pic en 2026-02 (306 offres), moyenne mensuelle 2025 = 52,0 vs
      2026 (jan-mars) = 292,0 — ~5,6x supérieur, constat descriptif
      sans causalité affirmée (couverture 2026 partielle).
- [x] **Viz 3 : répartition télétravail/présentiel** — bar chart
      exécuté réellement (section 8.3), capture
      `etape4_dashboard_remote_work.png`, chapitre 10 rédigé. Hybrid
      45,7% (686), Fully Remote 29,7% (445), On-site 24,6% (369).
- [x] **Viz 4 : salaire moyen par pays (top 10)** — barres horizontales
      exécutées réellement (section 8.4), capture
      `etape4_dashboard_salaire_pays.png`, chapitre 10 rédigé. USA en
      tête (226\,190\$, 515 offres) ; écart limité au sein du top 10,
      Canada (10e) à 180\,588\$ seulement 20,2% en dessous du leader.
- [x] **Viz 5 : top 10 compétences les plus demandées** — barres
      exécutées réellement (section 8.5, `spark.sql` sur
      `processed.competences`), capture
      `etape4_dashboard_top_competences.png`, chapitre 10 rédigé.
      Python 942 (62,8%), loin devant SQL (452) et Cloud (429).
- [x] **Viz 6 : heatmap de corrélation** — matrice exécutée réellement
      (section 8.6, même 4 variables que l'analyse 3 de #95), capture
      `etape4_dashboard_correlation_heatmap.png`, chapitre 10 rédigé.
      Valeurs identiques à celles calculées en SQL (corr salaire/
      demande 0,292 la plus forte, corr salaire/expérience 0,079 quasi
      nulle) — cohérence croisée SQL/Spark confirmée.

Les 6 visualisations sont rédigées dans le chapitre 10, chacune avec
requête source, capture et interprétation chiffrée affichée dans le
notebook lui-même. Voir section 8 du notebook
`src/Analyse_Marche_Emploi_IA_PySpark.ipynb`.

---

**TICKET — Rapport : chapitres 01 (introduction) et 02 (dataset)** — [#97](https://github.com/PaulPerigault/bigdata-ai-jobs-market/issues/97)
Label : `rapport`
Rédaction du contexte, de la problématique, des objectifs, et de la
présentation du dataset (source, volumétrie, variables, premières
observations qualité).
Critère d'acceptation : chapitres rédigés, PDF recompile sans erreur.

---

**TICKET — Rapport : chapitres 09-10 (analyses/KPI/dashboard)** — ✅ FAIT — [#98](https://github.com/PaulPerigault/bigdata-ai-jobs-market/issues/98) (fermée)
Label : `rapport`
Dépendait des tickets "KPI obligatoires" (#94), "4 analyses au choix"
(#95), "Dashboard" (#96) — les 3 sont fermées, chapitres 09 et 10
rédigés avec les vrais chiffres.
Critère d'acceptation : chapitres à jour avec les vrais chiffres, pas
de placeholder. Voir chapitres 09 et 10.

---

**TICKET — Rapport : chapitres 11-13 (synthèse, recommandations, limites)** — ✅ FAIT — [#99](https://github.com/PaulPerigault/bigdata-ai-jobs-market/issues/99) (fermée)
Label : `rapport`
- 6 à 10 constats reliés à un indicateur/requête précis chacun.
- 3 recommandations argumentées (résultat → interprétation →
  recommandation).
- Section limites de l'étude distincte (représentativité, volume,
  limites méthodologiques — ex. le dataset ne permet pas d'affirmer de
  causalité IA→emploi).
Critère d'acceptation : sections rédigées, distinctes les unes des
autres (ne pas mélanger constat et recommandation).
Rédigé le 18/09/2026 : **8 constats** (chapitre 11, chacun relié à un
KPI/analyse/requête précis des chapitres 8-10), **3 recommandations**
argumentées (chapitre 12, schéma résultat→interprétation→recommandation :
recrutement/rétention LLM Engineer, grille salariale indexée sur la
tension du marché plutôt que l'ancienneté, politique hybride par
défaut), **section limites distincte** (chapitre 13 : non-causalité,
représentativité incertaine du dataset — probablement synthétique vu
l'absence totale d'anomalie et la répartition d'expérience uniforme,
limites méthodologiques spécifiques au pic 2026 et aux corrélations de
Pearson). PDF recompilé (46 pages), pages 38-42 inspectées visuellement.

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

**TICKET — Rapport : chapitre 01 (Introduction)** — ✅ FAIT — [#110](https://github.com/PaulPerigault/bigdata-ai-jobs-market/issues/110) (fermée)
Label : `rapport`
Contexte du marché de l'emploi IA, problématique, objectifs
pédagogiques/techniques, intérêt de la chaîne HDFS→Hive→Spark→Jupyter.
Critère d'acceptation : chapitre rédigé, cohérent avec ce qui a été
réellement construit (pas le plan initial), PDF recompile sans erreur.
Rédigé le 18/09/2026, PDF recompilé (43 pages, inspection visuelle des
pages concernées) — voir chapitre 01.

---

**TICKET — Rapport : chapitre 02 (Présentation du dataset)** — ✅ FAIT — [#111](https://github.com/PaulPerigault/bigdata-ai-jobs-market/issues/111) (fermée)
Label : `rapport`
Source du dataset, volumétrie (1500 lignes, 26 colonnes), variables
principales, premières observations de qualité (avant nettoyage).
Critère d'acceptation : chapitre rédigé avec les vrais chiffres, pas
d'estimation.
Rédigé le 18/09/2026 avec les vrais chiffres (**25 colonnes**, pas 26 —
écart avec le libellé initial du ticket, corrigé et documenté au
chapitre 02 ; 14 pays distincts, 0 valeur manquante). PDF recompilé et
inspecté visuellement — voir chapitre 02.

---

**TICKET — Captures GitHub manuelles** — [#115](https://github.com/PaulPerigault/bigdata-ai-jobs-market/issues/115)
Label : `rapport` `figures`
À faire à la main (pas via Claude Code) : Project board (vue
Backlog/Todo/In Progress/In Review/Done), liste des issues fermées, un
run CI vert — les 3 captures volontairement laissées manuelles depuis
#101 (authentification GitHub, voir note ci-dessus).
Critère d'acceptation : 3 captures dans `report/figures/` (convention
`etapeX_outil_contenu.png`), intégrées au chapitre 03.

---

**TICKET — Bonus si le temps le permet** — [#116](https://github.com/PaulPerigault/bigdata-ai-jobs-market/issues/116)
Label : `bonus`
Non noté explicitement mais valorisant pour le recul critique :
comparaison à une source externe publique, export CSV/JSON des KPI
dans `output/`, schéma de séquence pour la soutenance orale.
Critère d'acceptation : optionnel, à ne traiter qu'une fois tout le
reste fermé.

---

> **Note du 17/09/2026** : trois tickets initialement proposés pour ce
> lot (chapitres 11-13, relecture croisée, vérification finale des
> livrables) faisaient doublon avec des tickets déjà existants et
> ouverts (#99, #102, #104 respectivement, créés le 16/09/2026).
> Créés par erreur en #112/#113/#114, fermés immédiatement en
> "not planned" avec renvoi vers le ticket original — l'automation du
> Project board les affiche en "Done" comme tout ticket fermé, mais il
> ne s'agit pas de travail réellement terminé : le vrai suivi reste sur
> #99/#102/#104, toujours ouverts.

> **Note du 18/09/2026 — audit complet des besoins du sujet** :
> relecture intégrale de `documentation/Projet_BigData_IA_Version_
> Etudiants_...pdf` (le sujet PDF réel, pas seulement le résumé qu'en
> fait `CLAUDE.md`) confrontée à `STATUS.md`, aux chapitres du rapport
> et aux issues ouvertes/fermées. Résultat : aucun point du sujet
> (objectifs pédagogiques, jour 1/2/3, requêtes obligatoires, KPI,
> livrables finaux, barème) sans trace dans le suivi — le remplacement
> Zeppelin/DAS → Jupyter/PySpark reste la seule déviation, déjà validée
> et documentée. Une incohérence de suivi trouvée et corrigée : **#97**
> ("chapitres 01+02") faisait doublon avec **#110** (chapitre 01) et
> **#111** (chapitre 02), créées séparément le 16/09/2026 pour
> permettre une fermeture indépendante par chapitre — #97 n'apparaissait
> déjà plus dans la liste "reste à faire" de ce fichier mais restait
> ouverte sur GitHub (colonne Todo du Project board). Fermée en
> "not planned" avec renvoi vers #110/#111, même pattern que
> #112/#113/#114 ci-dessus. Par ailleurs, `README.md` n'existait pas à
> la racine du dépôt malgré son rôle de point d'entrée attendu pour tout
> nouveau lecteur (professeur, membre de l'équipe) — créé (architecture,
> commandes Taskfile, structure du dépôt, modèle de données, conventions
> de contribution), sans ticket dédié (pas un livrable noté au barème,
> mais une lacune de présentation du projet).

---

**TICKET — Rapport : chapitre 14 (Conclusion)** — [#117](https://github.com/PaulPerigault/bigdata-ai-jobs-market/issues/117)
Label : `rapport`
Trouvé en marge de la rédaction des chapitres 11-13 (#99, 18/09/2026) :
`report/chapters/14_conclusion.tex` ne contient que
`\chapter{Conclusion}`, aucun contenu — aucun ticket existant ne le
couvrait explicitement jusqu'ici.
Critère d'acceptation : chapitre rédigé (clôture synthétique, sans
redite des chapitres 11/12), PDF recompile sans erreur.

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
8. **CI cassée une deuxième fois après le commit `2170739` (#95)** :
   `sqlfluff-lint` a échoué sur GitHub Actions
   (`sql/hive/03_analyses_choix.sql`, lignes trop longues + indentation)
   alors qu'un `pre-commit run --all-files` local avait rapporté "tout
   passe" juste avant de commit. Cause exacte non identifiée avec
   certitude (fichier probablement pas encore sauvegardé au moment du
   run local, ou lecture erronée de la sortie) — pas un problème
   d'environnement CI vs local puisqu'un nouveau `pre-commit run` local
   a immédiatement reproduit l'échec de GitHub. Corrigé (commit
   `2347b81`) : requête de corrélation ré-enveloppée avec des alias plus
   courts et une indentation à 4 espaces cohérente ; requête pays/
   compétences reformatée pour `LT09`/`AL01`. Vérifié avec
   `gh run watch` sur le run réel (pas seulement le pre-commit local) —
   `lint` et `test` verts sur `2347b81`.

## Règle de maintenance de ce fichier

Ce fichier fait partie de la **Definition of Done** définie dans
`CLAUDE.md` : aucune étape n'est terminée tant que la section "État
actuel" n'est pas mise à jour et que le ticket correspondant n'est pas
déplacé de "reste à faire" vers "fait". Ne pas laisser ce document
dériver du repo réel — il doit être aussi fiable que `CLAUDE.md`.
