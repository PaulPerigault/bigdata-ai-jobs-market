# Journal d'exécution

Trace des recettes Taskfile exécutées sur ce projet. Ajout en fin de
fichier uniquement (append) — ne jamais réorganiser ou supprimer une
entrée passée (voir CLAUDE.md).

## 2026-09-16 15:07 — task up (validation réelle Étape 1)
Commande : docker compose up -d (via colima, cf. CLAUDE.md)
Résultat : 6/6 services healthy (namenode, datanode, hive-metastore-postgresql,
hive-metastore, hive-server, jupyter). Vérifié en vrai : hdfs dfs -ls/-mkdir,
beeline SHOW DATABASES, et un job PySpark depuis Jupyter écrivant une table
Hive sur HDFS puis la relisant (round-trip HDFS -> Hive -> Spark confirmé).
Corrections apportées en cours de route : ports web namenode/datanode
(50070/50075, pas 9870/9864 — Hadoop 2.7.4), SERVICE_PRECONDITION datanode
(namenode:8020), backend Postgres remplacé par postgres:13.18 officiel
(bde2020/hive-metastore-postgresql crashait sous émulation), script
scripts/hive-metastore-entrypoint.sh pour initialiser le schéma Hive,
JAVA_TOOL_OPTIONS=-Xint pour contourner un blocage JIT sous QEMU.
Auteur : task automation

## 2026-09-16 15:35 — task ingest + task etl (validation réelle Étape 2)
Commande : bash scripts/01_ingest_hdfs.sh && spark-submit src/etl_pipeline.py
Résultat : CSV déposé dans /projet_ia/raw (1500 lignes de données vérifiées
ls/du/wc -l). Table projet_ia.ai_jobs_raw (EXTERNAL, TEXTFILE) créée et
interrogée via Beeline (COUNT=1500, AVG salaire=194892$). Pipeline ETL
exécuté pour de vrai : 0 doublon job_id, 0 salaire <=0 sur ce run, 25
métiers (processed.metiers), 1500 offres (processed.offres), 9548 liaisons
job_id<->compétence (processed.competences), toutes écrites en Parquet sur
HDFS /projet_ia/processed/ et exposées comme tables Hive externes.
Jointure offres<->metiers vérifiée via Beeline (top métier par volume :
LLM Engineer, 75 offres, salaire moyen 240960$).
Bug corrigé en cours de route : spark.sql lisant une table Hive TEXTFILE
n'honore pas skip.header.line.count (ligne d'en-tête comptée comme donnée,
1501 au lieu de 1500) -> etl_pipeline.py lit désormais le CSV RAW
directement depuis HDFS via spark.read.csv(header=True), cf. CLAUDE.md.
Auteur : task automation

