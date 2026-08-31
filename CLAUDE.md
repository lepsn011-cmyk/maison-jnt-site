# CLAUDE.md — Sites vitrine premium : méthode d'agence

Tu n'as aucun souvenir des projets qui ont produit ce fichier. Peu importe. Ce document synthétise quatre constructions complètes de sites vitrine premium (un tribute jeu vidéo, deux restaurants, un antiquaire) — des dizaines d'heures d'itération, des bugs payés cher, une méthode qui a convergé. Les §0-§7 couvrent le design/build d'un site **statique** ; la **§8 couvre la dimension backend / infrastructure / opérations** qu'a introduite le quatrième projet (site vivant piloté par le client). Lis-le en entier avant de toucher au premier fichier d'un nouveau projet.

Le principe qui chapeaute tout : **ne jamais affirmer qu'un rendu est correct sans l'avoir vu.** Deuxième principe, aussi cher : **ne jamais prétendre qu'un actif partagé existe s'il n'a pas été vérifié sur le disque.** Troisième principe, du projet le plus récent, qui généralise les deux premiers : **vérifie toujours à la SOURCE — DNS autoritatif, certificat servi, fichier réel sur disque, log/e-mail d'erreur, fichier réellement servi en production — jamais à une couche d'affichage qui ment ou retarde.** Et corollaire immédiat : **une hypothèse causale rapportée (par le client ou par toi-même) n'est pas un diagnostic — c'est une corrélation à prouver.**

---

## 0. État réel des actifs — lis ça avant de chercher un raccourci

Il n'existe **aucune skill dédiée, aucune bibliothèque de composants, aucun template** pour ces sites. Ce sont quatre dossiers indépendants à la racine de `C:\Users\adamt\` :

| Projet | Structure | Maturité | Ce qu'il illustre |
|---|---|---|---|
| `bloodborne-site/` | fichier unique | méthode documentée en détail (son propre `CLAUDE.md` local, absorbé ici) | brief créatif, diagnostic comparatif, AI-slop |
| `grec-algerien-site/` | fichiers séparés (`index.html` + `style.css` + `script.js`) | simple, antérieur | approche multi-fichiers — **abandonnée depuis**, voir §1.0 |
| `cham-site/` | fichier unique, + `PRODUCT.md`/`DESIGN.md` | le plus mature côté DESIGN, deux passes complètes (polish puis premium) | pipeline QA aboutie, chorégraphie hero, PRODUCT.md/DESIGN.md comme contexte skill |
| `aladdin-site/` | multi-fichiers (`index.html`+`theme.css`+`script.js`+`catalogue.js`) + fonctions Netlify + outillage `outils/` | le plus mature côté BACKEND/OPÉRATIONS ; son `CLAUDE.md` local tient un journal daté très détaillé | **site VIVANT** : backend serverless, console client autonome, API LLM externe, hébergement facturé, domaine propre, SEO/indexation — c'est la source de la §8 |

**Si un futur toi cherche une skill "site-commerce-premium" ou un dossier `/site-library/` ou `/templates/restaurant/` : ils n'existent pas.** Ne les invente pas, ne les suppose pas créés dans une session précédente non retrouvée. Si le besoin de consolidation en bibliothèque réutilisable se fait sentir (deux projets restaurant partagent déjà la structure carte/avis/contact/footer et la logique de scrim-sur-photo), **propose-le explicitement à l'utilisateur** avant de le construire — c'est un vrai chantier, pas une supposition à faire silencieusement.

**Ordre de consultation avant de générer quoi que ce soit from-scratch** :
1. Regarde si un projet-sœur existant (`cham-site/` en priorité — le plus abouti) résout déjà un problème similaire (grille de menu, overlay de section avis, QA de contraste). Copie le *pattern*, jamais les valeurs concrètes (couleurs, textes) d'un projet à l'autre.
2. Consulte les skills génuinement installées (`impeccable`, `emil-design-eng`, `ui-ux-pro-max`, `webapp-testing`) — voir §3.
3. Seulement ensuite, écris du code neuf.

---

## 1. ARCHITECTURE — décision tranchée

### 1.0 Fichier unique HTML/CSS/JS, pas de split

