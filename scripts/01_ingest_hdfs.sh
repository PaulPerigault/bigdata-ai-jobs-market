#!/usr/bin/env bash
# Dépose le CSV local (data/raw/) dans HDFS /projet_ia/raw et vérifie le
# dépôt (ls, du, wc -l). Nécessite la stack up (task up).
set -euo pipefail

CSV_NAME="ai_jobs_market_2025_2026.csv"
LOCAL_CSV="data/raw/${CSV_NAME}"
HDFS_DIR="/projet_ia/raw"

if [ ! -f "${LOCAL_CSV}" ]; then
  echo "Fichier introuvable : ${LOCAL_CSV} (le déposer localement avant de lancer l'ingestion)." >&2
  exit 1
fi

echo "== Création de l'arborescence HDFS =="
docker compose exec -T namenode hdfs dfs -mkdir -p "${HDFS_DIR}"
docker compose exec -T namenode hdfs dfs -mkdir -p /projet_ia/processed /projet_ia/output

echo "== Copie du CSV vers HDFS =="
docker compose cp "${LOCAL_CSV}" namenode:/tmp/"${CSV_NAME}"
docker compose exec -T namenode hdfs dfs -put -f /tmp/"${CSV_NAME}" "${HDFS_DIR}/${CSV_NAME}"
docker compose exec -T namenode rm -f /tmp/"${CSV_NAME}"

echo "== Vérification =="
docker compose exec -T namenode hdfs dfs -ls "${HDFS_DIR}"
docker compose exec -T namenode hdfs dfs -du -h "${HDFS_DIR}"

local_lines=$(wc -l < "${LOCAL_CSV}")
hdfs_lines=$(docker compose exec -T namenode hdfs dfs -cat "${HDFS_DIR}/${CSV_NAME}" | wc -l)
echo "Lignes locales : ${local_lines} / Lignes HDFS : ${hdfs_lines}"
if [ "${local_lines}" -ne "${hdfs_lines}" ]; then
  echo "ERREUR : nombre de lignes différent entre le fichier local et HDFS." >&2
  exit 1
fi
echo "OK : ${hdfs_lines} lignes déposées dans ${HDFS_DIR}/${CSV_NAME}"
