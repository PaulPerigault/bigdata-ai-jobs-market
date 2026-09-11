# Tests de qualité de données (niveau 2)

Ne tournent pas en CI — nécessitent le cluster k3d up et le pipeline déjà
exécuté (`/processed` peuplé). Voir `docs/TESTING.md`.

Exécution : `task test:data` (une fois les scripts écrits ici).

À couvrir, une fois les 3 tables produites :
- `offres` : unicité `job_id`, cohérence `salary_min_usd <= salary_max_usd`,
  non-nullité `country`/`job_title`
- `metiers` : unicité `metier_id`
- `competences` : intégrité référentielle vers `offres`, aucune valeur vide
