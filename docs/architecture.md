# Architecture

Deux couches à distinguer : le pipeline data imposé par le sujet
(`docs/sujet-synthese.md`), et l'infrastructure k3d qui l'héberge
(`CLAUDE.md`, section Stack technique). Ce document sert de source pour
`report/sections/03-architecture.tex`.

## Pipeline data (imposé par le sujet)

```mermaid
flowchart LR
    CSV[("Dataset CSV\nai_jobs_market_2025_2026.csv")]
    RAW["HDFS /projet_ia/raw"]
    SPARK["Spark\ncontrôle · nettoyage · transformation"]
    PROC["HDFS /projet_ia/processed\noffres · metiers · competences"]
    HIVE["Hive / Spark SQL\ntables externes + requêtes"]
    VIZ["Zeppelin + Data Analytics Studio\nKPI, visualisations, conclusions métier"]

    CSV --> RAW --> SPARK --> PROC --> HIVE --> VIZ
```

## Infrastructure k3d (héberge le pipeline)

```mermaid
flowchart TB
    subgraph k3d["Cluster k3d 'bigdata' (1 server + 2 agents, jetable)"]
        subgraph ns["namespace bigdata"]
            HDFS["HDFS\nNameNode + DataNode StatefulSet + PVC"]
            HMS["Hive Metastore + HiveServer2\n(backend Postgres)"]
            SPARKOP["Spark Operator\n(soumission de jobs PySpark)"]
            ZEP["Zeppelin\n(interpreters Spark + Hive)"]
            VOILA["Voilà\n(dashboard perso, conteneurisé)"]
            NP["NetworkPolicies\n(isolation namespace)"]
        end
        LB["Ingress / LoadBalancer k3d\n(ports 8080/8443 -> hôte)"]
    end

    JUPYTER["Jupyter\n(exploration, kernel PySpark)"] -.->|se connecte à| SPARKOP
    JUPYTER -.->|se connecte à| HMS
    SPARKOP -->|lit/écrit| HDFS
    HMS -->|référence| HDFS
    ZEP -->|interpreters| SPARKOP
    ZEP -->|interpreters| HMS
    VOILA -->|résultats Hive| HMS
    LB --> VOILA
    LB --> ZEP
```

## Rôle de chaque composant

| Composant | Rôle |
|---|---|
| HDFS | Stockage distribué, zones `raw` / `processed` / `output` |
| Hive Metastore + HiveServer2 | Catalogue de tables externes sur HDFS, exécution SQL |
| Spark Operator | Soumission et cycle de vie des jobs PySpark sur k8s |
| Jupyter | Exploration interactive (kernel PySpark connecté au cluster) |
| Zeppelin (+ DAS si le temps le permet) | Dashboard académique obligatoire : requêtes + visualisations |
| Voilà | Interface personnelle (portfolio), résultats Hive, derrière l'ingress |
| NetworkPolicies | Isolation réseau du namespace `bigdata` (durcissement J9) |

## Organisation HDFS (raw / processed / output)

```
/projet_ia/
├── raw/                          # CSV brut déposé tel quel
├── processed/
│   ├── offres/                   # 1 ligne par offre
│   ├── metiers/                  # référentiel métiers, metier_id stable
│   └── competences/               # 1 ligne par offre x compétence
└── output/                       # résultats agrégés / exports pour Zeppelin-DAS
```

Voir `docs/dataset-schema.md` pour le détail des colonnes source, et
`docs/sujet-synthese.md` pour le modèle logique complet (clés, jointures).
