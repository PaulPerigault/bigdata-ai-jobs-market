#!/bin/bash
# Monté dans le conteneur hive-metastore (voir compose.yaml). Doit rester un
# seul token dans `command:` — l'entrypoint.sh de bde2020/hive fait un
# `exec $@` non quoté qui casserait toute commande contenant des espaces.
set -e
/opt/hive/bin/schematool -dbType postgres -initSchema || true
exec /opt/hive/bin/hive --service metastore
