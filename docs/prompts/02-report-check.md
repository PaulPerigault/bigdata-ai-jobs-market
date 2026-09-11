Lis `CLAUDE.md` à la racine avant toute chose si ce n'est pas déjà fait
dans cette session.

Tâche de cette session, uniquement : vérifier `report/rapport.tex`. Pas
d'action sur le cluster k3d, pas de code Spark/infra, pas de rédaction de
contenu (le rapport se remplit au fil du projet, pas maintenant).

1. Compile `report/rapport.tex` avec `tectonic` (`task report:build`) et
   corrige toute erreur de compilation LaTeX (syntaxe, package manquant).
   Ne touche pas à la structure des sections — elle est calée
   intentionnellement sur la trame officielle du professeur (voir
   `docs/sujet-synthese.md` pour le contexte complet), ne réordonne rien et
   n'ajoute/ne retire aucune section.
2. Vérifie que les tableaux longtable (dictionnaire de données, questions
   métier, constats, matrice de vérification) se découpent proprement sur
   plusieurs pages sans déborder.
3. Le champ "Groupe" de la page de garde est vide — demande la valeur à
   Paul plutôt que d'inventer une valeur.
4. Ne remplis aucun `\textbf{[TODO]}` ni aucune case de tableau vide — ce
   contenu viendra au fur et à mesure du projet, pas à cette étape.

Résume l'état : compilation OK/KO, nombre de pages actuel (hors contenu),
et la question sur "Groupe" si elle reste ouverte.
