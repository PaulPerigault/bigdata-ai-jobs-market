#!/usr/bin/env bash
# Read-only control commands for the /projet_ia tree, per the Jour 1
# checklist (docs/sujet-synthese.md): -ls, -du, -cat/head, wc -l.
set -euo pipefail

NAMESPACE="bigdata"
NAMENODE_POD="hdfs-namenode-0"

exec_hdfs() {
  kubectl exec -n "$NAMESPACE" "$NAMENODE_POD" -- hdfs dfs "$@"
}

echo "==> Tree listing (-ls -R /projet_ia)"
exec_hdfs -ls -R /projet_ia

echo
echo "==> Disk usage (-du -h /projet_ia)"
exec_hdfs -du -h /projet_ia

echo
echo "==> First 5 lines of the raw CSV (-cat | head)"
exec_hdfs -cat /projet_ia/raw/ai_jobs_market_2025_2026.csv | head -5

echo
echo "==> Line count of the raw CSV (wc -l)"
exec_hdfs -cat /projet_ia/raw/ai_jobs_market_2025_2026.csv | wc -l