## 2026-09-16 16:00 — rattrapage rapport (Definition of Done, Étapes 1-2)
Commande : xelatex -interaction=nonstopmode -halt-on-error main.tex (x2, depuis report/)
Résultat : ajout d'une section "Definition of Done" dans CLAUDE.md (s'applique
à toutes les étapes suivantes). Éclatement de rapport/rapport_esiea.tex
(monolithique, placeholders) en report/main.tex + report/preamble/*.tex +
report/chapters/*.tex, avec rédaction réelle des chapitres concernés par les
Étapes 1-2 : 03_architecture (stack réelle + 3 corrections de sécurité issues
du scan automatique), 04_ingestion_hdfs (arborescence + 1501 lignes vérifiées),
05_hive_raw (DDL + bug skip.header.line.count ignoré par spark.sql, 1501 vs
1500), 06_spark_quality (comptages NULL/doublons chiffrés), 07_construction_
tables (fix metier_id + 1500 offres/25 metiers/9548 competences),
08_analyses (jointure offres<->metiers, LLM Engineer commenté). Compilation
vérifiée réellement (2 passes xelatex, 0 erreur, PDF 22 pages, polices Roboto/
Poppins versionnées dans report/fonts/ pour ne pas dépendre de l'install
système). Chapitres non encore concernés (01,02,09-15) laissés en placeholder,
normal tant que leur étape n'est pas atteinte.
Auteur : task automation

## 2026-09-16 16:15 — STATUS.md corrigé + issues GitHub recréées
Commande : gh issue delete/create/edit (voir historique de la session)
Résultat : corrections d'exactitude dans STATUS.md (pre-commit = ruff
seul, pas black ; GRANT_SUDO retiré du conteneur jupyter uniquement,
pas "conteneurs Hadoop" ; 9548 competences = chiffre exact, pas une
approximation ; label "sql" retiré du ticket 1, hors liste des 7 labels
approuvés). Ajout d'une 5e condition à la Definition of Done (CLAUDE.md)
: STATUS.md doit être mis à jour à chaque étape. Note ajoutée au ticket
"Captures d'écran" listant précisément les 4 captures manquantes
(report/figures/ vide, confirmé). 87 issues GitHub préexistantes
(CLOSED, ancienne architecture k3d/Zeppelin) supprimées après
confirmation utilisateur, labels pipeline/analytics/dashboard/rapport/
figures/qualité/livraison créés, 11 tickets de STATUS.md recréés en
issues #94-#104 (une erreur d'indexation de tableau bash a d'abord
décalé titres/labels vs corps de plusieurs issues — détectée et
corrigée avant validation finale). STATUS.md mis à jour avec les liens
vers chaque issue.
Auteur : task automation

## 2026-09-16 16:20 — Requêtes Hive SQL/Spark SQL manquantes (issue #103)
Commande : beeline -f sql/hive/01_analyses.sql ; spark-submit (comparaison)
Résultat : jointure offres<->competences dédiée exécutée pour de vrai
(top compétence Python, 942/1500 offres soit 63%). Requête GROUP BY +
HAVING exécutée (12 pays avec >50 offres et salaire moyen >150000$, USA
en tête à 226190$). Comparaison Hive SQL vs Spark SQL sur la même
requête (salaire moyen par expérience) : résultats identiques sur les 2
moteurs, Hive-on-MR 33.0s vs Spark SQL 8.8s (SparkSession chaude
comprise) - chiffré et documenté au chapitre 08. Rapport recompilé (2
passes xelatex, 0 erreur, 22 -> 24 pages). Issue #103 fermée, ticket
correspondant dans STATUS.md déplacé vers "fait".
Auteur : task automation

## 2026-09-16 16:35 — KPI obligatoires Jour 3 (issue #94)
Commande : beeline -f sql/hive/02_kpis.sql
Résultat : 10 KPI calculés pour de vrai sur le dataset réel : total 1500
offres/25 métiers, salaire moyen 194892$/médian 179421$, métier le mieux
rémunéré AI Solutions Architect (251577$), le plus demandé LLM Engineer
(75 offres), compétence la plus demandée Python (942 offres), pays le
mieux rémunéré USA (226190$), salaire par expérience (Lead 240055$ ->
Entry 150039$), Hybrid dominant (45.7%), écart LLM/GenAI documenté
(+8.6% de salaire mais premium_pct plus bas, sans affirmation causale),
pic d'activité fevrier 2026 (306 offres, ~5x le volume mensuel 2025 -
signale comme constat descriptif, pas une preuve de tendance). Chapitre
09 du rapport rédigé avec ces résultats réels. Rapport recompilé (2
passes xelatex, 0 erreur, 24 -> 26 pages, vérifié visuellement). Bug SQL
corrigé en route : Hive 2.3.2 ne supporte pas les sous-requêtes
scalaires en SELECT ni les CROSS JOIN (désactivés par sécurité) -> KPI1
réécrit en UNION ALL avec discriminant. Issue #94 fermée, ticket déplacé
vers "fait" dans STATUS.md.
Auteur : task automation

## 2026-09-16 16:50 — audit de cohérence complet + Project + issues rétroactives
Commande : git log --oneline --all ; gh issue create/close ; gh project item-edit ;
pre-commit run --all-files ; xelatex (2 passes)
Résultat : 5 issues rétroactives créées et fermées pour le travail déjà fait et
non encore représenté (#105 infra bootstrap, #106 pipeline de données, #107
restructuration rapport, #108 mise en place CI, #109 corrections sécurité),
chacune fermée avec un commentaire renvoyant vers le hash de commit exact
(80dd76a et 1737b51). Labels infra/ci/security créés. Projet GitHub existant
"Big Data AI Jobs — Roadmap" (#9, colonnes Backlog/Todo/In Progress/In
Review/Done) identifié — statuts alignés manuellement : #94/#103/#105-109 ->
Done, #95/#96/#97/#100/#101 -> Todo, #98/#99/#102/#104 -> Backlog (bloqués par
dépendances). Audit de cohérence complet (STATUS.md, CLAUDE.md, JOURNAL.md,
compilation+inspection visuelle du rapport, correspondance issues<->chapitres)
: 8 incohérences trouvées et corrigées, la plus grave étant que le job CI
"lint" échouait sur TOUS les runs GitHub Actions depuis le premier commit
d'infra (80dd76a) sans que cela ait jamais été vérifié sur GitHub -> notebook
src/Analyse_Marche_Emploi_IA_PySpark.ipynb jamais passé par `pre-commit run
--all-files`, seulement des runs scopés par commit. Corrigé (notebook
reformaté, règle --all-files ajoutée à CLAUDE.md, documenté au chapitre 03
comme exemple de recul critique). Autres corrections : CLAUDE.md (ruff/black
obsolète, ~9548->9548, liste des chapitres avec contenu réel incomplète,
mention SQL "à venir" obsolète), STATUS.md (lien #99 manquant dans la liste
des chapitres placeholder). Rapport recompilé et inspecté visuellement (2
passes xelatex, 0 erreur, 26 -> 27 pages).
Auteur : task automation

## 2026-09-16 17:20 — captures d'écran automatisées (issue #101)
Commande : task screenshots-cli ; task screenshots-web
Résultat : 9 captures régénérées dans report/figures/ via freeze
(charmbracelet/freeze, scripts/screenshots_cli.sh) et Playwright
(scripts/screenshots_web.py) plutot que prises a la main. Piège freeze
découvert : `freeze -x "<commande>"` a un timeout court (~2-3s) et échoue
(signal: killed / no command output) sur toute commande plus longue,
largement dépassé par Hive-on-MR -> le script capture la sortie dans un
fichier texte lui-même puis demande a freeze de rendre ce fichier deja
ecrit (rendu instantane, aucun souci de timeout). Image des 10 KPI
(12872px de haut) coupee en 2 via imagemagick pour rester imprimable ;
toutes les captures recompressees (-colors 64) pour repasser sous la
limite de 1024 Ko de check-added-large-files (1.3-1.5 Mo -> ~100-350 Ko,
qualite visuelle inchangee, verifie). Chapitres 03 (task up healthy +
environnement Jupyter), 05 (DESCRIBE raw/processed + explorer HDFS), 08
(jointure competences, GROUP BY+HAVING, comparaison Hive/Spark SQL avec
chiffres reconcilies sur ce run : 57s/15s), 09 (10 KPI) mis a jour avec
les figures. Bug de mise en page corrige en route : les 2 images KPI
(tres hautes) debordaient sur le pied de page et perdaient leur legende
en `width=`+`[h]` -> passees en `height=0.8\textheight`+`[p]`. Captures
GitHub authentifiees (Project board, Issues, run CI vert) volontairement
non automatisees (cf. CLAUDE.md) - restent a prendre a la main. Rapport
recompile et inspecte visuellement (2 passes xelatex, 0 erreur, 27 -> 33
pages). Issue #101 fermee, ticket deplace vers "fait" dans STATUS.md.
Auteur : task automation

## 2026-09-17 00:30 — Analyse 1/4 au choix : prime salariale IA (issue #95)
Commande : beeline -e "<top 5 metiers par prime IA moyenne>" ; task screenshots-cli (freeze manuel)
Resultat : requete executee reellement sur processed.offres JOIN
processed.metiers. Top 5 : Multimodal AI Engineer (premium 13.6%,
salaire 221791$), Robotics Engineer AI (13.55%), AI Compliance Manager
(13.45%, salaire 155939$ - le 3e plus fort premium n'est pas dans le
top salaires absolus), MLOps Engineer (13.23%), Generative AI Engineer
(13.22%). Capture etape3_analyse1_prime_ia.png generee et integree au
chapitre 09 (section 9.3, nouvelle, "4 analyses au choix"). 1/4 analyses
faites, DoD appliquee immediatement (pas en rattrapage) : requete +
capture + chapitre + STATUS.md a jour avant de passer a l'analyse
suivante.
Auteur : task automation

## 2026-09-17 00:35 — Analyse 2/4 au choix : LLM vs autres métiers (issue #95)
Commande : beeline -e "<LLM/GenAI vs autres métiers, comparaison enrichie>"
Resultat : requete executee reellement sur projet_ia.ai_jobs_raw
(comparaison enrichie vs KPI 9 : ajout mediane + demand_score, pas
seulement la moyenne). LLM/GenAI (327 offres) devance sur les 3
indicateurs : salaire moyen 207746$ vs 191309$ (+8.6%), salaire median
190500$ vs 179125$ (+6.3%, ecart plus resserre qu'en moyenne),
demand_score moyen 92.9 vs 86.0. Capture
etape3_analyse2_llm_vs_autres.png generee et integree au chapitre 09
section 9.3.2. 2/4 analyses faites, DoD appliquee immediatement.
Auteur : task automation

## 2026-09-17 00:40 — Analyse 3/4 au choix : correlation salaire/experience (issue #95)
Commande : beeline -e "<matrice de correlation salaire/experience/demande/premium>"
Resultat : requete CORR() executee reellement sur projet_ia.ai_jobs_raw
(Pearson, descriptif, aucun modele entraine - touche BI suggeree par
l'utilisateur). Resultat contre-intuitif et documente avec precaution :
corr(salaire, years_of_experience continu) quasi nulle (0.079), alors
que le KPI 7 montre une progression claire par tranche categorielle
(experience_level) - explique par un possible effet de seuil non
lineaire + variance intra-tranche, pas une contradiction. corr(salaire,
demand_score)=0.292 la plus forte du tableau mais reste modeste ;
corr(salaire, premium)=-0.02 et corr(experience, demand_score)=-0.096
quasi nulles. Capture etape3_analyse3_correlation.png generee et
integree au chapitre 09 section 9.3.3. 3/4 analyses faites, DoD
appliquee immediatement.
Auteur : task automation

## 2026-09-17 00:45 — Analyse 4/4 au choix : pays et competences (issue #95)
Commande : beeline -e "<competence n°1 par pays, top 5 paires par volume>"
Resultat : requete avec fonction fenetre ROW_NUMBER() executee reellement
sur processed.offres JOIN processed.competences. Python est la
competence n°1 dans les 5 premiers pays sans exception (USA 334 offres,
Chine 58, Allemagne 54, Canada 54, UK 52) - domination uniforme, aucune
specialisation nationale marquee sur la competence phare. Capture
etape3_analyse4_pays_competences.png generee et integree au chapitre 09
section 9.3.4. 4/4 analyses faites - issue #95 fermee, ticket deplace
vers "fait" dans STATUS.md. Rapport recompile et inspecte visuellement
a chaque sous-etape (2 passes xelatex, 0 erreur, 33 -> 36 pages au
final). DoD appliquee par sous-etape tout du long (requete + capture +
chapitre + STATUS.md avant de passer a l'analyse suivante), pas en
rattrapage.
Auteur : task automation
