Lis `CLAUDE.md` à la racine avant toute chose si ce n'est pas déjà fait
dans cette session — c'est la source de vérité du projet.

Tâche de cette session, uniquement : mise en place GitHub. Pas d'action sur
le cluster k3d, pas de code Spark/infra.

1. Crée tous les labels définis dans `docs/CONTRIBUTING.md` (section
   Labels) via `gh label create` (couleurs libres, cohérentes par catégorie
   type/scope/priority/academic).
2. Crée les 28 issues définies dans `docs/issues-seed.yml` via
   `gh issue create` — titre, body et labels sont déjà rédigés dans le
   fichier, ne les réécris pas, utilise-les tels quels.
3. Crée le GitHub Project selon `docs/project-board.md` : champ Status par
   défaut + champs custom `Day` et `Type`, les 3 vues décrites (Board,
   Roadmap, Barème), l'automatisation (item ajouté -> Backlog, PR mergée /
   issue fermée -> Done).
4. Lie chaque issue créée à l'étape 2 au Project, et renseigne les champs
   `Day`/`Type` à partir du label de l'issue (le mapping est direct : le
   label `academic:required` ou le préfixe `type:` de chaque issue donne
   `Type`, le commentaire `# --- J<n> ---` dans `issues-seed.yml` donne
   `Day`).

Une fois fait, résume : nombre de labels créés, nombre d'issues créées,
lien vers le Project. N'entame aucune autre tâche sans validation de Paul.
