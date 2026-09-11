# GitHub Project — spécification

## Création

```
gh project create --owner @me --title "Big Data AI Jobs — Roadmap"
```

Récupérer le numéro du projet retourné (`gh project list --owner @me`) pour
les commandes suivantes.

## Champs custom

En plus du champ `Status` par défaut (Backlog / Todo / In Progress / In
Review / Done) :

```
gh project field-create <NUM> --owner @me --name "Day" --data-type SINGLE_SELECT \
  --single-select-options "J1,J2,J3,J4-J5,J6,J7,J8,J9,J10,J11,J12,J13"

gh project field-create <NUM> --owner @me --name "Type" --data-type SINGLE_SELECT \
  --single-select-options "academic,infra,security,docs"

gh project field-create <NUM> --owner @me --name "Team" --data-type SINGLE_SELECT \
  --single-select-options "infra,data-eng,analytics,insights,docs-qa"
```

## Vues

1. **Board** (par défaut) — groupé par `Status`, pour le suivi quotidien.
2. **Roadmap** — table groupée par `Day`, pour voir la charge par jour et
   repérer si un jour déborde sur le suivant.
3. **Barème** — table filtrée sur `Type=academic`, pour vérifier en un coup
   d'œil que rien de noté n'est oublié avant la deadline.
4. **Par équipe** — board groupé par `Team`, une colonne par rôle — vue
   utilisée pour la répartition du travail entre les 5 personnes.

Ces vues se créent depuis l'UI GitHub Projects (pas encore scriptable
proprement via `gh` à ce jour) — 2 minutes une fois le projet ouvert.

## Automatisation

Dans les Workflows du Project (UI, Project → Workflows) :
- "Item added to project" → Status = Backlog
- "Pull request merged" → Status = Done
- "Issue closed" → Status = Done

## Lier les issues au projet

Une fois les issues créées depuis `docs/issues-seed.yml` :

```
gh issue list --repo <owner>/bigdata-ai-jobs-market --json number \
  --jq '.[].number' | xargs -I{} gh project item-add <NUM> --owner @me \
  --url https://github.com/<owner>/bigdata-ai-jobs-market/issues/{}
```

Puis renseigner `Day` et `Type` pour chaque item (le label GitHub de l'issue
donne déjà l'info — copie manuelle ou script `gh project item-edit` si le
volume le justifie).