`grec-algerien-site` (fichiers séparés) a précédé `cham-site` (fichier unique) et n'a pas été repris depuis. Le fichier unique a gagné dans la pratique : zéro problème de chemin relatif, un seul `<style>` à faire défiler pour auditer toute la palette, déploiement Netlify trivial (un dossier, `index.html` à la racine, aucun build step). **Pour tout nouveau site vitrine one-page, pars sur un fichier unique.** N'introduis un split que si le site dépasse largement l'échelle one-page (multi-pages réelles, pas juste des ancres).

### 1.1 PRODUCT.md / DESIGN.md comme contexte de skill

`cham-site/` et `aladdin-site/` ont ces fichiers — ajoutés pour donner du contexte à la skill `impeccable` (register `brand`, users, palette verrouillée, anti-références). Deux projets sur quatre les ont, et ce sont les deux plus aboutis : le lien n'est pas un hasard. **Crée-les dès le début d'un nouveau projet**, pas après coup : ils évitent que la skill design réinvente une palette ou un ton qui contredit un brief déjà donné par le client.

---

## 2. WORKFLOW CLIENT DE BOUT EN BOUT

### Phase 1 — Collecte (avant tout code)

- Récupère ou déduis : nom, adresse, téléphone, horaires, carte/prix, univers/ton, photos réelles du lieu (si le client en a — sinon poser la question avant de sourcer des stocks).
- **Vérifie le format réel des assets fournis dès réception.** Sur `cham-site`, les `.jpg` livrés par le client étaient en réalité des PNG renommés (12,3 Mo pour 5 images). `PIL.Image.open(...).format` avant tout usage — ne fais jamais confiance à l'extension.
- Écris `PRODUCT.md` (register, users, purpose, brand personality, anti-références, principes, accessibilité) avant la première ligne de HTML. Fais-le confirmer par l'utilisateur si le brief est sparse — ne synthétise pas un PRODUCT.md complet à partir d'une phrase.
- Écris `DESIGN.md` une fois qu'un premier système de couleurs/typo existe (palette du client si fournie — elle est verrouillée et prime sur toute liste de rejet AI-slop — sinon dérivée du brief).

### Phase 2 — Assemblage / structure

- Une section à la fois : nav, hero, contenu principal (carte/menu), avis, contact, footer.
- Palette + typographie posées AVANT le contenu détaillé — pas l'inverse.
- Placeholders patternés (pas de gris vide) tant qu'un asset réel manque, avec le nom du fichier attendu affiché en clair (`assets/hero.jpg` visible en légende) — ça évite l'ambiguïté "l'image est cassée" vs "l'image n'a jamais été fournie".

### Phase 3 — Personnalisation / intégration des assets réels

- Détourage logo si besoin (voir §4, méthode PIL par seuil de luminance).
- Intégration des photos réelles → généralement le moment où les scrims/overlays théoriques du brief s'avèrent insuffisants au contraste réel (voir §4). Prévois cette itération, ne la découvre pas en fin de projet.
- Conversion systématique des formats mal fournis en JPEG progressif optimisé (voir §4).

### Phase 4 — Polish (skill `impeccable`)

- Invoque `impeccable` une fois la structure et le contenu stables — pas sur un squelette encore instable.
- Grille systématique : hiérarchie, espacement (échelle 80px mobile / 120px desktop validée sur cham-site), cohérence des tokens couleur, états d'interaction complets (hover/focus/active/disabled), responsive aux 3 largeurs.
- C'est la phase où `emil-design-eng` s'invoque pour toute décision d'animation/micro-interaction — easing, durée, justification narrative de chaque mouvement.

### Phase 5 — QA (voir §5 pour les critères binaires)

- Contraste par pixel (méthode canvas, jamais le calcul théorique token-vs-token).
- Overflow 375/768/1440, cibles tactiles ≥44px, console vierge, `prefers-reduced-motion` complet.
- Rapport honnête avec note chiffrée justifiée dimension par dimension, jamais un score global impressionniste.

### Phase 6 — Livraison / déploiement

