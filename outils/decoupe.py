#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
decoupe.py — produit les photos produit à partir des flat-lays du client.

    python3 outils/decoupe.py --verifier   # contrôle sources et boîtes, n'écrit rien
    python3 outils/decoupe.py              # produit assets/parfums/<slug>.jpg

POURQUOI UN FICHIER DE BOÎTES, ET PAS UN RECADRAGE À LA MAIN
------------------------------------------------------------
Les coordonnées de découpe vivent dans `outils/decoupes.json`, versionné. Le
script est déterministe : relancé, il regénère exactement les mêmes fichiers.
On peut donc auditer une photo (« d'où vient ce cadrage ? »), la refaire après
avoir reçu une source de meilleure qualité, ou corriger une boîte de quelques
pixels — sans repartir de zéro et sans geste manuel irreproductible.

CE QUE LE TRAITEMENT FAIT, ET CE QU'IL NE FAIT PAS
---------------------------------------------------
Fait : recadrage, mise à l'échelle, léger vignettage pour détacher le flacon.
Ce sont des conventions de la parfumerie haut de gamme, pas la signature d'un
concurrent.

Ne fait PAS : ajouter un décor. Pas de marbre, pas de bokeh, pas d'accessoire
thématique fabriqué. Le fond reste celui de la photo d'origine du client. Une
mise en scène inventée serait une image mensongère de son rayon.
"""

import argparse
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFilter

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOITES = os.path.join(RACINE, 'outils', 'decoupes.json')
SORTIE = os.path.join(RACINE, 'assets', 'parfums')
COTE = 800          # carré : le ratio 1/1 est celui réservé par la grille
QUALITE = 82

VERT, ROUGE, JAUNE, GRIS, RAZ = '\033[32m', '\033[31m', '\033[33m', '\033[90m', '\033[0m'


def vignettage(im, force=0.22):
    """Assombrit doucement les bords pour détacher le flacon du fond.

    Volontairement discret : au-delà, l'image prend un air de filtre appliqué,
    ce qui est l'inverse de l'effet recherché.
    """
    l, h = im.size
    masque = Image.new('L', (l, h), 0)
    ImageDraw.Draw(masque).ellipse(
        (-l * 0.20, -h * 0.20, l * 1.20, h * 1.20), fill=255)
    masque = masque.filter(ImageFilter.GaussianBlur(radius=min(l, h) * 0.18))
    sombre = Image.new('RGB', (l, h), (0, 0, 0))
    return Image.composite(im, Image.blend(im, sombre, force), masque)


def recadrer(src, boite):
    """Recadre puis remplit un carré, sans jamais déformer le flacon."""
    x, y, w, h = boite
    zone = src.crop((x, y, x + w, y + h))
    cote = min(zone.size)
    gauche = (zone.width - cote) // 2
    haut = (zone.height - cote) // 2
    zone = zone.crop((gauche, haut, gauche + cote, haut + cote))
    return zone.resize((COTE, COTE), Image.LANCZOS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--verifier', action='store_true',
                    help='contrôle les sources et les boîtes sans rien écrire')
    a = ap.parse_args()

    if not os.path.isfile(BOITES):
        print(f'{JAUNE}Aucun fichier de boîtes : {BOITES}{RAZ}')
        print('Il se remplit une fois les flat-lays du client déposés dans '
              'assets/sources/. Format attendu :')
        print(json.dumps([{
            'slug': 'lattafa-yara',
            'source': 'assets/sources/flatlay-frais.jpg',
            'boite': [120, 60, 420, 520],
            'note': 'flacon blanc et or, calligraphie arabe, en haut à gauche'
        }], indent=2, ensure_ascii=False))
        return 0

    decoupes = json.load(open(BOITES, encoding='utf-8'))
    caches, erreurs, faits = {}, [], []

    for d in decoupes:
        chemin = os.path.join(RACINE, d['source'])
        if not os.path.isfile(chemin):
            erreurs.append(f"{d['slug']} : source absente ({d['source']})")
            continue
        if chemin not in caches:
            im = Image.open(chemin)
            # Format RÉEL, jamais l'extension : un .jpg peut être un PNG renommé.
            reel = (im.format or '?').upper()
            print(f'{GRIS}source {d["source"]} — {reel} {im.size[0]}×{im.size[1]}{RAZ}')
            caches[chemin] = im.convert('RGB')
        src = caches[chemin]

        x, y, w, h = d['boite']
        if x < 0 or y < 0 or x + w > src.width or y + h > src.height:
            erreurs.append(f"{d['slug']} : boîte hors de la source "
                           f"({x},{y},{w},{h}) vs {src.width}×{src.height}")
            continue
        if min(w, h) < 260:
            erreurs.append(f"{d['slug']} : boîte trop petite ({w}×{h}) — "
                           f"le flacon serait flou une fois agrandi, garder le placeholder")
            continue
        if a.verifier:
            faits.append(f"{d['slug']} : OK ({w}×{h})")
            continue

        os.makedirs(SORTIE, exist_ok=True)
        out = os.path.join(SORTIE, d['slug'] + '.jpg')
        vignettage(recadrer(src, d['boite'])).save(
            out, 'JPEG', quality=QUALITE, optimize=True, progressive=True)
        faits.append(f"{d['slug']} : {os.path.getsize(out) / 1024:.0f} Ko")

    for f in faits:
        print(f'  {VERT}OK  {RAZ} {f}')
    for e in erreurs:
        print(f'  {ROUGE}ÉCART{RAZ} {e}')
    print(f'\n{len(faits)} traitées, {len(erreurs)} écartées.')
    if erreurs:
        print('Les références écartées gardent leur placeholder — c\'est le '
              'comportement voulu, pas un échec.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
