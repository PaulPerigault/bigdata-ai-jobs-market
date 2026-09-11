# Rôles de l'équipe (5 personnes)

Répartition par rôle/label, pas nominative pour l'instant — assigner les
pseudos GitHub aux labels `team:*` quand ils sont connus.

## `team:infra`
k3d, namespace, HDFS (NameNode/DataNode), Hive Metastore/HiveServer2, Spark
Operator, NetworkPolicies, secrets (Sealed Secrets/SOPS), CI infra
(scan-images, manifest-lint). Dépend de rien, bloque tout le reste — à
prioriser en premier (J1-J2-J3).

## `team:data-eng`
Chargement Spark, règles de nettoyage (NULL/doublons/types), construction
des 3 tables (offres/metiers/competences), scripts PySpark finaux
versionnés, tests unitaires (`docs/TESTING.md` niveau 1). Dépend de
`team:infra` (a besoin du cluster Spark/HDFS déployé).

## `team:analytics`
Requêtes Hive SQL / Spark SQL obligatoires (Jour 1, 2, 3), KPI, dashboard
Zeppelin/DAS (6+ visualisations), Voilà. Dépend de `team:data-eng` (a
besoin des 3 tables construites).

## `team:insights`
Les 4 analyses au choix, étude LLM/GenAI, synthèse des constats,
recommandations, limites de l'étude. Dépend de `team:analytics` (a besoin
des requêtes/KPI disponibles).

## `team:docs-qa`
Rédaction des sections du rapport (`report/sections/`) au fur et à mesure
que les autres rôles livrent, captures d'écran (`docs/screenshots/`),
tests de qualité de données (niveau 2), relecture finale contre la matrice
de vérification. Rôle transverse — actif du début à la fin, pas seulement
en fin de projet.

## Dépendances entre rôles

```
team:infra → team:data-eng → team:analytics → team:insights
                                              ↘
                                          team:docs-qa (transverse, tout le long)
```

`team:infra` doit avoir une bonne longueur d'avance (J1-J3) avant que les
autres rôles puissent réellement démarrer leur propre travail.
