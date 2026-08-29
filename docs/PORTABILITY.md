# Portabilité — ce qui a été vérifié, ce qui reste incertain

Vérifié en construisant ce dépôt (2026-08-29), pas supposé.

## Ce qui est pleinement portable

`CLAUDE.md`, `emil-design-eng`, `webapp-testing`, `find-skills`,
`review-animations`, `animation-vocabulary` : texte pur (Markdown), aucune
dépendance de chemin, aucun outil externe requis pour LIRE et SUIVRE leurs
instructions. Copiés verbatim, zéro correction nécessaire.

`impeccable` : contenait des références en dur à son ancien emplacement
(`.agents/skills/impeccable/scripts/...`, dans `SKILL.md` et 5 fichiers de
`reference/`, plus 2 occurrences fonctionnelles dans `scripts/hook-admin.mjs`).
**Corrigées** dans cette copie vers `.claude/skills/impeccable/...` — la
convention réelle de ce dépôt. Preuve que ça fonctionne : au moment même où
`README.md` a été écrit dans ce dépôt, le harnais Claude Code a détecté et
listé les 6 skills copiés comme skills de projet actifs (visible dans les
system-reminders de la session ayant construit ce dépôt) — pas une simple
promesse, un fait observé.

## Trois réserves réelles, à connaître avant de compter dessus en cloud

1. **`impeccable` a un mécanisme de hooks** (`scripts/hook.mjs`,
   `hook-admin.mjs`, `hook-before-edit.mjs`) qui s'active en écrivant dans
   `.claude/settings.json` du projet (commande `$impeccable hooks on`).
   Copier les fichiers ne suffit pas à l'activer — c'est un geste à refaire
   par projet si tu veux le detector auto-run. Sans hooks activés, le skill
   reste utilisable normalement (polish, audit, critique...), seul
   l'auto-déclenchement après édition ne l'est pas par défaut.
2. **`webapp-testing` pilote Playwright** (`from playwright.sync_api import
   sync_playwright`). Les instructions sont portables telles quelles, mais
   leur EXÉCUTION suppose Python + le paquet `playwright` (+ navigateurs
   installés) disponibles dans l'environnement cloud. Les sessions Claude
   Code cloud provisionnent généralement ce qu'il faut à la demande, mais ce
   n'est pas garanti à 100 % — si `playwright` est absent, la première
   commande du skill (`pip install playwright && playwright install`) le
   révèle immédiatement, ce n'est pas un échec silencieux.
3. **`ui-ux-pro-max` mentionne une intégration MCP optionnelle** (« shadcn/ui
   MCP for component search and examples »). Le skill fonctionne pleinement
   sans elle (c'est une bibliothèque de guidance : styles, palettes,
   pairings — du texte, pas du code) ; seule la fonctionnalité de recherche
   de composants shadcn en direct dépend d'un serveur MCP configuré dans la
   session en cours, ce qui est propre à chaque environnement et ne se copie
   pas par fichier.

## Ce qui n'a PAS été copié, et pourquoi

`~/.agents/skills/` contient ~50 autres entrées (les familles `expo-*`,
`gsap-*`, `eas-*`, `shadcn`, `material-3`, `banner-design`, `brand`, `design`,
`design-system`, `enterprise`, `frontend-design`, `frontend-ui-ux`,
`industrial-brutalist-ui`, `minimalist-ui`, `mobile-app-ui-design`, `premium`,
`slides`, `swiftui-skills`, `task-observer`, `ui-styling`). Elles n'ont **pas
été utilisées** sur les projets qui ont produit `CLAUDE.md` (aladdin-site,
cham-site, bloodborne-site) — les inclure aurait gonflé ce dépôt de skills non
éprouvées par la méthode qu'il documente.

**Point non vérifié, à ne pas supposer réglé** : je n'ai pas pu confirmer
d'où vient exactement `~/.agents/skills/` (produit bundlé, marketplace de
plugins, ou convention partagée entre plusieurs outils sur cette machine) ni
si une session cloud fraîche les propose déjà nativement par un autre canal.
Si un futur toi le découvre, documente-le ici plutôt que de le supposer.

## Ce qui manque encore, et n'est volontairement pas dans ce dépôt

Les autres skills mentionnés dans `CLAUDE.md` §6 comme « génuinement
installées » à l'époque de sa rédaction. Si un futur projet en a besoin et
qu'elles se révèlent absentes en session cloud, ajoute-les à ce dépôt en
suivant le même protocole que ci-dessus (copier le contenu réel, jamais un
lien symbolique, corriger les chemins internes en dur, vérifier qu'aucun
`.agents/` ou `C:\Users\adamt` ne subsiste).
