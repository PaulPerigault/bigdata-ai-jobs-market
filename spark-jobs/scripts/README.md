# spark-jobs/scripts/

Scripts PySpark versionnés (repo Git) — version finale propre extraite de
l'exploration Jupyter (`spark-jobs/notebooks/`). Voir `CLAUDE.md`.

Convention de découpage (une responsabilité par module, pas de logique
métier mêlée à l'I/O — voir `docs/TESTING.md` niveau 1) :

- `io_raw.py` — lecture du CSV brut depuis HDFS
- `cleaning.py` — règles de nettoyage (nulls, doublons, types), fonctions
  pures testables
- `transform_offres.py`, `transform_metiers.py`, `transform_competences.py`
  — construction des 3 tables (grain, `metier_id`, `split`/`explode`)
- `io_processed.py` — écriture des 3 tables dans `/processed`

Chaque fonction de transformation notable a son test unitaire associé dans
`tests/unit/`, écrit dans la même PR qui l'introduit.
