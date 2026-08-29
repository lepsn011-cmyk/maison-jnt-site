# Maison JNT — site vitrine

Boutique de parfums indépendante et multi-marques. Site vitrine statique :
**aucune vente en ligne**, aucun panier, aucun back-office. L'objectif est de
faire venir en boutique.

## Ouvrir le site

Double-cliquez sur `index.html`. Rien à installer, rien à compiler — la donnée
est chargée par `<script src>` et non par `fetch()`, précisément pour que
l'ouverture directe depuis le disque fonctionne.

## Modifier le catalogue

**Tout se passe dans `catalogue.js`.** `index.html` ne contient aucun nom de
parfum en dur : ajouter, retirer ou modifier une référence dans ce seul fichier
suffit, sans toucher au code.

Une entrée ressemble à ceci :

```js
{
  slug: 'lattafa-khamrah',        // identifiant unique, sans accent ni espace
  nom: 'Khamrah',
  marque: 'Lattafa',
  annee: 2022,
  genre: 'mixte',                 // homme | femme | mixte
  concentration: 'EDP',           // EDT | EDP | Extrait
  famille: 'ambree',              // florale|boisee|ambree|hesperidee|fougere|chypree
  nouveaute: false,
  editionLimitee: false,
  prix: null,                     // null → « Prix en boutique » ; 89 → « 89 € »
  notes: { tete: [...], coeur: [...], fond: [...] },
  description: '…',
  source: 'https://…'             // d'où vient la pyramide (traçabilité)
}
```

Points à connaître :

- **Les filtres se construisent tout seuls** à partir de la donnée. Ajoutez une
  marque : sa puce apparaît. Passez une référence en `editionLimitee: true` : la
  puce « Édition limitée » apparaît, alors qu'elle est absente aujourd'hui
  puisque aucune référence ne la porte.
- **Les prix sont optionnels par conception.** `prix: null` affiche « Prix en
  boutique » ; un nombre affiche le montant formaté. Il n'y a jamais de
  « 0 € » ni de case vide.
- La section « La maison du mois » se pilote par l'objet `MAISON_DU_MOIS`, en bas
  du même fichier. Un `slug` qui n'existe plus est simplement ignoré.

## Renseigner la boutique

Objet `BOUTIQUE`, en bas de `catalogue.js`. Les champs à `null` s'affichent
« à confirmer » sur le site — ils n'ont pas été inventés. Renseignez la valeur,
elle apparaît immédiatement :

```js
telephone: '01 23 45 67 89',
horaires: [{ jours: 'Lundi – Samedi', heures: '10h – 19h30' }],
```

Restent à fournir : **adresse, horaires, téléphone, pseudo Instagram** (la bio
Instagram transmise était tronquée sur la capture), plus le **fichier logo** et
la **photo d'intérieur** — voir `assets/README.md`.

## Vérifier avant de mettre en ligne

```bash
pip install playwright pillow      # une seule fois
python3 outils/qa.py               # contrôle complet, chiffré
python3 outils/shoot.py --out /tmp/vue.png --width 375
```

`outils/qa.py` mesure — il n'estime pas : contraste composite au pixel,
débordement horizontal, cibles tactiles, console, mouvement réduit, glyphes sans
encre, et l'absence des termes e-commerce écartés par le client. Sortie `OK` /
`FAIL` avec la valeur pour chaque contrôle.

## Mise en ligne

Site statique sans étape de compilation : déposez le dossier sur Netlify (ou
équivalent) avec `index.html` à la racine et `.` comme dossier de publication.

Attention à un malentendu fréquent : **rendre le dépôt GitHub privé ne rend pas
le site en ligne privé.** Ce sont deux choses distinctes.

## Documents du projet

| Fichier | Contenu |
|---|---|
| `PRODUCT.md` | Registre, utilisateurs, personnalité de marque, anti-références |
| `DESIGN.md` | Palette, typographie, densité, budget d'animation, interdits |
| `CLAUDE.md` | Méthode d'agence, dont §9 : les écarts propres à ce projet |
