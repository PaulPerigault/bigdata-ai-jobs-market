# Captures d'écran — limitation de cette session automatisée

Convention `docs/screenshots/J<N>-<slug>.png` posée dans `CLAUDE.md`,
pensée pour une capture d'écran visuelle prise par une personne qui pilote
un terminal/navigateur interactivement.

Cette session (agent Claude Code, exécution non-interactive) n'a pas de
mécanisme de capture d'écran réelle (pas de GUI, pas de screenshot du
terminal). À la place, les sorties de commandes clés (`k3d cluster list`,
`kubectl get ns`, etc.) sont collées dans le corps des PR/issues
correspondantes, et si pertinent un log texte est déposé dans
`docs/screenshots/` avec l'extension `.txt` au lieu de `.png`, clairement
nommé.

**Action pour Paul** : si de vraies captures PNG sont nécessaires pour les
annexes du rapport ou le portfolio DevSecOps, elles seront à reprendre
manuellement en pilotant le cluster interactivement au fur et à mesure —
je ne peux pas les fabriquer après coup.
