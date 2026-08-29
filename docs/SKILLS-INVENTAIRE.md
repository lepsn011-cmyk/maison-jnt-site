# Inventaire des skills — état des lieux au 2026-08-29

Constaté en listant réellement le disque (`ls`, `diff`), pas supposé. Sert de
preuve à la sélection faite dans ce dépôt et de point de départ si un futur
toi doit en ajouter d'autres.

## Où vivent les skills sur la machine source (`C:\Users\adamt\`)

Deux emplacements, pas un seul :

- **`~/.claude/skills/`** — l'emplacement que le harnais Claude Code lit
  réellement.
- **`~/.agents/skills/`** — la plupart des entrées de `~/.claude/skills/`
  n'y sont que des **liens symboliques** vers ce second dossier. Un lien
  symbolique ne survit pas à un `git clone` sur une autre machine ni à une
  session cloud fraîche : c'est pour ça qu'une copie de fichiers réels était
  nécessaire, pas juste un pointeur.

## Les 7 skills copiés dans ce dépôt, et pourquoi

| Skill | Statut sur la machine source | Taille | Utilisé sur |
|---|---|---|---|
| `impeccable` | lien symbolique → `.agents/skills/impeccable` (2,3 Mo réels) | 2,3 Mo | cham-site, aladdin-site (audit + finition) |
| `ui-ux-pro-max` | lien symbolique → `.agents/skills/ui-ux-pro-max` (1,8 Mo réels) | 1,8 Mo | mentionné en Phase 1 de la méthode racine |
| `emil-design-eng` | dossier réel, **dupliqué à l'identique** dans `.agents/skills/` (diff vide) | 28 Ko | cham-site (motion), aladdin-site |
| `webapp-testing` | dossier réel, dupliqué à l'identique | 32 Ko | pipeline QA §7 de la méthode racine |
| `find-skills` | dossier réel, dupliqué à l'identique | 8 Ko | référencé en §6 de la méthode racine |
| `review-animations` | dossier réel, **local uniquement** (absent de `.agents/skills/`) | 24 Ko | outillage disponible, pas encore utilisé sur un projet documenté |
| `animation-vocabulary` | dossier réel, **local uniquement** | 16 Ko | idem |

## Les ~50 skills NON copiés

Tout le reste de `~/.agents/skills/` : les familles `expo-*` (13 entrées),
`gsap-*` (8), `eas-*` (6), plus `shadcn`, `material-3`, `banner-design`,
`brand`, `design`, `design-system`, `enterprise`, `frontend-design`,
`frontend-ui-ux`, `industrial-brutalist-ui`, `minimalist-ui`,
`mobile-app-ui-design`, `premium`, `slides`, `swiftui-skills`,
`task-observer`, `ui-styling`.

Raison du tri : aucune n'apparaît dans l'historique des projets qui ont
produit `CLAUDE.md`. Les copier aurait fait de ce dépôt une archive de tout
ce qui existe sur la machine plutôt qu'un reflet de la méthode réellement
pratiquée. Si un projet futur en a besoin, ajoute-la avec le même protocole
(voir `PORTABILITY.md`, dernière section).

## Ce qui n'est PAS un skill mais vit au même endroit

`~/.claude/plugins/` contient un cache de plugin (`claude-mem`, avec ses
propres `node_modules` — plusieurs milliers de fichiers). Ignoré ici : c'est
un plugin d'outillage de session (mémoire long-terme entre conversations),
pas un skill de méthode de conception, et son cache n'a aucun sens copié
hors de son mécanisme d'installation.
