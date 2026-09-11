#!/usr/bin/env bash
# Creates the HDFS raw/processed/output tree and deposits the source CSV
# into /projet_ia/raw. Idempotent (mkdir -p, put -f). Requires a running
# k3d cluster with HDFS deployed (infra/manifests/10-hdfs/) — see
# `task k3d:up` and `kubectl apply -f infra/manifests/10-hdfs/`.
set -euo pipefail

NAMESPACE="bigdata"
NAMENODE_POD="hdfs-namenode-0"
LOCAL_CSV="data/ai_jobs_market_2025_2026.csv"
REMOTE_TMP="/tmp/ai_jobs_market_2025_2026.csv"

echo "==> Creating HDFS tree under /projet_ia"
kubectl exec -n "$NAMESPACE" "$NAMENODE_POD" -- hdfs dfs -mkdir -p \
  /projet_ia/raw \
  /projet_ia/processed/offres \
  /projet_ia/processed/metiers \
  /projet_ia/processed/competences \
  /projet_ia/output

echo "==> Copying $LOCAL_CSV into the namenode pod"
kubectl cp "$LOCAL_CSV" "$NAMESPACE/$NAMENODE_POD:$REMOTE_TMP"

echo "==> Depositing the CSV into /projet_ia/raw"
kubectl exec -n "$NAMESPACE" "$NAMENODE_POD" -- hdfs dfs -put -f "$REMOTE_TMP" /projet_ia/raw/

echo "==> Cleaning up the temporary copy on the pod"
kubectl exec -n "$NAMESPACE" "$NAMENODE_POD" -- rm -f "$REMOTE_TMP"

echo "==> Done. Run infra/scripts/hdfs-verify.sh to check the result."
