# assets/sources/decors/ — décors de famille olfactive

Déposez ici les **6 images générées**, puis lancez :

```bash
python3 outils/decors.py
```

Le script vérifie le format réel, recadre au carré, produit `assets/decors/<famille>.jpg`
en 800×800, et **réécrit tout seul la table `window.DECORS` de `catalogue.js`** avec les
seules familles réellement présentes. Rien d'autre à modifier à la main.

## Noms de fichiers attendus

Exactement ces six, sans accent ni majuscule — ce sont les clés de famille déjà utilisées
dans `catalogue.js`. L'extension importe peu (`.png`, `.jpg`, `.jpeg`, `.webp`) : le
format est lu dans le fichier, jamais déduit du nom.

| Fichier | Famille | Réfs concernées |
|---|---|---|
| `ambree.png` | Ambrée / orientale | 9 |
| `boisee.png` | Boisée | 4 |
| `chypree.png` | Chyprée | 3 |
| `florale.png` | Florale | 4 |
| `fougere.png` | Fougère | 2 |
| `hesperidee.png` | Hespéridée | 2 |

## Contraintes

- **Minimum 800 × 800 px.** En dessous, le script refuse l'image plutôt que de l'agrandir :
  une vignette floue est pire qu'un emplacement en attente.
- **Carré (1:1)** de préférence. Un format différent sera recadré au carré centré — ce qui
  peut couper les bords de la composition.
- Une famille sans fichier garde simplement son emplacement « photo à venir ». Ce n'est pas
  un échec : le site reste cohérent avec 1, 3 ou 6 décors.

## Ce que ces images sont, et ne sont pas

Ce sont des **mises en scène des notes** — safran, vanille, oud, jasmin — sur pierre ou
marbre. Elles n'ont **aucun flacon**, et c'est délibéré : générer un flacon de marque
produirait une approximation (forme, étiquette, bouchon faux) publiée comme étant le stock
de la boutique, devant des gens qui se déplacent ensuite sur place.

Un décor est partagé par toute une famille. Deux orientaux ambrés ont le même univers —
c'est une direction artistique qui traite les familles comme des mondes, pas un raccourci.

Ce dossier contient les **originaux**, non servis au visiteur. Seuls les fichiers produits
dans `assets/decors/` le sont.
