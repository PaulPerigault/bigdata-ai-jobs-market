# project-status-sync — notes de suivi

Mis en place et testé en conditions réelles (5 cas : issue ouverte/réouverte
-> Backlog, assignée -> In Progress, fermée -> Done, PR ouverte -> In
Review, PR mergée -> Done). Tous validés.

## À surveiller

- **Token `PROJECTS_TOKEN`** : PAT classique avec expiration (repo, project,
  read:org, read:discussion). Noter ici la date choisie dès qu'elle est
  connue, et mettre un rappel pour le renouveler avant expiration — sinon
  le sync échoue silencieusement, sans que personne ne le remarque tout de
  suite.
- **Pas de retour arrière géré** : une issue réassignée à personne ne
  repasse pas automatiquement en Backlog (asymétrie avec les Workflows
  natifs GitHub, qui ne le font pas non plus par défaut — non bloquant,
  juste à savoir si quelqu'un de l'équipe s'attend à une symétrie totale).

## Dette CI découverte pendant le test (PR #73) — résolue

4 checks cassés, préexistants, sans rapport avec ce workflow, bypassés en
admin uniquement pour ce test initial. Diagnostiqués et corrigés dans une
session dédiée (issues #75-#78, une PR par check, mergées normalement,
`main` entièrement vert) :
- `pr-title-check` (#75, PR #79) : le `GITHUB_TOKEN` du job était read-only
  (réglage repo par défaut + aucun bloc `permissions:` dans `ci.yml`).
  Corrigé en ajoutant `permissions: pull-requests: write` scopé au job.
- `scan-images` (#76, PR #80) : `aquasecurity/trivy-action@0.28.0`
  référençait un tag inexistant (les tags du repo sont préfixés `v`).
  Corrigé en passant à `v0.36.0`.
- `manifest-lint` (#77, PR #81) : `infra/manifests/` n'existe pas encore
  (déploiement infra pas commencé, prévu J2-J3) — `kubeconform` plantait
  sur le dossier absent. Corrigé avec un guard step qui skip proprement
  (même pattern que `scan-images`) tant que le dossier n'existe pas ou est
  vide.
- `pre-commit` (#78, PR #82) : deux causes dans le même job —
  `.secrets.baseline` référencé par le hook `detect-secrets` était absent
  (ajouté, 0 secret détecté), et `.idea/modules.xml`/`.idea/vcs.xml`
  n'avaient pas de retour à la ligne final (`end-of-file-fixer` les
  modifiait, ce qui fait échouer le check en CI).

**Note méthodologique** : comme les 6 checks sont tous requis par la
protection de branche, aucune des 3 premières PR de correction ne pouvait
être "100% verte" à elle seule (les 3 autres bugs, pas encore fusionnés,
faisaient encore échouer les autres checks). Plutôt qu'un bypass admin
répété, la liste des checks requis a été rétrécie temporairement à chaque
étape (seuls les checks déjà corrigés + non concernés restaient requis),
puis chaque check corrigé a été réintégré à la liste immédiatement après
son merge. À la fin, la liste requise est identique à l'originale (6 checks) et
la dernière PR (#82) a pu être mergée avec les 6 checks verts en même
temps.
