# DESIGN.md — Maison JNT

> Système visuel. Écrit après la pose de la palette et de la typographie, avant le contenu détaillé
> (`CLAUDE.md` §1.1, §2 Phase 2). Lu par `impeccable` comme contexte de projet.

---

## 1. La palette est verrouillée — et pourquoi c'est un arbitrage, pas un oubli

Le client a donné sa couleur : **le beige de son logo** (beige rosé très doux). Non négociable.

La skill `impeccable` classe précisément cette bande — OKLCH L 0.84–0.97 / C < 0.06 / teinte 40–100 —
comme *« le défaut AI saturé de 2026 »*, et déconseille les noms de token `--beige`, `--cream`,
`--sand`.

**Arbitrage : le client gagne.** `CLAUDE.md` §2 Phase 1 est explicite : « palette du client si
fournie — elle est verrouillée et **prime sur toute liste de rejet AI-slop** ».

Mais le diagnostic sous la règle reste juste, et il est appliqué. **Le tell n'est pas le beige :
c'est le beige dilué en quasi-blanc, étalé sur toute la page, sans structure tonale.** D'où trois
décisions qui gardent la couleur du client tout en évitant le piège :

1. **Le beige est engagé, pas délavé.** Stratégie « Committed » d'`impeccable` : il porte la surface
   à sa valeur pleine — celle du carton du logo — pas à L 0.97.
2. **Un second beige plus profond** (`--grege`) alterne les bandes. La page a un relief tonal.
3. **Une section entière sur noir chaud** (l'éditorial « maison du mois »). La page possède une
   vraie architecture de contraste, pas un aplat de crème du début à la fin.

### Tokens

| Token | Valeur | Rôle |
|---|---|---|
| `--beige` | `oklch(0.906 0.016 65)` = `#E8DED5` | surface dominante — **mesurée** sur le logo |
| `--grege` | `oklch(0.858 0.018 65)` | bandes alternées, cartes, séparations |
| `--grege-fonce` | `oklch(0.798 0.020 65)` | filets, bordures, états au repos |
| `--encre` | `oklch(0.205 0.012 65)` | texte principal + surface éditoriale sombre |
| `--encre-douce` | `oklch(0.392 0.011 65)` | texte secondaire (jamais plus clair : cf. §5) |
| `--accent` | `oklch(0.44 0.09 40)` | **unique accent**, états interactifs |
| `--sur-encre` | `oklch(0.940 0.008 65)` | texte sur surface sombre |

### D'où vient le beige, exactement

`#E8DED5`, **échantillonné au pixel** sur le carton du logo dans la capture du profil
Instagram (zones plates, à l'écart du lettrage, médiane des pixels clairs). Il remplace une
estimation visuelle à `oklch(0.902 0.014 52)`.

L'écart tient en une ligne : **distance OKLab 0,0056**, RGB (+1, +2, −1) — tout juste au
seuil de perception. L'estimation initiale était bonne ; la mesure la remplace par principe,
pas parce que le rendu change. La teinte des neutres suit la mesure (65 au lieu de 52).

**Limite assumée** : la source est un JPEG d'une capture d'écran affichant le logo, pas le
fichier logo. Une ligne à corriger le jour où le vrai fichier arrive.

### L'accent, et une correction

`--accent` est un **bois de rose choisi** dans la famille chaude (teinte 40), retenu parce
qu'il évite le réflexe or-parfum qu'`impeccable` classe en piège de second ordre.

Une version antérieure de ce document le présentait comme « la teinte du beige poussée en
chroma ». C'était vrai tant que le beige était estimé à 52 ; la mesure le place à 65, et
l'accent reste délibérément à 40. Il est donc voisin, pas dérivé — la formulation est
corrigée ici plutôt que laissée à induire en erreur.

**Emploi de l'accent : ≤ 5 % de la surface.** Filtre actif, soulignement de lien, anneau de focus.
Rien d'autre. Le beige est la couleur engagée ; l'accent est retenu.

### Les familles olfactives ne sont pas codées par couleur

Six familles = six teintes = la fin de « un accent discret unique », et une violation de
`color-not-only` (`ui-ux-pro-max` §1). Les familles sont **nommées**, différenciées
typographiquement. Aucune pastille colorée.

---

## 2. Typographie

Directive client : *serif fin en capitales espacées pour les titres, sans-serif discret pour le
corps.*

| Usage | Fonte | Justification |
|---|---|---|
| Display / titres | **Bodoni Moda** | Didone à fort contraste — fait écho au « JNT » du logo, qui est un didone |
| Corps + petites étiquettes | **Jost** | Géométrique discret, calme, bon rendu des accents français |
| Mot-signature « Maison » | **Italianno** | **Uniquement** dans la reconstruction du wordmark |

Pairing validé par `ui-ux-pro-max` (`--domain typography`, entrée « Luxury Minimalist »).

**Rejeté : Playfair Display + Inter**, que la même skill proposait en premier résultat (« Classic
Elegant »). C'est le réflexe « luxe » saturé — `impeccable` le classerait en AI-slop. Bodoni est à
la fois plus juste vis-à-vis du logo et moins prévisible.

### Règles dures

- **Bodoni Moda uniquement ≥ 24 px.** Ses déliés disparaissent en petit corps et échouent au
  contraste réel. Toute étiquette < 24 px est en Jost.
- Capitales espacées : `letter-spacing` 0.12–0.18em sur les titres de section.
- Interlettrage display **≥ −0.04em** (plancher `impeccable`) — ici on reste positif, la direction
  est à l'espacement, pas au resserrement.
- Corps ≥ 16 px, interligne 1.6, mesure plafonnée à 68ch.
- `text-wrap: balance` sur h1–h3, `pretty` sur la prose.
- Italianno n'apparaît **qu'une fois** par écran. La signature manuscrite du logo inspire, elle ne
  se surexploite pas (directive client).

---

## 3. Densité et rythme

La boutique physique vend l'abondance (murs de flacons). La grille le dit :

| Largeur | Colonnes |
|---|---|
| 375 px | 2 |
| 768 px | 3 |
| 1440 px | 4 |

**Rejeté : « Exaggerated Minimalism / massive whitespace »**, recommandé par `ui-ux-pro-max`. Trois
produits par écran contrediraient l'argument commercial du client.

Échelle d'espacement de section : **80 px mobile / 120 px desktop** (valeur éprouvée sur
`cham-site`, `CLAUDE.md` §2 Phase 4). Espacement interne sur trame de 4 px.

---

## 4. Mouvement — budget serré, dérivé de `emil-design-eng`

Le cadre de décision de la skill part de la **fréquence d'usage**. Appliqué ici, il donne un
résultat contre-intuitif, retenu quand même :

| Interaction | Fréquence | Décision |
|---|---|---|
| Bascule d'un filtre | dizaines de fois/jour | **Aucune animation de grille.** Re-rendu instantané. Seule la puce transitionne (120 ms). |
| Survol de carte | dizaines de fois/jour | Réduit : fond + filet, 120 ms. Pas de lift, pas de scale. |
| Ouverture d'une fiche | occasionnel | 220 ms, *origin-aware* — part de la carte cliquée |
| Fermeture d'une fiche | occasionnel | 150 ms (≈ 65 % de l'entrée) |
| Premier rendu de la grille | rare | Stagger 35 ms, plafonné aux 12 premières cartes |
| Panneau filtres mobile | occasionnel | 300 ms, courbe drawer |

