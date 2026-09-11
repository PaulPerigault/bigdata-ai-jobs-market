NE LANCE CE PROMPT QUE QUAND TU ES PRÊT À DÉMARRER LE TRAVAIL INFRA POUR DE
VRAI — il déclenche des actions sur le cluster.

Lis `CLAUDE.md` à la racine avant toute chose si ce n'est pas déjà fait
dans cette session. Lis aussi `docs/sujet-synthese.md` pour le détail exact
des livrables Jour 1.

Tâche de cette session : bootstrap infra J1 (voir `docs/issues-seed.yml`,
issues day: J1).

1. Confirme d'abord avec Paul avant d'exécuter quoi que ce soit qui modifie
   l'état du cluster (`task k3d:up`, création de namespace, etc.) — c'est
   la règle d'or du projet, rappelée dans `CLAUDE.md`.
2. Une fois confirmé : bootstrap du cluster k3d + namespace `bigdata`
   (issue "infra: bootstrap cluster k3d + namespace bigdata").
3. Crée le squelette de dossiers `infra/{k3d,manifests,security}`,
   `spark-jobs/{notebooks,scripts}`, `voila-app/` (issue "infra: squelette
   des dossiers").
4. Dépose `data/ai_jobs_market_2025_2026.csv` dans `/projet_ia/raw` une
   fois HDFS déployé (dépend de l'issue J2, pas de cette session si HDFS
   n'est pas encore en place — dans ce cas, arrête-toi à l'étape 3).
5. Prends une capture d'écran de chaque étape clé dans
   `docs/screenshots/` avec la convention `J1-<slug>.png` — le cluster est
   jetable, capture au fur et à mesure.

Ferme les issues correspondantes une fois chaque critère d'acceptation
vérifié. Résume l'état en fin de session et attends le feu vert avant J2.