- Site statique → Netlify (ou équivalent) sans build step : `git init` → repo GitHub → import Netlify → publish directory `.`.
- Rendre le repo GitHub privé si le client le demande, mais **prévenir que ça ne rend pas le site déployé privé** — c'est un malentendu fréquent. La protection par mot de passe Netlify est payante ; l'alternative gratuite est un header Basic Auth via `netlify.toml`, à proposer seulement si le client insiste (sinon c'est un chantier hors scope).

---

## 3. QUEL MODÈLE / EFFORT POUR CHAQUE PHASE

Cette section synthétise ce qui a été observé fonctionner, pas une règle abstraite :

| Phase | Modèle recommandé | Effort | Pourquoi |
|---|---|---|---|
| Collecte, PRODUCT.md/DESIGN.md | Sonnet, effort normal | Standard | Synthèse structurée à partir du brief, pas de créativité visuelle à inventer |
| Assemblage structure + contenu | Sonnet, effort normal | Standard | Mécanique — HTML/CSS répétitif à partir d'un système déjà posé, pas besoin d'un modèle plus coûteux |
| Intégration assets réels (détourage, conversion, scrims) | Sonnet, effort normal | Standard | Diagnostic technique + mesure, pas de créativité |
| **Passe créative exceptionnelle** (hero cinématique, direction artistique qui doit "faire 10 000€", chorégraphie sur-mesure) | **Fable**, sur demande explicite du client | Élevé | Réservé aux moments où le client demande explicitement un niveau au-dessus du polish standard — c'est la passe qui a produit la chorégraphie hero de `cham-site` (ken burns, séquence lettre-par-lettre, profondeur au pointeur). Ne bascule pas sur Fable par défaut : c'est plus coûteux et le gain n'est perceptible que sur les décisions vraiment créatives, pas sur l'exécution mécanique. |
| QA, mesure de contraste, audit responsive | Sonnet, effort normal (peut déléguer à un agent Explore/general-purpose pour des scans larges) | Standard | Scripts déterministes, pas de jugement créatif |
| Debug d'un bug visuel non compris (stacking context, deadlock d'observer) | Sonnet, effort élevé si le premier diagnostic échoue | Standard → élevé | Monte l'effort seulement après un premier essai infructueux, pas préventivement |

**Règle pratique** : reste sur Sonnet effort normal par défaut. Ne monte en modèle/effort que sur signal explicite du client ("je veux du 10/10", "rends-le spectaculaire", refus répété d'un rendu jugé "générique") — c'est le signal qui a déclenché la passe Fable sur `cham-site`, pas une anticipation de ta part.

---

## 4. ERREURS HISTORIQUES À NE JAMAIS RÉPÉTER

*Fusion des leçons `bloodborne-site` + `cham-site`. Chacune a été payée par une session réelle.*

### Diagnostic et vérification

1. **Affirmer qu'un rendu est correct sans l'avoir regardé.** La leçon la plus chère, répétée sur plusieurs projets avant de rentrer. L'observation de l'utilisateur gagne toujours face à une inspection de code — va vérifier, ne discute pas.
2. **Diagnostiquer depuis un rendu d'outil (Grep) plutôt que le fichier réel.** Un artefact d'affichage d'outil a été signalé comme "commentaire CSS corrompu" — le fichier réel était intact. Confirme toujours via `Read` direct avant de signaler une anomalie de syntaxe.
3. **Confirmer une tâche accomplie sans preuve reproductible.** "C'est fait" doit toujours venir avec un chemin de screenshot, un extrait de sortie de script, ou une mesure chiffrée.
4. **Ne pas vérifier le format réel d'un asset fourni.** Des `.jpg` de 12,3 Mo au total étaient en réalité des PNG renommés — `PIL.Image.open().format` avant tout usage, jamais confiance à l'extension.

### Bugs CSS/JS récurrents (grep-les tous dès qu'un apparaît une fois)

5. **`backdrop-filter` sur une nav fixe devient le containing block de ses descendants `position:fixed`.** Le panneau de menu mobile `inset:0` se retrouve écrasé à la hauteur de la barre. Fix : neutraliser le `backdrop-filter` sur la classe d'état ouvert (`.menu-open { backdrop-filter: none }`).
6. **`position: relative` sans `z-index` explicite ne contient pas ses enfants en `z-index` négatif** — une image de fond en `z-index:-1` s'échappe et se peint derrière toute la page. Dès qu'un bug de ce type est trouvé sur une section, grep immédiatement toutes les sections pour le même pattern.
7. **`clip-path: inset(0 0 100%)` sur l'élément OBSERVÉ par un `IntersectionObserver` annule sa surface d'intersection.** Chromium calcule l'intersection après clip → `isIntersecting` reste `false` pour toujours, aucune erreur console, deadlock silencieux. Toujours porter le clip de révélation sur un enfant (l'`<img>`), jamais sur l'élément observé.
8. **`getBoundingClientRect()` sur un élément `text-align:center` en `display:block`** retourne la boîte pleine largeur du bloc, pas la largeur réelle du texte rendu — pollue toute mesure de contraste qui en dépend (capture des pixels de fond loin du texte réel). Fix : `Range.selectNodeContents(el).getClientRects()[0]` pour une bbox collée aux glyphes.
9. **`getComputedStyle().color` peut renvoyer `oklch(...)` sur Chromium récent** et casser silencieusement un parsing basé sur `rgb(...)`. Résous toujours la couleur réelle via un round-trip `<canvas>` `fillStyle`/`getImageData`, jamais un regex sur la chaîne CSS.

