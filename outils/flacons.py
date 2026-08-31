#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
flacons.py — pose le VRAI flacon du client devant le décor de sa famille.

    python3 outils/flacons.py

CE QUE FAIT CE SCRIPT, ET CE QU'IL NE FAIT PAS
----------------------------------------------
Il découpe un flacon dans l'un des deux flat-lays fournis par la boutique et le
compose devant le décor de sa famille olfactive, dans l'esprit des vignettes
PDS Shop : produit net au premier plan, décor en retrait et flou.

Il ne traite QUE les références réellement présentes ET lisibles dans les
flat-lays. C'est une contrainte de la matière première, pas un manque d'effort :
les deux photos contiennent surtout des flacons qui ne sont pas au catalogue
(Roses de Jacques, Bon Bon, Solara, Blend Luxe, Mystère, White...). Attribuer un
flacon non lisible à une référence publierait une image de produit FAUSSE —
pire qu'un emplacement provisoire assumé.

POURQUOI LE DÉCOR EST FORTEMENT FLOUTÉ
--------------------------------------
Les flat-lays sont pris à la verticale, à plat. Les décors sont des scènes de
table vues à 15° d'élévation. Coller un flacon vu de dessus sur une table vue de
côté donne un autocollant : les deux perspectives ne peuvent pas coexister. En
poussant le flou du décor, la table cesse d'être un plan lisible et devient une
ambiance colorée — le conflit de perspective disparaît, et le résultat reste
celui demandé : produit net devant, décor en retrait.

