# assets/sources/ — images d'origine du client

Déposez ici les fichiers **originaux**, jamais des captures d'écran recompressées :
la qualité de la source plafonne celle de tous les recadrages qui en sortent.

| Fichier attendu | Usage |
|---|---|
| `flatlay-frais.jpg` | Flat-lay des flacons clairs (Yara, Kenzie, Bon Bon, Blend Luxe…) |
| `flatlay-ambre.jpg` | Flat-lay des flacons ambrés (Asad Bourbon, Liquid Brun, Proud of You…) |
| `boutique-interieur.jpg` | Intérieur de la boutique, comptoir JNT |
| `logo-jnt.svg` *(ou PNG détouré)* | Logo — verrouille aussi la valeur exacte du beige |

## Ensuite

```bash
python3 outils/decoupe.py --verifier   # contrôle sources et boîtes, n'écrit rien
python3 outils/decoupe.py              # produit assets/parfums/<slug>.jpg
```

Les coordonnées de découpe vivent dans `outils/decoupes.json` (créé à ce
moment-là). Le script est déterministe : relancé, il regénère exactement les
mêmes fichiers — la découpe reste donc auditable et refaisable.

Ce dossier contient les **originaux**, qui ne sont pas servis au visiteur.
Seuls les fichiers produits dans `assets/parfums/` le sont.
