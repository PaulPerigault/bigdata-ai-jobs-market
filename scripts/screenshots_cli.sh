#!/usr/bin/env bash
# Régénère les captures terminal/requêtes de report/figures/ via freeze
# (charmbracelet/freeze - https://github.com/charmbracelet/freeze).
# Déterministe : relance les vraies commandes sur la stack déjà up
# (task up), ne rejoue pas un artefact figé. Recette : task screenshots-cli.
#
# `freeze -x "<cmd>"` a un timeout court (~2-3s) et échoue sur toute
# commande qui prend plus longtemps (Hive-on-MR dépasse ça en quelques
# secondes) : on capture donc la sortie dans un fichier texte nous-mêmes,
# puis on demande à freeze de rendre ce fichier (rendu instantané, aucun
# souci de timeout).
set -euo pipefail

cd "$(dirname "$0")/.."
FIGURES_DIR="report/figures"
TMP_DIR=$(mktemp -d)
trap 'rm -rf "${TMP_DIR}" src/_tmp_spark_sql_compare.py' EXIT
mkdir -p "${FIGURES_DIR}"

FREEZE_OPTS=(--window -m 20 -p 30 -r 10 --shadow.blur 20 --shadow.x 0 --shadow.y 8)

# capture <fichier.txt> <invite affichée> <commande réelle>
capture() {
  local txt="${TMP_DIR}/$1"
  local prompt="$2"
  local cmd="$3"
  echo "$ ${prompt}" > "${txt}"
  eval "${cmd}" >> "${txt}" 2>/dev/null
  echo "${txt}"
}

render() {
  local txt="$1"
  local out="$2"
  echo "== ${out} =="
  freeze "${txt}" -o "${FIGURES_DIR}/${out}" "${FREEZE_OPTS[@]}"
  # PNG à fond quasi uni + texte : 64 couleurs suffisent, gain ~10x de
  # poids (pré-commit rejette tout fichier > 1024 Ko, cf. check-added-large-files).
  if command -v magick >/dev/null 2>&1; then
    magick "${FIGURES_DIR}/${out}" -strip -define png:compression-level=9 -colors 64 "${FIGURES_DIR}/${out}"
  fi
}

BEELINE="docker compose exec -T hive-server beeline -u jdbc:hive2://localhost:10000 --silent=true"

# 1. task up : 6 services healthy.
t=$(capture "1.txt" "docker compose ps" \
  "docker compose ps --format 'table {{.Name}}\t{{.Status}}'")
render "$t" "etape1_task_up_healthy.png"

# 2. DESCRIBE de la table RAW.
t=$(capture "2.txt" "beeline -e 'DESCRIBE projet_ia.ai_jobs_raw;'" \
  "${BEELINE} -e 'DESCRIBE projet_ia.ai_jobs_raw;'")
render "$t" "etape2_hive_raw_describe.png"

# 3. DESCRIBE des 3 tables processed.
t=$(capture "3.txt" "beeline -e 'DESCRIBE processed.offres; DESCRIBE processed.metiers; DESCRIBE processed.competences;'" \
  "${BEELINE} -e 'DESCRIBE processed.offres; DESCRIBE processed.metiers; DESCRIBE processed.competences;'")
render "$t" "etape2_processed_tables_describe.png"

# 4. Jointure offres <-> competences dédiée (issue #103).
JOIN_SQL="SELECT c.competence, COUNT(DISTINCT o.job_id) AS nb_offres, ROUND(AVG(o.annual_salary_usd),0) AS salaire_moyen FROM processed.offres AS o INNER JOIN processed.competences AS c ON o.job_id = c.job_id GROUP BY c.competence ORDER BY nb_offres DESC LIMIT 10;"
t=$(capture "4.txt" "beeline -e \"<jointure offres<->competences>\"" \
  "${BEELINE} -e \"${JOIN_SQL}\"")
render "$t" "etape3_join_offres_competences.png"

