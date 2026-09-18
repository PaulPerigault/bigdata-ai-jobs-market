# Politique de sécurité du projet

Dépôt pédagogique (ESIEA — Fondamentaux du Big Data). Ce document reste
volontairement proportionné à un projet étudiant de 5 jours, mais applique
les réflexes DevSecOps de base plutôt que de les ignorer parce que
"c'est juste un TP".

## Périmètre

- Le dataset (`ai_jobs_market_2025_2026.csv`) est un jeu de données
  public (Kaggle), sans donnée personnelle identifiante. Aucune
  classification particulière n'est requise, mais il n'est **jamais**
  committé dans le dépôt (voir `.gitignore`) — il est déposé localement
  dans `data/raw/` par chaque membre et référencé par le pipeline HDFS.
- Le périmètre couvre : le code source (`src/`), les scripts
  d'infrastructure (`compose.yaml`, `Taskfile.yml`), les notebooks, et
  le rapport LaTeX.

## Secrets et configuration

- Aucun secret, mot de passe, token ou clé d'API ne doit être committé.
- Toute configuration sensible (identifiants Hive/HDFS de dev, ports
  personnalisés) passe par `.env`, listé dans `.gitignore`.
  `.env.example` est versionné avec des valeurs factices documentant les
  variables attendues.
- `pre-commit` inclut `gitleaks` pour scanner chaque commit avant push.
  Un secret détecté bloque le commit — ne pas contourner avec
  `--no-verify` sans en avertir l'équipe.
- Si un secret est accidentellement committé : le considérer compromis,
  le régénérer/changer immédiatement (pas seulement le supprimer du
  dernier commit — il reste dans l'historique Git tant qu'il n'est pas
  purgé avec `git filter-repo` ou équivalent).

## Conteneurs et dépendances

- Images Docker **toujours pinnées** par tag de version précis, jamais
  `:latest` — reproductibilité et surface d'attaque connue.
- Pas de service exposé au-delà de `localhost` / du réseau Docker
  interne : ce projet tourne en local pour un rendu académique, pas en
  production, donc aucun port n'a besoin d'être ouvert sur Internet.
- Dépendances Python figées via `pyproject.toml` (versions explicites,
  pas de plage ouverte non bornée sur les packages critiques comme
  `pyspark`).

## Wrapper `./run` : montage du socket Docker (exception assumée)

`./run` (voir `README.md`) exécute `task` dans un conteneur jetable
construit depuis `Dockerfile.runner`, pour que personne dans l'équipe
n'ait besoin d'installer go-task nativement. Ce conteneur monte le
socket Docker de l'hôte (`-v /var/run/docker.sock:/var/run/docker.sock`)
pour que les recettes du Taskfile puissent piloter `docker compose`
(démarrer la stack, exécuter des commandes dans `jupyter`/`hive-server`,
etc.).

**Compromis assumé, à ne jamais généraliser** : monter le socket Docker
donne au conteneur exactement les mêmes privilèges que l'utilisateur
Docker de l'hôte — en pratique un accès root-équivalent au système
Docker (et donc, transitivement, à la machine hôte : un conteneur avec
accès au socket peut démarrer n'importe quel autre conteneur, monter
n'importe quel chemin de l'hôte, etc.). Ce n'est **pas** un sandbox.

Ce compromis est acceptable ici, et seulement ici, parce que :
- Le conteneur `./run` n'exécute que du code du dépôt (`Dockerfile.runner`
  + `Taskfile.yml`, tous deux versionnés et relus par l'équipe) — jamais
  du code tiers non maîtrisé.
- Usage strictement local, poste de développement individuel, projet
  académique sans service exposé (voir sections précédentes).
- L'alternative (installer go-task nativement sur 5 machines avec des
  configurations différentes) coûtait plus cher en risque de dérive de
  configuration que le montage du socket ne coûte en surface d'attaque,
  vu le contexte.

**Ne jamais reproduire ce pattern** dans un contexte où le conteneur
exécuterait du code non maîtrisé (dépendance tierce non auditée, entrée
utilisateur, CI partagée avec d'autres projets) : un conteneur compromis
avec accès au socket Docker compromet l'hôte entier, pas seulement son
propre système de fichiers.

## Accès et périmètre réseau

- HDFS, Hive et Jupyter tournent uniquement sur le réseau Docker Compose
  local. Aucune authentification renforcée n'est mise en place (hors
  périmètre pour un projet pédagogique local), mais aucun service ne
  doit être bindé sur `0.0.0.0` avec un port exposé publiquement.
- Tous les ports publiés dans `compose.yaml`/`compose.override.yaml`
  sont explicitement bindés sur `127.0.0.1` (ex. `"127.0.0.1:8888:8888"`),
  jamais en `"8888:8888"` nu — ce raccourci Docker bind sur `0.0.0.0`
  par défaut, ce qui exposerait le service sur le réseau local (Wi-Fi
  partagé, etc.), pas seulement sur la machine du développeur.

## Signalement

Projet académique sans processus de disclosure formel. Si un membre de
l'équipe repère un problème de sécurité dans le dépôt (secret exposé,
dépendance vulnérable signalée par un outil, mauvaise configuration) :
ouvrir une issue GitHub taguée `security` ou prévenir directement
l'équipe sur le canal du projet — pas de canal public externe nécessaire
vu le périmètre.

## Ce qui est explicitement hors périmètre

- Durcissement en environnement de production (ce projet n'est jamais
  déployé au-delà du poste de travail local des membres de l'équipe).
- Authentification multi-utilisateurs sur HDFS/Hive.
- Chiffrement au repos des données (dataset public, non sensible).