Le découpage est feutré (masque à bords doux) plutôt que détouré au pixel : sur
ces deux photos, les flacons blancs sur table blanche (Yara) et les verres
translucides (Kenzie) rendent tout détourage automatique par luminance
impossible. Un bord doux est honnête ; un détourage raté ne l'est pas.
"""

import io
import os
import re
import sys

from PIL import Image, ImageDraw, ImageFilter

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCES = os.path.join(RACINE, 'assets', 'sources')
DECORS = os.path.join(RACINE, 'assets', 'decors')
SORTIE = os.path.join(RACINE, 'assets', 'produits')
CATALOGUE = os.path.join(RACINE, 'catalogue.js')

COTE = 800
QUALITE = 84

VERT, ROUGE, JAUNE, GRIS, RAZ = '\033[32m', '\033[31m', '\033[33m', '\033[90m', '\033[0m'

# Boîtes relevées À LA MAIN sur une grille de coordonnées posée sur chaque
# flat-lay, après lecture de l'étiquette. Aucune n'est déduite d'un numéro de
# fichier ni d'une ressemblance de forme : seulement d'un nom lu.
FLACONS = {
    # 'angle' redresse le flacon : dans les flat-lays ils sont COUCHÉS en
    # diagonale. Sans redressement ils paraissent renversés sur le décor.
    'lattafa-yara': {
        'src': 'flatlay-frais.jpg', 'boite': (66, 30, 205, 335), 'angle': 6,
        'famille': 'florale', 'lu': 'YARA / Lattafa',
    },
    'volare-kenzie-summer-bottled': {
        'src': 'flatlay-frais.jpg', 'boite': (126, 668, 302, 980), 'angle': 3,
        'famille': 'florale', 'lu': 'KENZIE SUMMER BOTTLED / Volare',
    },
    # ÉCARTÉS APRÈS AVOIR REGARDÉ LE RENDU — ne pas les remettre sans
    # nouvelle photo :
    #   lattafa-asad-bourbon     : le cadre montre aussi Liquid Brun derrière
    #   french-avenue-liquid-brun: le cadre montre aussi le flacon strié voisin
    # Dans les deux cas le redressement (18° et 34°) laisse en plus des coins
    # vides. Publier un visuel où DEUX produits apparaissent sous le nom d'un
    # seul est une image de produit fausse — l'emplacement provisoire est
    # préférable. Ces deux flacons sont trop imbriqués dans le flat-lay pour
    # être isolés ; il faut une photo dédiée.
    'fragrance-world-proud-of-you-amber': {
        'src': 'flatlay-ambre.jpg', 'boite': (246, 792, 462, 1020), 'angle': 12,
        'famille': 'ambree', 'lu': 'PROUD OF YOU AMBER / Fragrance World',
    },
}


def fond(famille):
    """Le décor de la famille, poussé loin en arrière-plan."""
    p = os.path.join(DECORS, famille + '.jpg')
    im = Image.open(p).convert('RGB').resize((COTE, COTE), Image.LANCZOS)
    im = im.filter(ImageFilter.GaussianBlur(radius=13))
    # Assombrir légèrement : un fond trop clair mange le contour du flacon.
    return Image.blend(im, Image.new('RGB', im.size, (26, 22, 19)), 0.28)


def masque_doux(taille):
    """Rectangle à coins arrondis, bords fondus.

    Un ovale large rognait le haut des flacons et laissait entrer les voisins
    sur les côtés ; un rectangle arrondi épouse la silhouette d'un flacon et ne
    coupe plus le bouchon.
    """
    w, h = taille
    m = Image.new('L', (w, h), 0)
    d = ImageDraw.Draw(m)
    dx = int(w * 0.06)
    d.rounded_rectangle([dx, int(h * 0.02), w - dx, int(h * 0.98)],
                        radius=int(min(w, h) * 0.16), fill=255)
    return m.filter(ImageFilter.GaussianBlur(radius=max(6, int(min(w, h) * 0.045))))


def composer(slug, spec):
    im = Image.open(os.path.join(SOURCES, spec['src'])).convert('RGB')
    dec = fond(spec['famille'])

    crop = im.crop(spec['boite'])
    if spec.get('angle'):
        crop = crop.rotate(spec['angle'], resample=Image.BICUBIC, expand=True,
                           fillcolor=(240, 238, 235))
        # La rotation ajoute des coins vides : on rogne la marge qu'elle crée.
        r = 0.13
        w, h = crop.size
        crop = crop.crop((int(w * r), int(h * r), int(w * (1 - r)), int(h * (1 - r))))

    h_cible = int(COTE * 0.66)
    ratio = h_cible / crop.height
    crop = crop.resize((max(1, int(crop.width * ratio)), h_cible), Image.LANCZOS)
    # Le flacon fait ~150 px dans la source pour ~530 px à l'écran : sans
    # accentuation il ressort mou face au décor.
    crop = crop.filter(ImageFilter.UnsharpMask(radius=2.2, percent=115, threshold=3))

    m = masque_doux(crop.size)

    x = (COTE - crop.width) // 2
    y = int(COTE * 0.20)

    # Ombre portée : sans elle, le flacon flotte au lieu de reposer.
    ombre = Image.new('RGBA', (COTE, COTE), (0, 0, 0, 0))
    od = ImageDraw.Draw(ombre)
    od.ellipse([x + crop.width * 0.10, y + crop.height * 0.88,
                x + crop.width * 0.90, y + crop.height * 1.06],
               fill=(0, 0, 0, 130))
    ombre = ombre.filter(ImageFilter.GaussianBlur(radius=22))
    dec = Image.alpha_composite(dec.convert('RGBA'), ombre).convert('RGB')

    dec.paste(crop, (x, y), m)

    os.makedirs(SORTIE, exist_ok=True)
    out = os.path.join(SORTIE, slug + '.jpg')
    dec.save(out, 'JPEG', quality=QUALITE, optimize=True, progressive=True)
    return out, os.path.getsize(out) / 1024


def reecrire_table(faits):
    """Écrit window.PRODUITS avec les SEULES références réellement composées."""
    src = io.open(CATALOGUE, encoding='utf-8').read()
    motif = re.compile(r'window\.PRODUITS = \{[^}]*\};')
    if faits:
        lg = max(len(s) for s in faits)
        lignes = ',\n'.join(
            f"  {repr(s) + ':':<{lg + 4}} 'assets/produits/{s}.jpg'" for s in sorted(faits))
        bloc = 'window.PRODUITS = {\n' + lignes + '\n};'
    else:
        bloc = 'window.PRODUITS = {};'
    if not motif.search(src):
        # Première pose : juste après la table des décors.
        src = src.replace('window.DECORS = {', bloc + '\n\nwindow.DECORS = {', 1)
        io.open(CATALOGUE, 'w', encoding='utf-8').write(src)
        return 'table créée'
    neuf = motif.sub(lambda _: bloc, src, count=1)
    if neuf == src:
        return 'table déjà à jour'
    io.open(CATALOGUE, 'w', encoding='utf-8').write(neuf)
    return f'table réécrite ({len(faits)} référence(s))'


def main():
    faits = []
    for slug, spec in FLACONS.items():
        out, ko = composer(slug, spec)
        faits.append(slug)
        print(f"  {VERT}OK  {RAZ} {slug:36} {ko:5.0f} Ko   lu : « {spec['lu']} »")
    print(f'  {VERT}TABLE{RAZ} catalogue.js : {reecrire_table(faits)}')
    print(f'\n{len(faits)} flacons réels composés. Les {24 - len(faits)} autres références '
          'gardent leur décor et sont marquées « visuel provisoire ».')
    return 0


if __name__ == '__main__':
    sys.exit(main())
