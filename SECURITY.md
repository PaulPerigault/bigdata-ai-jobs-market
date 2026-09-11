# Politique de sécurité

Ce projet est un démonstrateur pédagogique et personnel (pipeline Big Data +
infra k3d), pas un service en production. Pas de bug bounty, mais les
remontées sont prises au sérieux.

## Signaler une vulnérabilité

Ne pas ouvrir d'issue publique pour une vulnérabilité (secret exposé, faille
dans un manifest, dépendance vulnérable critique). Utiliser plutôt l'onglet
**Security → Report a vulnerability** du repo (GitHub Security Advisories),
qui permet une divulgation privée.

À inclure si possible :
- Composant concerné (`hdfs`, `hive`, `spark`, `zeppelin`, `voila`, `k3d`, `ci`)
- Étapes de reproduction
- Impact estimé

## Ce qui est déjà couvert automatiquement

- Scan de secrets avant commit (`detect-secrets`) et en CI
- Scan de vulnérabilités filesystem/dépendances (`Trivy`) en CI
- Validation des manifests Kubernetes (`kubeconform`) en CI
- Pas de credentials en clair dans les manifests (secrets via Sealed
  Secrets/SOPS)

## Portée

Le cluster k3d est local et jetable — aucune donnée sensible n'y est
attendue au-delà du dataset public *AI Jobs Market 2025-2026*.