# 5. Requête GROUP BY + HAVING (issue #103).
HAVING_SQL="SELECT country, COUNT(*) AS nb_offres, ROUND(AVG(annual_salary_usd),0) AS salaire_moyen FROM processed.offres GROUP BY country HAVING COUNT(*) > 50 AND AVG(annual_salary_usd) > 150000 ORDER BY salaire_moyen DESC;"
t=$(capture "5.txt" "beeline -e \"<GROUP BY + HAVING>\"" \
  "${BEELINE} -e \"${HAVING_SQL}\"")
render "$t" "etape3_group_by_having.png"

# 6. Comparaison Hive SQL vs Spark SQL, même requête (issue #103).
cat > "${TMP_DIR}/spark_sql_compare.py" <<'PYEOF'
from etl.spark_session import get_spark

spark = get_spark("cmp")
spark.sql(
    """
    SELECT experience_level, COUNT(*) AS nb_offres,
           ROUND(AVG(annual_salary_usd), 0) AS salaire_moyen
    FROM processed.offres
    GROUP BY experience_level
    ORDER BY salaire_moyen DESC
    """
).show()
PYEOF
# Copié dans src/ (== /home/jovyan/work, monté par compose.override.yaml)
# et non /tmp : le script importe `etl.spark_session`, résolu via le
# sys.path[0] du script (son propre dossier), qui doit donc être src/.
cp "${TMP_DIR}/spark_sql_compare.py" src/_tmp_spark_sql_compare.py

CMP_SQL="SELECT experience_level, COUNT(*) AS nb_offres, ROUND(AVG(annual_salary_usd),0) AS salaire_moyen FROM processed.offres GROUP BY experience_level ORDER BY salaire_moyen DESC;"
{
  echo "\$ beeline -e \"<salaire moyen par expérience>\"   # Hive-on-MR"
  start=$(date +%s)
  eval "${BEELINE} -e \"${CMP_SQL}\"" 2>/dev/null
  echo "  -> temps : $(( $(date +%s) - start ))s"
  echo
  echo "\$ spark.sql(\"<même requête>\").show()   # Spark SQL, plan Catalyst"
  start=$(date +%s)
  docker exec bigdata-ai-jobs-market-jupyter-1 /usr/local/spark/bin/spark-submit /home/jovyan/work/_tmp_spark_sql_compare.py 2>/dev/null
  echo "  -> temps : $(( $(date +%s) - start ))s"
} > "${TMP_DIR}/6.txt"
render "${TMP_DIR}/6.txt" "etape3_hive_vs_spark_sql.png"
rm -f src/_tmp_spark_sql_compare.py

# 7. Les 10 KPI Jour 3 (issue #94). Sortie longue (10 tables) -> rendue
# en un seul PNG puis coupée en 2 moitiés pour rester lisible/imprimable.
docker compose cp sql/hive/02_kpis.sql hive-server:/tmp/02_kpis.sql >/dev/null
t=$(capture "7.txt" "beeline -f sql/hive/02_kpis.sql" \
  "${BEELINE} -f /tmp/02_kpis.sql")
render "$t" "etape3_kpis_full.png"

if command -v magick >/dev/null 2>&1; then
  full="${FIGURES_DIR}/etape3_kpis_full.png"
  height=$(magick identify -format '%h' "${full}")
  half=$((height / 2))
  magick "${full}" -crop "x${half}+0+0" "${FIGURES_DIR}/etape3_kpis_1.png"
  magick "${full}" -crop "x$((height - half))+0+${half}" "${FIGURES_DIR}/etape3_kpis_2.png"
  rm -f "${full}"
else
  echo "AVERTISSEMENT : imagemagick (magick) absent, etape3_kpis_full.png non coupé en 2." >&2
fi

echo "OK : $(ls "${FIGURES_DIR}"/*.png 2>/dev/null | wc -l) captures dans ${FIGURES_DIR}/"
