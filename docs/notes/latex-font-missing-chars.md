# Caractères manquants dans le rendu LaTeX (`—`, `→`)

Constaté en vérifiant le build (`task report:build`, via Docker, issue
#87) : la police par défaut de tectonic (Latin Modern / `ec-lmr10`) ne
sait pas représenter certains caractères Unicode utilisés dans plusieurs
sections du rapport — `—` (tiret cadratin) et `→` (flèche). Le moteur
émet un warning et **omet silencieusement le caractère** dans le PDF
final (pas d'erreur bloquante, mais le texte rendu diffère du texte
source).

Sections concernées à ce jour : `08-hive-spark-sql`,
`09-analyse-metiers-salaires`, `10-dashboard`, `11-synthese`,
`12-recommandations`, `13-limites`, `14-conclusion`, `15-annexes`.

**Pas corrigé maintenant** (hors périmètre de la conteneurisation du
build) : soit remplacer `—`/`→` par leurs équivalents LaTeX natifs
(`--\,--` ou `\textemdash`, `$\rightarrow$`), soit charger une police avec
un jeu de caractères Unicode plus large (`fontspec` + XeLaTeX/LuaLaTeX,
mais ça changerait le moteur de compilation). À traiter avant la relecture
finale (J12, matrice de vérification) — sinon des morceaux de phrase
disparaissent silencieusement du PDF rendu.
