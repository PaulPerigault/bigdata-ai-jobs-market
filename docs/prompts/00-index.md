# Prompts Claude Code — index

Un prompt = une session/tâche bien délimitée, à coller tel quel dans Claude
Code. Toujours dans cet ordre :

1. `01-github-setup.md` — labels, issues, GitHub Project. Aucune action sur
   le cluster, exécutable immédiatement.
2. `02-report-check.md` — vérification/compilation du rapport LaTeX déjà
   scaffoldé. Aucune action sur le cluster.
3. `03-j1-infra-bootstrap.md` — démarrage réel du cluster k3d (J1). À ne
   lancer que quand tu es prêt à commencer le travail infra pour de vrai.

Chaque prompt suppose que Claude Code a déjà lu `CLAUDE.md` (source de
vérité du projet) — c'est rappelé en tête de chaque prompt au cas où la
session soit nouvelle.

Rappel valable pour tous les prompts : dual objectif académique/portfolio
(jamais sacrifier la note), et règle d'or — rien qui touche au cluster sans
validation explicite de Paul.
