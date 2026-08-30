#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
decors.py — intègre les décors de famille olfactive générés hors de cet environnement.

    python3 outils/decors.py --verifier   # contrôle, n'écrit rien
    python3 outils/decors.py              # produit assets/decors/<famille>.jpg

POURQUOI CE SCRIPT EXISTE
-------------------------
Les décors sont générés par le client depuis son navigateur (Higgsfield), parce que
cet environnement a deux verrous : crédits à zéro, et CDN de résultat refusé par la
politique d'egress (403). Il dépose les fichiers bruts, ce script les normalise.

LE CONTRAT
----------
    assets/sources/decors/<famille>.png|.jpg   <- déposé par le client (brut)
    assets/decors/<famille>.jpg                <- produit ici (servi au visiteur)

Six familles, exactement les clés utilisées dans catalogue.js :
    ambree  boisee  chypree  florale  fougere  hesperidee

L'extension déposée n'a aucune importance : on lit le FORMAT RÉEL par PIL. Un .jpg
qui est un PNG renommé est déjà arrivé sur un projet précédent — l'extension ne
prouve rien.

DÉTERMINISME
------------
Relancé sur les mêmes sources, ce script réécrit des fichiers identiques à l'octet.
C'est ce qui rend l'intégration auditable et refaisable si une source est remplacée.
"""

import argparse
import hashlib
import io
import os
import re
import sys

from PIL import Image

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCES = os.path.join(RACINE, 'assets', 'sources', 'decors')
SORTIE = os.path.join(RACINE, 'assets', 'decors')
FAMILLES = ['ambree', 'boisee', 'chypree', 'florale', 'fougere', 'hesperidee']
COTE = 800          # le carré réservé par la grille du catalogue
QUALITE = 82
EXTENSIONS = ('.png', '.jpg', '.jpeg', '.webp')

CATALOGUE = os.path.join(RACINE, 'catalogue.js')

VERT, ROUGE, JAUNE, GRIS, RAZ = '\033[32m', '\033[31m', '\033[33m', '\033[90m', '\033[0m'


def reecrire_table(livrees):
    """Réécrit `window.DECORS` dans catalogue.js avec les SEULES familles livrées.

    Pourquoi la table est générée et non tenue à la main : déclarer le chemin
    d'un décor qui n'existe pas encore produit une requête 404 par carte en
    production. Mesuré : 5 requêtes échouées dans la console pour 5 familles
    en attente. La table doit donc rester vraie par construction — c'est
    l'outil qui la tient, jamais une saisie manuelle.
    """
    src = io.open(CATALOGUE, encoding='utf-8').read()
    motif = re.compile(r'window\.DECORS = \{[^}]*\};')
    if not motif.search(src):
        return False, 'bloc window.DECORS introuvable dans catalogue.js'
    if livrees:
        largeur = max(len(f) for f in livrees)
        lignes = ',\n'.join(
            f"  {f + ':':<{largeur + 1}} 'assets/decors/{f}.jpg'" for f in sorted(livrees))
        bloc = 'window.DECORS = {\n' + lignes + '\n};'
    else:
        bloc = 'window.DECORS = {};'
    neuf = motif.sub(lambda _: bloc, src, count=1)
    if neuf == src:
        return True, 'table déjà à jour'
    io.open(CATALOGUE, 'w', encoding='utf-8').write(neuf)
    return True, f'table réécrite ({len(livrees)} famille(s))'


def trouver(famille):
    """Retourne le premier fichier source d'une famille, quelle que soit l'extension."""
    for ext in EXTENSIONS:
        p = os.path.join(SOURCES, famille + ext)
        if os.path.isfile(p):
            return p
    return None


def carre(im):
    """Recadre au carré centré, sans jamais déformer la scène."""
    cote = min(im.size)
    g = (im.width - cote) // 2
    h = (im.height - cote) // 2
    return im.crop((g, h, g + cote, h + cote)).resize((COTE, COTE), Image.LANCZOS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--verifier', action='store_true',
                    help='contrôle les sources sans rien écrire')
    a = ap.parse_args()

    if not os.path.isdir(SOURCES):
        print(f'{JAUNE}Dossier absent : {SOURCES}{RAZ}')
        print('Créez-le et déposez-y les décors générés, nommés :')
        for f in FAMILLES:
            print(f'  {f}.png')
        return 0

    faits, manquants, erreurs = [], [], []

    for famille in FAMILLES:
        src = trouver(famille)
        if not src:
            manquants.append(famille)
            continue
        try:
            im = Image.open(src)
            reel = (im.format or '?').upper()
            w, h = im.size
            im = im.convert('RGB')
        except Exception as e:
            erreurs.append(f'{famille} : illisible ({e})')
            continue

        # Une source plus petite que la sortie serait agrandie : on refuse plutôt
        # que de livrer du flou, comme pour les découpes de flacons.
        if min(w, h) < COTE:
            erreurs.append(f'{famille} : source {w}×{h}, plus petite que {COTE}×{COTE} — '
                           f'régénérer en résolution supérieure plutôt qu\'agrandir')
            continue

        print(f'{GRIS}source {os.path.basename(src)} — {reel} {w}×{h}{RAZ}')
        if a.verifier:
            faits.append(f'{famille} : OK ({reel} {w}×{h})')
            continue

        os.makedirs(SORTIE, exist_ok=True)
        out = os.path.join(SORTIE, famille + '.jpg')
        carre(im).save(out, 'JPEG', quality=QUALITE, optimize=True, progressive=True)
        md5 = hashlib.md5(open(out, 'rb').read()).hexdigest()[:8]
        faits.append(f'{famille} : {os.path.getsize(out) / 1024:.0f} Ko  md5 {md5}')

    for f in faits:
        print(f'  {VERT}OK  {RAZ} {f}')
    for e in erreurs:
        print(f'  {ROUGE}ÉCART{RAZ} {e}')
    for m in manquants:
        print(f'  {JAUNE}ATTENTE{RAZ} {m} : aucun fichier dans assets/sources/decors/')

    # La table ne liste QUE ce qui existe réellement sur le disque.
    livrees = [f for f in FAMILLES
               if os.path.isfile(os.path.join(SORTIE, f + '.jpg'))]
    if not a.verifier:
        ok, detail = reecrire_table(livrees)
        print(f"  {VERT if ok else ROUGE}{'TABLE' if ok else 'ERREUR'}{RAZ} catalogue.js : {detail}")

    print(f'\n{len(faits)} intégrés, {len(erreurs)} écartés, {len(manquants)} en attente.')
    if manquants:
        print('Les familles en attente gardent l\'emplacement « photo à venir » — '
              'c\'est le comportement voulu, pas un échec.')
    return 1 if erreurs else 0


if __name__ == '__main__':
    sys.exit(main())
