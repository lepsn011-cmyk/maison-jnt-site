#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
produits.py — intègre les visuels produit générés hors de cet environnement.

    python3 outils/produits.py --verifier   # contrôle, n'écrit rien
    python3 outils/produits.py              # produit assets/produits/<slug>.jpg

POURQUOI CE SCRIPT EXISTE
-------------------------
Un visuel produit = le VRAI flacon, régénéré debout dans le décor de sa famille, à
partir de DEUX références jointes au modèle : la photo du flacon (assets/sources/refs/)
et le décor de sa famille (assets/sources/decors/). Le packaging vient donc d'une photo
et non de la mémoire d'un modèle.

La génération se fait dans le navigateur du client : cet environnement a les crédits à
zéro ET la politique d'egress refuse au CONNECT (403) tous les hôtes de génération
testés — pollinations, together, fal, deepinfra, huggingface. Vérifié, pas supposé.

Ce qui a été ABANDONNÉ, et ne doit pas revenir : découper le flacon du flat-lay pour le
coller sur le décor. Flat-lay pris à la verticale contre décor de table vu à 15° : un
objet vu de dessus posé sur une table vue de côté reste un autocollant, quel que soit
le flou. Le flacon doit être REGÉNÉRÉ debout, pas déplacé.

LE CONTRAT
----------
    assets/sources/produits/<slug>.png|.jpg   <- déposé par le client (brut)
    assets/produits/<slug>.jpg                <- produit ici (servi au visiteur)

Le <slug> est celui de catalogue.js. Toute clé inconnue est signalée plutôt qu'ignorée :
un fichier mal nommé ne doit pas disparaître en silence.

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
SOURCES = os.path.join(RACINE, 'assets', 'sources', 'produits')
SORTIE = os.path.join(RACINE, 'assets', 'produits')
COTE = 800          # le carré réservé par la grille du catalogue
QUALITE = 82
EXTENSIONS = ('.png', '.jpg', '.jpeg', '.webp')

CATALOGUE = os.path.join(RACINE, 'catalogue.js')

VERT, ROUGE, JAUNE, GRIS, RAZ = '\033[32m', '\033[31m', '\033[33m', '\033[90m', '\033[0m'