### Direction artistique

10. **Overlay semi-transparent plat par défaut au lieu d'un scrim dégradé justifié.** Un voile uniforme aplatit la photo au lieu de la révéler — c'est le réflexe AI-slop. Scrim asymétrique (dense où le texte doit se lire, transparent où l'image doit respirer), justifié par la composition réelle de la photo.
11. **Contraste théorique (token vs token) ≠ contraste réel sur une photo.** Un overlay à l'opacité exacte du brief peut échouer au contraste réel sur une zone claire de la photo (ex. reflet doré). Mesure toujours le composite réel (texte rendu transparent, screenshot, échantillonnage pixel), assombris au-delà de la valeur théorique si la mesure l'exige.
12. **Pictogramme SVG plat à côté d'une photographie réelle** = le moment le plus "maquette" du site. Si un élément narratif existe déjà dans l'image, utilise-le au lieu d'ajouter une icône.
13. **Un h1 texte qui duel visuellement avec un wordmark déjà gravé dans l'image/logo.** Un seul point focal typographique par section — démote l'un des deux (taille, position) plutôt que les laisser se concurrencer. (Sur `cham-site`, le kicker arabe الشام a été supprimé du hero car redondant avec la calligraphie déjà présente dans le logo — gardé seulement dans l'`alt` pour l'accessibilité.)
14. **Recadrage mobile naïf (`object-fit: cover`) sur une image qui porte un élément textuel intégré** peut couper un wordmark en fragment illisible. Génère un crop mobile dédié quand c'est le cas.
15. **Installer/exécuter du code tiers sans vérification** — toujours confirmer qu'un repo existe réellement avant de l'installer ou de l'exécuter.

---

## 5. CRITÈRES DE VALIDATION BINAIRES — avant toute livraison

Chaque ligne doit être **mesurée**, pas estimée à l'œil. Aucune livraison ne sort tant qu'une case est rouge sans justification explicite documentée dans le rapport.

- [ ] **Contraste** : toutes les zones de texte critique ≥ 4.5:1 (normal) / 3:1 (large), mesuré par échantillonnage pixel composite (texte rendu transparent + screenshot + Range API), pas par calcul théorique token-vs-token.
- [ ] **Overflow horizontal** : 0px à 375 / 768 / 1440, mesuré (`document.documentElement.scrollWidth - clientWidth`), pas visuel.
- [ ] **Cibles tactiles** : toutes ≥ 44×44px aux largeurs mobile/tablette (audit DOM automatisé, pas un coup d'œil).
- [ ] **Console** : 0 erreur, 0 warning, 0 requête réseau échouée, aux 3 largeurs.
- [ ] **`prefers-reduced-motion`** : 100% du contenu visible d'emblée sans JS/animation, toutes les boucles et cinématiques coupées — testé avec `reduced_motion='reduce'` en contexte Playwright, pas supposé.
- [ ] **Format des assets** : vérifié via lecture du format réel (PIL/exiftool), pas via l'extension du fichier. Poids total du dossier assets raisonnable pour du web (viser <2 Mo total sauf raison spécifique).
- [ ] **Aucune mention d'un service que le client a explicitement quitté** (ex. Uber Eats sur `cham-site`) — grep exhaustif, pas une relecture visuelle.
- [ ] **Logo/wordmark sur photo** : contraste non-text ≥ 3:1 au p05 (5e percentile), mesuré par échantillonnage du fond réel derrière l'élément, logo masqué pendant la capture.
- [ ] **Menu mobile / burger** : ouvert et vérifié par screenshot à chaque largeur tactile, pas juste au desktop.
- [ ] **Rapport de livraison** : note chiffrée par dimension (jamais un score global seul), limites de la vérification explicitement documentées (ex. "transitions validées en état initial/final, pas en inspection frame par frame").

---

## 6. SKILLS DISPONIBLES ET QUAND LES UTILISER

- **`impeccable`** — polish final une fois structure/contenu stables. Lit `PRODUCT.md`/`DESIGN.md` si présents (Phase 4). Ne l'invoque pas sur un squelette instable.
- **`emil-design-eng`** — toute décision d'animation/micro-interaction : easing, durée, justification narrative. Convoque-la dès qu'une animation semble décorative plutôt que fonctionnelle.
- **`ui-ux-pro-max`** — hiérarchie visuelle, palettes de référence, pairings typographiques, structure de layout par type de produit. Utile en Phase 1 pour ancrer les choix dans du testé plutôt que d'improviser.
- **`webapp-testing`** — pipeline Playwright pour toute vérification visuelle nécessitant un serveur local. Le tool preview intégré peut être peu fiable (timeouts) ; bascule sur un `ThreadingHTTPServer` + Playwright sync autogéré (voir pattern §7) sans insister après un ou deux échecs.
- **`find-skills`** — avant d'écrire du code from-scratch pour une tâche qui a probablement déjà une skill dédiée (bannières, PDF, xlsx...).

**Séquencement** : brief (`ui-ux-pro-max`) → assemblage section par section → vérification (`webapp-testing`) → polish global (`impeccable` + `emil-design-eng` pour le motion) → QA finale (contraste, overflow, console).

---

## 7. PATTERN TECHNIQUE RÉUTILISABLE — pipeline QA

```python
# ThreadingHTTPServer éphémère + Playwright sync — fonctionne de façon fiable
# là où le tool preview intégré peut timeout.
import functools, threading
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright

handler = functools.partial(SimpleHTTPRequestHandler, directory=r'CHEMIN_DU_PROJET')
handler.log_message = lambda *a, **k: None
server = ThreadingHTTPServer(('127.0.0.1', 0), handler)
threading.Thread(target=server.serve_forever, daemon=True).start()
port = server.server_address[1]
# ... piloter via sync_playwright(), toujours fermer browser + server.shutdown()
```

Scripts à recréer en tête de chaque nouveau projet (`scratchpad/shoot.py`, `scratchpad/qa.py`) :
- `shoot.py` : `--out PATH --section ID --width N --height N --fullpage --settle MS --click SELECTOR`
- `qa.py` : contraste par échantillonnage pixel (fonds unis via round-trip canvas ; composites via texte transparent + `Range.getClientRects()`), overflow, erreurs console — sortie `OK`/`FAIL` par zone avec ratio chiffré.

---

## 8. SITES VIVANTS — backend, infrastructure facturée, autonomie client, opérations

*Les §0-§7 supposent un site statique livré une fois. Un site que le client PILOTE lui-même (console d'admin, ajout autonome de contenu, statuts) et qui parle à des services externes (API LLM, stockage git, e-mail) ouvre une dimension entière que le design ne couvre pas. Ces leçons sont transférables à TOUT projet ayant ces ingrédients — pas seulement à un catalogue.*

### 8.1 Diagnostic : vérifier à la source, et ne jamais fixer une hypothèse

- **La couche d'affichage ment ou retarde. Descends à la source autoritative.** DNS → interroge les serveurs autoritatifs directement (un `NXDOMAIN` à l'autoritatif = réellement absent, pas « en cours de propagation » ; un résolveur public peut cacher). Certificat → inspecte le certificat servi au handshake (`openssl s_client`), pas le cadenas « sécurisé » du navigateur. État déployé → `curl` les fichiers réellement servis, pas l'état du dépôt (le local peut être en avance ou en retard sur la prod). Cause d'un bug → le log / l'e-mail de rejet / le status HTTP réel, pas ce qu'on suppose.
- **Une hypothèse causale rapportée n'est pas un diagnostic.** « Ça a marché quand j'ai retiré X » est une corrélation, pas une causalité — souvent, autre chose a changé en même temps (le temps écoulé, un quota qui s'est rechargé, un cache). Trouve la vraie cause AVEC PREUVE avant de toucher au code, et explique le mécanisme réel plutôt que d'accepter l'hypothèse.
- **Tes propres suppositions méritent la même défiance, surtout quand tu es sûr.** Une réponse « évidente » sur ce qu'un hébergeur/une plateforme/une interface propose peut être fausse (mauvais produit, option repliée, comportement non documenté). Vérifie avant d'affirmer.
- **La couche que tu MESURES doit être celle qui compte.** Le contraste d'un élément dans son état actif (focus, survol) ne dit rien de sa lisibilité au repos ; mesurer l'état facile ne valide pas l'état par défaut. Idem : un « déploiement réussi » ne prouve pas que le changement est reflété — vérifie la donnée/le fichier réellement servi.

### 8.2 Infrastructure facturée ou à quota : l'anticiper AVANT de coder

- **Un modèle de coût par action doit façonner l'architecture dès la conception, pas après la première facture.** Un coût fixe par déploiement → regroupe les déploiements, et sépare l'action FRÉQUENTE du client de ce qui déclenche un déploiement (une bascule de statut ne doit pas coûter un build complet).
- **Un quota « par minute avec réservation » fait échouer une requête PAR CONSTRUCTION.** Si le fournisseur réserve le maximum de tokens/ressources demandé AVANT d'exécuter, une requête qui demande trop échoue quel que soit l'usage réel. Dimensionne chaque appel sur son besoin RÉEL mesuré, jamais sur un plafond confortable, et additionne le coût des appels enchaînés dans la même fenêtre.
- **Un réessai doit être conscient du temps ET de la nature de l'erreur.** Rejouer immédiatement contre une limite par minute ne peut pas réussir (deux échecs dans la même seconde). Distingue le transitoire (429/5xx → attendre, respecter `retry-after`) du définitif (jamais réessayé, c'est du temps perdu), et plafonne l'attente pour ne pas faire expirer la fonction — mieux vaut un message actionnable qu'un timeout opaque.
- **Vérifie le gain réel d'une dépense avant de la conseiller.** Un upgrade payant n'achète parfois qu'un confort, pas une capacité qui manque — dis-le franchement au client plutôt que de laisser payer un abonnement qui ne change rien.

### 8.3 Un correctif de code NE répare PAS les données déjà écrites

- Corriger le code qui a produit un bug ne corrige jamais les **enregistrements déjà corrompus** par ce bug. Pire : un enregistrement fautif peut bloquer **silencieusement** tout un système (une validation globale qui rejette à cause d'une vieille donnée invisible). Après tout correctif touchant à la production de données, pose explicitement la question : **faut-il aussi une migration/correction des données existantes ?**
- **Quand une écriture passe par plusieurs chemins (manuel + autonome, formulaire + import), ils doivent avoir le MÊME filet de validation.** Un bug entre toujours par le chemin le moins gardé. Si un contrôle existe sur un chemin, vérifie qu'il existe sur tous.

### 8.4 Séparer les interfaces à faible risque des interfaces à texte libre — dès la conception

- **La sûreté d'une interface vient de sa FORME, pas de la discipline de l'utilisateur.** Une interface à énumération fermée (boutons, bascule d'état, choix contraint) ne PEUT pas injecter de contenu arbitraire dans le dépôt ; une interface à texte/voix libre le peut et exige validation, marqueurs et structuration. Conçois-les séparées : le geste fréquent et sûr d'un côté, le geste rare et risqué de l'autre.
- **Une donnée contrainte (prix, identifiant, date) ne doit jamais être du texte libre, ni être extraite par une IA depuis de la prose.** Normalise-la de façon déterministe côté serveur. Une donnée commerciale mal extraite est une valeur FAUSSE publiée — et un montant faux se remarque.
- **Si une donnée n'a pas de champ dédié, l'utilisateur la mettra où il peut** (dans la description, dans un coin). Ce n'est pas son erreur, c'est un manque de l'interface. Le vrai correctif est le champ manquant, pas un rappel à l'ordre de l'utilisateur.

### 8.5 Opérations : git, déploiement, domaine

- **Committe/sauvegarde avant toute opération risquée** ; vérifie l'état RÉEL (git status, DNS, certificat) plutôt qu'un affichage. Avant un `git checkout`/`reset`/`clean`, regarde ce qui serait perdu.
- **Avant un push, récupère et inspecte ce que le distant contient et que tu n'as pas.** Un système autonome (console client) peut pousser des commits pendant ton travail. Rebase proprement, et prouve zéro conflit en confirmant que les fichiers touchés sont disjoints — ne fusionne jamais à l'aveugle.
- **Piège de branche** : une branche locale qui suit un distant de nom DIFFÉRENT (`master` → `main`) fait échouer un `git push` nu, ou pire crée une branche fantôme qui ne déclenche aucun déploiement. Vérifie où un push atterrit réellement (`git push origin HEAD:<branche>` explicite).
- **Regroupe les opérations coûteuses ou irréversibles** (déploiements) : prépare et committe en local, déploie une SEULE fois, groupé. Sur une contrainte de coût, prépare un changement cosmétique et **laisse-le voyager gratuitement avec le prochain vrai déploiement** plutôt que de dépenser un déploiement dédié.
- **Après un déploiement, vérifie que le CHANGEMENT est en production** (le fichier/la donnée réellement servi), pas seulement que le workflow « a réussi ».
- **Fige l'identité d'un site AVANT de le signaler à un moteur de recherche.** Fais la migration de domaine/DNS d'abord, puis fixe canonical/OG/sitemap sur une valeur unique (réécrite en un geste par un petit outil, jamais à la main), et SEULEMENT ENSUITE demande l'indexation — sinon tu provoques une migration de signaux inutile. Et rappelle au client que l'indexation elle-même n'a aucune date garantie : c'est le moteur qui décide.
- **Certaines actions à fort levier ne sont pas du code et t'appartiennent à toi, pas à l'agent** (créer un compte, valider une propriété, souscrire, brancher un DNS). Identifie-les tôt, liste-les clairement au client, et ne prétends jamais pouvoir les faire à sa place.

### 8.6 Patcher un fichier de données plutôt que le régénérer

- Quand tu modifies un fichier de données par outillage (au lieu de le régénérer entièrement — utile s'il porte des commentaires ou une structure écrite à la main), **teste le mécanisme contre le VRAI fichier sur disque, avec ses vraies fins de ligne et son vrai encodage**, jamais un mock synthétique propre. Le CRLF vs LF, un BOM, un champ étalé sur plusieurs lignes cassent des heuristiques qui « marchent » sur un exemple fabriqué (piège rencontré deux fois sur le même fichier).
- **Prouve la correction par inversion, pas par heuristique** : applique N patchs, défais-les tous, exige une égalité **octet pour octet** avec l'original. Une réversion exacte garantit qu'aucun octet hors cible n'a bougé — un contrôle bien plus fort qu'une relecture.

---

## 9. ÉCARTS LOCAUX — projet Maison JNT (2026-08)

*La « Note finale » autorise une raison locale spécifique et vérifiée à l'emporter sur une règle générale, à condition de la documenter. Voici les trois écarts de ce projet, et quatre leçons neuves.*

### 9.1 Deux fichiers au lieu d'un (§1.0)

`index.html` + `catalogue.js`. Le brief impose un catalogue « 100 % piloté par un fichier de données », et le client doit pouvoir éditer ses parfums sans ouvrir le HTML. **`catalogue.js` déclare `window.CATALOGUE` — surtout pas un `fetch()` de JSON**, qui casserait à l'ouverture en `file://`.

### 9.2 Le beige l'emporte sur l'anti-slop d'`impeccable` (§2 Phase 1)

`impeccable` classe la bande OKLCH L 0.84-0.97 / C < 0.06 / teinte 40-100 comme « le défaut AI saturé de 2026 » — exactement le beige du logo client. **La palette client est verrouillée et prime**, la règle §2 le dit.

Mais le diagnostic sous la règle reste juste et il a été appliqué : le tell n'est pas le beige, c'est **le beige dilué en quasi-blanc sur toute la page sans structure tonale**. D'où beige à valeur pleine (stratégie « Committed »), second beige plus profond en bandes alternées, et une section entière sur noir chaud. La page a une architecture de contraste, pas un aplat.

### 9.3 Les skills se contredisent — il faut trancher, pas empiler

`ui-ux-pro-max` recommandait pour « E-commerce Luxury » un style **Glassmorphism**, interdit absolu chez `impeccable`. Elle proposait aussi une palette rose vif et le pairing Playfair + Inter. **`impeccable` fait autorité sur le polish (§6) ; le client fait autorité sur la palette.** Retenu d'`ui-ux-pro-max` : le pairing Bodoni Moda + Jost, et sa checklist. Une recommandation de skill est un avis, pas un ordre — mais l'écarter se documente.

### 9.4 LEÇON NEUVE — un glyphe peut exister dans le cmap et n'avoir aucune encre

Le tiret cadratin `—` disparaissait au milieu d'une phrase en **Bodoni Moda**. `fontTools` confirmait pourtant U+2014 présent dans le cmap : la fausse piste « glyphe absent » était très crédible. Le rendu comparé a montré la vérité — **le glyphe est déclaré mais dessiné sans trait**.

Aucun contrôle ne l'attrape : pas d'erreur console, pas d'échec réseau, pas d'échec de contraste, pas de débordement. **Seul l'œil sur une capture l'a vu.** Correctif durable : une face `@font-face` ne couvrant que `U+2013-2014`, placée avant Bodoni dans la pile, qui délègue les tirets à la sans-serif. Un contrôle « glyphes sans encre » a été ajouté à `outils/qa.py` (canvas + `getImageData`, ratissage de tous les caractères réellement affichés).

### 9.5 LEÇON NEUVE — vérifier que les polices sont RÉELLEMENT peintes avant toute capture

Chromium n'atteignait pas `fonts.googleapis.com` dans l'environnement de recette (`ERR_CONNECTION_RESET`) alors que `curl` y arrivait — le proxy sert l'outil, pas le navigateur. **Les captures montraient des polices de repli tout en paraissant normales.** Juger la typographie dessus aurait été juger un rendu qui n'existe pas.

`document.fonts.check()` **ment** : il renvoie `true` dès qu'un repli existe. Seule `Array.from(document.fonts).filter(f => f.status === 'loaded')` fait foi. Contrôle ajouté à `qa.py`, et attente de `document.fonts.ready` dans `shoot.py`. Corrigé au fond en **auto-hébergeant les polices** — ce qui règle aussi la question CNIL et supprime une requête tierce.

### 9.6 LEÇON NEUVE — la portée de la mesure de contraste fait tout

Trois faux échecs successifs, tous dus à la portée et non au site :

1. **Modale ouverte** → le `::backdrop` assombrit la page derrière ; mesurer le texte du fond donnait 1,65:1 pour du texte que personne ne lit. Quand une modale est ouverte, ne mesurer **que** son contenu.
2. **Souris laissée sur le dernier élément cliqué** → c'est son état `:hover` qui était mesuré. `page.mouse.move(0,0)` avant toute mesure : l'état au repos est celui qui compte.
3. **Contenu hors de la zone visible d'une modale qui défile** → sa bbox pointe une zone où il n'est pas peint. Ne mesurer que le visible, puis refaire un passage après défilement.

Généralisation : **avant de corriger le site sur un échec de mesure, vérifier que la mesure vise la bonne couche.** Sinon on « corrige » un design sain pour satisfaire un instrument faux.

### 9.7 LEÇON NEUVE — chercher la donnée manquante, jamais la compléter de mémoire

Deux erreurs évitées uniquement par la vérification : **« Philos Jade » (Maison Alhambra) n'existe pas** — le nom était plausible et me venait spontanément ; et **« Ameerat Al Arab » est d'Asdaaf, pas de Paris Corner**. Une famille olfactive manquante (la chyprée) se cherche dans le catalogue réel — elle ne se fabrique pas en reclassant abusivement un parfum déjà présent.

---

## Note finale

Ce fichier documente une méthode convergée sur quatre projets réels, pas un résultat figé ni une structure aspirée. Si un futur projet contredit une règle ici avec une raison locale spécifique et vérifiée, cette raison locale gagne. Mais si tu t'apprêtes à répéter une des 15 erreurs de la §4, ou à supposer qu'une skill/bibliothèque existe sans l'avoir vue sur le disque, c'est que tu n'as pas encore vérifié quelque chose que tu aurais dû vérifier. Va le vérifier avant d'avancer.
