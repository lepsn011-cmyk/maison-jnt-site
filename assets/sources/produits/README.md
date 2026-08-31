# assets/sources/produits/ — visuels produit (flacon dans son décor)

Déposez ici les images générées, puis lancez :

```bash
python3 outils/produits.py
```

Le script vérifie le format réel, recadre au carré, produit `assets/produits/<slug>.jpg`
en 800×800, et **réécrit tout seul `window.PRODUITS` dans `catalogue.js`** avec les seules
références réellement présentes. Rien d'autre à modifier à la main.

## Nommer les fichiers

Le nom est le **slug** de `catalogue.js`. Mais **le nom court suffit** : `khamrah.jpeg`
retrouve `lattafa-khamrah`. L'outil n'exige pas le slug complet — il s'adapte au nom
naturel, pas l'inverse.

Une seule règle : si le nom court désigne **plusieurs** références, l'outil refuse et le
dit, au lieu de deviner. Deviner publierait le mauvais produit sous le bon nom.
Exemple : `asad.jpeg` → `lattafa-asad` sans ambiguïté ; pour l'autre, écrire
`asad-bourbon.jpeg`.

L'extension n'a aucune importance (`.png`, `.jpg`, `.jpeg`, `.webp`) : le format est lu
dans le fichier, jamais déduit du nom.

## Contraintes

- **Minimum 800 × 800 px.** En dessous, le script refuse plutôt que d'agrandir : une
  vignette floue est pire qu'une carte en décor seul.
- **Carré (1:1)** de préférence. Un autre format sera recadré au carré centré.
- Une référence sans fichier garde simplement le décor de sa famille. Ce n'est pas un
  échec : le site reste cohérent avec 3, 10 ou 24 visuels produit.

## Comment ces images sont faites

Deux images de référence jointes au modèle : **la photo du vrai flacon**
(`assets/sources/refs/`) et **le décor de sa famille** (`assets/sources/decors/`). Le
flacon est REGÉNÉRÉ debout dans la scène, jamais découpé et collé.

Ne pas revenir au découpage depuis un flat-lay : les flat-lays sont pris à la verticale,
les décors sont des scènes de table vues à 15°. Un objet vu de dessus posé sur une table
vue de côté reste un autocollant, quel que soit le flou.
