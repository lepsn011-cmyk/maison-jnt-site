# project-bootstrap

Point de départ portable pour tout nouveau site vitrine premium : la méthode
d'agence (`CLAUDE.md`) + les skills réellement utilisés, dans le format exact
que Claude Code attend — pas une archive de référence à relire à la main.

Ce dépôt existe parce qu'une session cloud (GitHub-connectée, ex. depuis
iPad) démarre à vide : elle ne voit ni `C:\Users\adamt\CLAUDE.md`, ni
`~/.claude/skills/`, ni `~/.agents/skills/` — ces chemins n'existent que sur
la machine locale. Ce dépôt rend portable ce qui, sans lui, resterait
prisonnier d'un seul PC.

## Contenu

```
CLAUDE.md                          <- copie verbatim de C:\Users\adamt\CLAUDE.md
.claude/skills/
  impeccable/                      <- polish, audit, critique, palette...
  ui-ux-pro-max/                   <- styles, palettes, pairings typo, layout
  emil-design-eng/                 <- micro-interactions, motion
  webapp-testing/                  <- pipeline Playwright de vérification
  find-skills/                     <- découverte de skills installées
  review-animations/               <- audit d'animations
  animation-vocabulary/            <- glossaire terme <-> effet
docs/
  PORTABILITY.md                   <- ce qui ne fonctionne PAS à l'identique en cloud
  SKILLS-INVENTAIRE.md             <- état des lieux complet au 2026-08 (racine, tous les skills trouvés)
```

`.claude/skills/<nom>/SKILL.md` est la convention réelle de Claude Code pour
un skill de PROJET : une fois ces fichiers dans un dépôt, n'importe quelle
session Claude Code qui travaille dans ce dépôt (locale ou cloud) les
reconnaît et peut les invoquer directement — ce n'est pas un simple texte de
référence à copier-coller.

## Démarrer un nouveau projet (ex. Maison JNT)

**Méthode recommandée — dépôt modèle GitHub, marche depuis n'importe où y
compris l'iPad, aucune ligne de commande requise :**

1. Sur la page GitHub de `project-bootstrap`, active **Settings → Template
   repository** (case à cocher, une fois, voir note plus bas — je ne peux
   pas le faire moi-même sans authentification `gh`).
2. Pour chaque nouveau projet : bouton vert **« Use this template » → « Create
   a new repository »** en haut de la page du dépôt. Fonctionne à l'identique
   sur mobile Safari.
3. Nomme le nouveau dépôt (`maison-jnt-site`), crée-le.
4. Clone-le (ou ouvre-le directement dans une session cloud connectée à
   GitHub) : `CLAUDE.md` et `.claude/skills/` sont déjà à la racine, prêts à
   l'emploi — pas de fusion, pas de copie manuelle.
5. Supprime ensuite `README.md` et `docs/` (propres à *ce* dépôt, pas au
   site) une fois le nouveau projet initialisé, et adapte `CLAUDE.md` si le
   nouveau projet justifie un écart (voir sa Note finale : « une raison
   locale spécifique et vérifiée gagne »).

**Méthode alternative, si le mode template n'est pas activé :** clone
`project-bootstrap` dans un dossier temporaire, copie `CLAUDE.md` et
`.claude/` à la racine du nouveau dépôt, committe. Un peu plus de gestes,
même résultat.

**Ce qui NE marche PAS de façon fiable : cloner `project-bootstrap` à côté du
projet (dossier frère).** Claude Code charge `CLAUDE.md`/`.claude/skills`
depuis le répertoire du projet en cours et ses parents — pas depuis un
dossier voisin sans lien. Un clone côte à côte resterait invisible tant que
son contenu n'est pas copié DANS l'arbre du projet. D'où la méthode
« template » ci-dessus.

## Avant d'utiliser sur un vrai projet

Lis `docs/PORTABILITY.md` — trois skills ont des dépendances d'environnement
réelles (scripts Node, Playwright, un MCP optionnel) qui ne sont pas garanties
disponibles telles quelles dans une session cloud fraîche.