def slugs_connus():
    """Les slugs réellement présents dans catalogue.js, lus par node.

    On n'invente pas la liste et on ne la duplique pas ici : elle est dérivée de
    la donnée, donc elle suit automatiquement toute référence ajoutée.
    """
    import json, subprocess
    out = subprocess.run(
        ['node', '-e',
         "global.window={};require('" + CATALOGUE.replace("\\", "/") + "');"
         "console.log(JSON.stringify(window.CATALOGUE.map(p=>p.slug)))"],
        capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def reecrire_table(livrees):
    """Réécrit `window.PRODUITS` dans catalogue.js avec les SEULES entrées livrées.

    Pourquoi la table est générée et non tenue à la main : déclarer le chemin
    d'un décor qui n'existe pas encore produit une requête 404 par carte en
    production. Mesuré : 5 requêtes échouées dans la console pour 5 familles
    en attente. La table doit donc rester vraie par construction — c'est
    l'outil qui la tient, jamais une saisie manuelle.
    """
    src = io.open(CATALOGUE, encoding='utf-8').read()
    motif = re.compile(r'window\.PRODUITS = \{[^}]*\};')
    if not motif.search(src):
        return False, 'bloc window.PRODUITS introuvable dans catalogue.js'
    if livrees:
        largeur = max(len(f) for f in livrees) + 3
        lignes = ',\n'.join(
            f"  {repr(f) + ':':<{largeur}} 'assets/produits/{f}.jpg'" for f in sorted(livrees))
        bloc = 'window.PRODUITS = {\n' + lignes + '\n};'
    else:
        bloc = 'window.PRODUITS = {};'
    neuf = motif.sub(lambda _: bloc, src, count=1)
    if neuf == src:
        return True, 'table déjà à jour'
    io.open(CATALOGUE, 'w', encoding='utf-8').write(neuf)
    return True, f'table réécrite ({len(livrees)} référence(s))'


def base(nom):
    return os.path.splitext(nom)[0].lower()


def apparier(slugs):
    """Associe chaque fichier déposé à un slug du catalogue.

    Les slugs sont longs (`lattafa-khamrah`) mais un humain nomme spontanément
    son fichier `khamrah.png`. Exiger le nom long ferait rejeter des fichiers
    parfaitement valides — l'outil s'adapte au nom naturel, pas l'inverse.

    Trois cas, dans cet ordre :
      1. le nom EST un slug           -> retenu
      2. le nom est un suffixe d'un SEUL slug -> retenu (khamrah -> lattafa-khamrah)
      3. le nom est un suffixe de PLUSIEURS slugs -> refusé et signalé
         (« asad » vise lattafa-asad et lattafa-asad-bourbon : deviner
         publierait le mauvais produit sous le bon nom)
    """
    fichiers = [f for f in sorted(os.listdir(SOURCES))
                if f.lower().endswith(EXTENSIONS)]
    par_slug, ecarts = {}, []
    for f in fichiers:
        b = base(f)
        if b in slugs:
            cible = b
        else:
            cands = [s_ for s_ in slugs if s_.endswith('-' + b)]
            if len(cands) == 1:
                cible = cands[0]
            elif len(cands) > 1:
                ecarts.append(f'{f} : « {b} » correspond à {len(cands)} références '
                              f'({", ".join(cands)}) — renommer avec le slug complet')
                continue
            else:
                ecarts.append(f'{f} : aucun slug de ce nom dans catalogue.js — '
                              f'vérifier le nom')
                continue
        if cible in par_slug:
            ecarts.append(f'{f} : {cible} déjà fourni par '
                          f'{os.path.basename(par_slug[cible])} — un seul fichier par référence')
            continue
        par_slug[cible] = os.path.join(SOURCES, f)
    return par_slug, ecarts


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
        # Sortir ici SANS toucher à la table laissait `window.PRODUITS` pointer des
        # fichiers disparus : mesuré, 5 requêtes 404 en console alors que le QA en
        # exige zéro. La table doit rester vraie même quand il n'y a plus rien.
        print(f'{JAUNE}Dossier absent : {SOURCES}{RAZ}')
        print('Créez-le et déposez-y les visuels générés, nommés <slug>.png.')
        if not a.verifier:
            ok, detail = reecrire_table([])
            print(f"  {VERT if ok else ROUGE}{'TABLE' if ok else 'ERREUR'}{RAZ} "
                  f'catalogue.js : {detail}')
        return 0

    slugs = slugs_connus()
    faits, manquants = [], []
    # Un fichier mal nommé ne doit PAS disparaître en silence : c'est le cas
    # d'erreur le plus probable côté client.
    sources, erreurs = apparier(slugs)

    for slug in slugs:
        src = sources.get(slug)
        if not src:
            manquants.append(slug)
            continue
        try:
            im = Image.open(src)
            reel = (im.format or '?').upper()
            w, h = im.size
            im = im.convert('RGB')
        except Exception as e:
            erreurs.append(f'{slug} : illisible ({e})')
            continue

        if min(w, h) < COTE:
            erreurs.append(f'{slug} : source {w}×{h}, plus petite que {COTE}×{COTE} — '
                           f'régénérer en résolution supérieure plutôt qu\'agrandir')
            continue

        print(f'{GRIS}source {os.path.basename(src)} — {reel} {w}×{h}{RAZ}')
        if a.verifier:
            faits.append(f'{slug} : OK ({reel} {w}×{h})')
            continue

        os.makedirs(SORTIE, exist_ok=True)
        out = os.path.join(SORTIE, slug + '.jpg')
        carre(im).save(out, 'JPEG', quality=QUALITE, optimize=True, progressive=True)
        md5 = hashlib.md5(open(out, 'rb').read()).hexdigest()[:8]
        faits.append(f'{slug} : {os.path.getsize(out) / 1024:.0f} Ko  md5 {md5}')

    for f_ in faits:
        print(f'  {VERT}OK  {RAZ} {f_}')
    for e in erreurs:
        print(f'  {ROUGE}ÉCART{RAZ} {e}')

    livrees = [s_ for s_ in slugs
               if os.path.isfile(os.path.join(SORTIE, s_ + '.jpg'))]
    if not a.verifier:
        ok, detail = reecrire_table(livrees)
        print(f"  {VERT if ok else ROUGE}{'TABLE' if ok else 'ERREUR'}{RAZ} "
              f'catalogue.js : {detail}')

    print(f'\n{len(faits)} visuels produit intégrés, {len(erreurs)} écartés, '
          f'{len(manquants)} références encore en décor seul.')
    return 1 if erreurs else 0


if __name__ == '__main__':
    sys.exit(main())