Animer la grille à chaque filtrage rendrait le catalogue *plus lent à l'usage* : c'est le geste le
plus répété du site.

### Tokens d'easing (repris verbatim de la skill)

```css
--ease-out:    cubic-bezier(0.23, 1, 0.32, 1);
--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);
```

**Jamais `ease-in`** sur une animation d'interface.

### `prefers-reduced-motion`

Toutes les durées → 0.01 ms, stagger supprimé, fiche en fondu simple. **Le contenu est visible par
défaut** : aucune visibilité n'est conditionnée à une classe ou à un `IntersectionObserver`
(`impeccable` : un reveal doit enrichir un état déjà visible, jamais le produire).

---

## 5. Contraintes vérifiées, pas supposées

- Contraste mesuré par **échantillonnage pixel composite** (texte rendu transparent + capture +
  `Range.getClientRects()`), jamais par calcul token contre token.
- `getComputedStyle().color` peut renvoyer `oklch(...)` : toute couleur est résolue par aller-retour
  `<canvas>` (`CLAUDE.md` §4.9).
- `--encre-douce` est le **plancher** du texte secondaire. Le gris clair « pour l'élégance » est,
  selon `impeccable`, la première cause d'illisibilité des designs générés.
- Cibles tactiles ≥ 44 × 44 px, y compris chaque puce de filtre.
- Échelle de `z-index` sémantique — jamais 999 ni 9999.

---

## 6. Interdits appliqués (`impeccable`, bans absolus)

- ❌ Gradient text (`background-clip: text`)
- ❌ Glassmorphism décoratif — **y compris contre l'avis de `ui-ux-pro-max`**, qui recommandait
  « Liquid Glass + Glassmorphism » pour le type produit « E-commerce Luxury ». Interdit absolu chez
  `impeccable`, qui fait autorité sur le polish (`CLAUDE.md` §6).
- ❌ Bordure latérale colorée > 1 px
- ❌ Kicker capitales espacées au-dessus de *chaque* section
- ❌ Marqueurs numérotés 01 / 02 / 03 en scaffolding
- ❌ `border: 1px solid` **+** `box-shadow` ≥ 16 px sur le même élément
- ❌ `border-radius` > 16 px sur les cartes
- ❌ Fonds à rayures / grilles décoratives, illustrations SVG « croquis »
- ❌ Emoji en guise d'icône

## 7. Interdits métier (demande explicite du client)

Bandeau défilant · prix barrés · pastilles de remise · « ajouter au panier » · newsletter −10 % ·
badges de réassurance.

**Vérifiés par grep sur le texte rendu** (`innerText` via Playwright), pas sur la source — c'est la
couche qui compte (`CLAUDE.md` §8.1).

---

## 8. Assets — état réel

Aucun fichier client n'est sur le disque à ce jour. Rien n'est simulé comme présent :

| Attendu | Traitement provisoire |
|---|---|
| `assets/logo-jnt.svg` (ou `.png` détouré) | Wordmark **reconstruit typographiquement**, isolé dans un composant unique → remplacement en une édition |
| `assets/boutique-interieur.jpg` | Placeholder patterné, **nom de fichier affiché en clair**, ratio réservé (zéro décalage à l'intégration) |

La valeur `--beige` est **estimée visuellement** depuis une capture Instagram — pas mesurée au
pixel, faute de fichier. Un seul token à corriger dès réception du logo.
