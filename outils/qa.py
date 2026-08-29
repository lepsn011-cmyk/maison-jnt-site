#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
qa.py — contrôle qualité mesuré du site Maison JNT.

Applique les critères binaires de CLAUDE.md §5. Chaque ligne est MESURÉE,
jamais estimée à l'œil. Sortie OK/FAIL par zone, avec la valeur chiffrée.

    python3 outils/qa.py            # tout
    python3 outils/qa.py --rapide   # sans la mesure de contraste (la plus lente)

Deux pièges d'environnement déjà traités ici, à ne pas redécouvrir :

  1. playwright 1.62 réclame un build Chromium que cette image ne fournit pas
     (`chromium_headless_shell-1234` vs `-1194` présent), et `playwright
     install` est interdit. D'où EXE ci-dessous : on pointe le binaire réel.

  2. Le contraste est mesuré sur le COMPOSITE RÉEL, jamais token contre token :
       - bbox collée aux glyphes via Range.getClientRects() — getBoundingClientRect
         sur un bloc centré renvoie la boîte pleine largeur et pollue la mesure
         (CLAUDE.md §4.8) ;
       - couleur résolue par aller-retour <canvas>, car getComputedStyle().color
         peut renvoyer oklch(...) sur Chromium récent et casser tout parsing
         rgb() (CLAUDE.md §4.9).
"""

import argparse
import functools
import io
import json
import os
import re
import sys
import threading
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

from playwright.sync_api import sync_playwright
from PIL import Image

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXE = '/opt/pw-browsers/chromium'
LARGEURS = [375, 768, 1440]

# Termes que le client a explicitement refusés (registre e-commerce).
# Mesurés sur le TEXTE RENDU (innerText), pas sur la source : c'est la couche
# qui compte (CLAUDE.md §8.1). Un mot dans un commentaire CSS n'est pas affiché.
TERMES_BANNIS = [
    r'ajouter au panier', r'\bpanier\b', r'\bcommander\b', r'\bcheckout\b',
    r'-\s?10\s?%', r'\bpromo\b', r'\bsoldes?\b', r'\bréductions?\b', r'\bremise\b',
    r'livraison gratuite', r'paiement s[ée]curis[ée]', r'satisfait ou rembours[ée]',
    r'newsletter', r'prix barr[ée]',
]

ROUGE, VERT, JAUNE, GRIS, RAZ = '\033[31m', '\033[32m', '\033[33m', '\033[90m', '\033[0m'
resultats = []


def note(zone, ok, detail, tolere=False):
    resultats.append((zone, ok, detail, tolere))
    if ok:
        etat = f'{VERT}OK  {RAZ}'
    elif tolere:
        etat = f'{JAUNE}TOL {RAZ}'
    else:
        etat = f'{ROUGE}FAIL{RAZ}'
    print(f'  {etat} {zone:<44} {detail}')


# --------------------------------------------------------------------------
# Serveur éphémère (pattern CLAUDE.md §7)
# --------------------------------------------------------------------------

def demarrer_serveur():
    h = functools.partial(SimpleHTTPRequestHandler, directory=RACINE)
    h.log_message = lambda *a, **k: None
    srv = ThreadingHTTPServer(('127.0.0.1', 0), h)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, srv.server_address[1]


# --------------------------------------------------------------------------
# Contraste
# --------------------------------------------------------------------------

JS_CIBLES = r"""
() => {
  // Résout n'importe quelle notation CSS (oklch inclus) en RGB réel, par
  // aller-retour canvas. Jamais de regex sur la chaîne CSS.
  const cv = document.createElement('canvas');
  cv.width = cv.height = 1;
  const cx = cv.getContext('2d', { willReadFrequently: true });
  const enRGB = (css) => {
    cx.clearRect(0, 0, 1, 1);
    cx.fillStyle = '#000';
    cx.fillStyle = css;
    cx.fillRect(0, 0, 1, 1);
    const d = cx.getImageData(0, 0, 1, 1).data;
    return [d[0], d[1], d[2]];
  };

  // Portée : quand une modale est ouverte, on ne mesure QUE son contenu.
  // Le reste de la page est derrière un ::backdrop à 55 % : ce texte est
  // assombri, inerte, et personne ne le lit. Le mesurer ferait échouer des
  // zones parfaitement lisibles à l'état où elles comptent vraiment.
  const modale = document.querySelector('dialog[open]');
  const racine = modale || document.body;

  const out = [];
  racine.querySelectorAll('*').forEach((el) => {
    if (el.closest('dialog:not([open])')) return;
    // Uniquement les éléments portant DIRECTEMENT du texte.
    let propre = '';
    el.childNodes.forEach((n) => { if (n.nodeType === 3) propre += n.textContent; });
    if (!propre.trim()) return;

    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none' || parseFloat(cs.opacity) < 0.1) return;

    // bbox COLLÉE AUX GLYPHES : getBoundingClientRect renverrait la boîte
    // pleine largeur d'un bloc centré (CLAUDE.md §4.8).
    let r = null;
    try {
      const rg = document.createRange();
      rg.selectNodeContents(el);
      const rects = Array.from(rg.getClientRects()).filter((x) => x.width > 1 && x.height > 1);
      if (rects.length) {
        const l = Math.min(...rects.map((x) => x.left));
        const t = Math.min(...rects.map((x) => x.top));
        const rt = Math.max(...rects.map((x) => x.right));
        const b = Math.max(...rects.map((x) => x.bottom));
        r = { left: l, top: t, width: rt - l, height: b - t };
      }
    } catch (e) { /* ignoré : on retombe sur null */ }
    if (!r || r.width < 2 || r.height < 2) return;

    // Dans une modale qui défile, un élément hors de la zone visible n'est pas
    // peint là où sa bbox l'annonce : on échantillonnerait le backdrop au lieu
    // de son vrai fond. On ne mesure donc que ce qui est RÉELLEMENT visible ;
    // l'appelant refait un passage après défilement pour couvrir le reste.
    if (modale) {
      const m = modale.getBoundingClientRect();
      if (r.top < m.top - 1 || r.top + r.height > m.bottom + 1) return;
    }

    const px = parseFloat(cs.fontSize);
    const poids = parseInt(cs.fontWeight, 10) || 400;
    const grand = px >= 24 || (px >= 18.66 && poids >= 700);

    out.push({
      classe: (el.className && typeof el.className === 'string')
        ? el.className.split(/\s+/)[0] : el.tagName.toLowerCase(),
      tag: el.tagName.toLowerCase(),
      texte: propre.trim().slice(0, 42),
      couleur: enRGB(cs.color),
      px: px, grand: grand,
      x: r.left + window.scrollX, y: r.top + window.scrollY,
      w: r.width, h: r.height,
    });
  });
  return out;
}
"""

# Rend TOUT le texte transparent : la capture donne alors le fond réel
# derrière les glyphes, composite compris (photo, dégradé, superposition).
CSS_TRANSPARENT = """
*, *::before, *::after {
  color: transparent !important;
  text-shadow: none !important;
  text-decoration-color: transparent !important;
  -webkit-text-fill-color: transparent !important;
  caret-color: transparent !important;
}
"""


def luminance(c):
    def canal(v):
        v /= 255.0
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * canal(c[0]) + 0.7152 * canal(c[1]) + 0.0722 * canal(c[2])


def ratio(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def mesurer_contraste(page, etiquette):
    # On écarte la souris AVANT de mesurer. Sinon le dernier élément cliqué
    # reste en :hover et c'est son état survolé qui est mesuré — or l'état
    # survolé ne dit rien de la lisibilité au repos, qui est celle qui compte
    # (CLAUDE.md §8.1 : « la couche que tu MESURES doit être celle qui compte »).
    page.mouse.move(0, 0)
    page.wait_for_timeout(180)
    cibles = page.evaluate(JS_CIBLES)
    if not cibles:
        note(f'contraste [{etiquette}]', False, 'aucune cible trouvée')
        return

    marqueur = page.add_style_tag(content=CSS_TRANSPARENT)
    page.wait_for_timeout(120)
    brut = page.screenshot(full_page=True)
    page.evaluate('(n) => n.remove()', marqueur)

    img = Image.open(io.BytesIO(brut)).convert('RGB')
    W, H = img.size

    pires = {}
    for c in cibles:
        x0, y0 = max(0, int(c['x'])), max(0, int(c['y']))
        x1, y1 = min(W, int(c['x'] + c['w'])), min(H, int(c['y'] + c['h']))
        if x1 - x0 < 2 or y1 - y0 < 2:
            continue
        zone = img.crop((x0, y0, x1, y1))
        pixels = list(zone.convert("RGB").getdata()) if False else list(zone.getdata())
        if not pixels:
            continue

        rs = sorted(ratio(c['couleur'], p) for p in pixels)
        # 5e percentile plutôt que le minimum absolu : un pixel isolé de bordure
        # ou d'anticrénelage ne doit pas décider du verdict.
        p05 = rs[max(0, int(len(rs) * 0.05))]
        seuil = 3.0 if c['grand'] else 4.5
        cle = c['classe'] or c['tag']
        if cle not in pires or p05 < pires[cle][0]:
            pires[cle] = (p05, seuil, c['texte'], c['px'])

    echecs = [(k, v) for k, v in pires.items() if v[0] < v[1]]
    for k, v in sorted(pires.items(), key=lambda kv: kv[1][0])[:4]:
        print(f'{GRIS}       · {k:<26} {v[0]:5.2f}:1  (seuil {v[1]}, {v[3]:.0f}px) "{v[2]}"{RAZ}')

    if echecs:
        pire = min(echecs, key=lambda kv: kv[1][0])
        note(f'contraste [{etiquette}]', False,
             f'{len(echecs)} zone(s) sous le seuil — pire : {pire[0]} à {pire[1][0]:.2f}:1')
    else:
        mini = min(v[0] for v in pires.values())
        note(f'contraste [{etiquette}]', True,
             f'{len(pires)} zones mesurées, minimum {mini:.2f}:1')


# --------------------------------------------------------------------------
# Glyphes sans encre
# --------------------------------------------------------------------------
# Une fonte peut DÉCLARER un codepoint dans son cmap et n'en dessiner aucun
# trait : le caractère disparaît alors au milieu d'une phrase, sans erreur
# console, sans échec réseau, sans échec de contraste. C'est exactement ce qui
# est arrivé au tiret cadratin en Bodoni Moda — repéré à l'œil sur une capture,
# et par rien d'autre. D'où ce contrôle.
JS_ENCRE = r"""
() => {
  const cv = document.createElement('canvas');
  cv.width = 80; cv.height = 80;
  const cx = cv.getContext('2d', { willReadFrequently: true });

  const aDeLEncre = (ch, police) => {
    cx.clearRect(0, 0, 80, 80);
    cx.fillStyle = '#000';
    cx.font = '48px ' + police;
    if (cx.measureText(ch).width === 0) return true;  // sans chasse : pas un défaut
    cx.fillText(ch, 8, 58);
    const d = cx.getImageData(0, 0, 80, 80).data;
    for (let i = 3; i < d.length; i += 4) if (d[i] > 8) return true;
    return false;
  };

  const vus = new Set(), muets = [];
  document.querySelectorAll('body *').forEach((el) => {
    if (el.closest('dialog:not([open])')) return;
    let propre = '';
    el.childNodes.forEach((n) => { if (n.nodeType === 3) propre += n.textContent; });
    if (!propre.trim()) return;
    const police = getComputedStyle(el).fontFamily;
    for (const ch of propre) {
      if (/\s/.test(ch)) continue;
      const cle = ch + '|' + police;
      if (vus.has(cle)) continue;
      vus.add(cle);
      if (!aDeLEncre(ch, police)) {
        muets.push(ch + ' (U+' + ch.codePointAt(0).toString(16).toUpperCase().padStart(4, '0')
                   + ') dans ' + police.split(',')[0]);
      }
    }
  });
  return muets;
}
"""


# --------------------------------------------------------------------------
# Passe principale
# --------------------------------------------------------------------------

def auditer(rapide=False):
    srv, port = demarrer_serveur()
    base = f'http://127.0.0.1:{port}/index.html'
    print(f'{GRIS}Serveur éphémère sur {base}{RAZ}\n')

    with sync_playwright() as pw:
        nav = pw.chromium.launch(headless=True, executable_path=EXE)

        for largeur in LARGEURS:
            print(f'{GRIS}── {largeur}px {"─" * 52}{RAZ}')
            ctx = nav.new_context(viewport={'width': largeur, 'height': 900},
                                  device_scale_factor=1, locale='fr-FR')
            page = ctx.new_page()
            erreurs, avertissements, echecs_reseau = [], [], []
            page.on('console', lambda m: (erreurs if m.type == 'error' else
                                          avertissements if m.type == 'warning' else []).append(m.text))
            page.on('pageerror', lambda e: erreurs.append(str(e)))
            page.on('requestfailed', lambda r: echecs_reseau.append(
                f'{r.url[:70]} ({(r.failure or "?")})'))

            page.goto(base, wait_until='networkidle')
            page.wait_for_timeout(400)

            # -- la donnée est-elle bien arrivée jusqu'au DOM ?
            n = page.eval_on_selector_all('.entree', 'e => e.length')
            attendu = page.evaluate('() => (window.CATALOGUE || []).length')
            note(f'catalogue rendu [{largeur}]', n == attendu and n > 0,
                 f'{n} entrées affichées / {attendu} dans la donnée')

            # -- Les polices sont-elles RÉELLEMENT peintes ?
            # document.fonts.check() ment : il répond true dès qu'un repli
            # existe. Seule la liste document.fonts, alimentée par un @font-face
            # effectivement chargé, fait foi. Sans cette garde, toute capture
            # montrerait des polices de repli en laissant croire au vrai rendu.
            polices = page.evaluate(
                '() => Array.from(document.fonts)'
                '.filter(f => f.status === "loaded").map(f => f.family)')
            attendues = {'Bodoni Moda', 'Jost', 'Italianno'}
            manquantes = attendues - set(polices)
            note(f'polices réellement chargées [{largeur}]', not manquantes,
                 f'{sorted(set(polices))}' if not manquantes else f'MANQUE {sorted(manquantes)}')

            muets = page.evaluate(JS_ENCRE)
            note(f'glyphes sans encre [{largeur}]', not muets,
                 'aucun caractère muet' if not muets else f'MUETS : {muets[:4]}')

            # -- overflow horizontal : mesuré, pas regardé
            of = page.evaluate(
                '() => document.documentElement.scrollWidth - document.documentElement.clientWidth')
            note(f'overflow horizontal [{largeur}]', of <= 0, f'{of}px')

            # -- cibles tactiles
            petites = page.evaluate(r"""
              () => {
                const sel = 'a[href], button, input, select, textarea, [tabindex]:not([tabindex="-1"])';
                const mauvais = [];
                document.querySelectorAll(sel).forEach((el) => {
                  if (el.closest('dialog:not([open])')) return;
                  const cs = getComputedStyle(el);
                  if (cs.display === 'none' || cs.visibility === 'hidden') return;
                  // La case de puce est volontairement superposée à son label :
                  // c'est le label qui porte la cible tactile.
                  if (el.classList.contains('puce__case')) return;
                  // Lien d'évitement : 1x1 hors focus, pleine taille au focus.
                  // C'est le motif accessible standard, pas une cible trop petite.
                  if (el.classList.contains('evitement')) return;
                  const r = el.getBoundingClientRect();
                  if (r.width === 0 && r.height === 0) return;
                  if (r.width < 44 || r.height < 44) {
                    mauvais.push((el.className || el.tagName) + ' ' +
                                 Math.round(r.width) + 'x' + Math.round(r.height));
                  }
                });
                return mauvais;
              }
            """)
            note(f'cibles tactiles ≥44px [{largeur}]', len(petites) == 0,
                 'toutes conformes' if not petites else f'{len(petites)} trop petites : {petites[:3]}')

            # -- termes bannis, sur le texte RENDU
            texte = page.evaluate('() => document.body.innerText').lower()
            trouves = [t for t in TERMES_BANNIS if re.search(t, texte)]
            note(f'termes e-commerce bannis [{largeur}]', not trouves,
                 'aucun' if not trouves else f'TROUVÉS : {trouves}')

            # -- le filtrage fonctionne-t-il réellement ?
            if largeur >= 900:
                avant = page.eval_on_selector_all('.entree', 'e => e.length')
                page.click('.puce__case[value="chypree"]', force=True)
                page.wait_for_timeout(200)
                apres = page.eval_on_selector_all('.entree', 'e => e.length')
                url_ok = 'famille=chypree' in page.url
                note(f'filtre + sync URL [{largeur}]', 0 < apres < avant and url_ok,
                     f'{avant} → {apres} références, URL={"oui" if url_ok else "NON"}')
                page.click('#tout-effacer')
                page.wait_for_timeout(200)

            # -- la fiche produit s'ouvre-t-elle vraiment ?
            page.click('.entree')
            page.wait_for_timeout(400)
            ouverte = page.evaluate('() => document.getElementById("fiche").open')
            etages = page.eval_on_selector_all('#fiche-pyramide .etage', 'e => e.length')
            note(f'fiche + pyramide [{largeur}]', ouverte and etages == 3,
                 f'ouverte={ouverte}, {etages} étages (tête/cœur/fond)')
            if not rapide and ouverte:
                mesurer_contraste(page, f'fiche {largeur} haut')
                # En étroit la fiche défile : le bas (prix, source) n'est pas
                # visible au premier écran. On le mesure vraiment, plutôt que de
                # le déclarer conforme sans l'avoir vu.
                defile = page.evaluate("""() => {
                  const f = document.getElementById('fiche');
                  const avant = f.scrollTop;
                  f.scrollTop = f.scrollHeight;
                  return f.scrollTop > avant;
                }""")
                if defile:
                    page.wait_for_timeout(200)
                    mesurer_contraste(page, f'fiche {largeur} bas')
            page.keyboard.press('Escape')
            page.wait_for_timeout(300)

            # -- panneau de filtres mobile : ouvert ET vérifié (CLAUDE.md §5)
            if largeur < 900:
                page.click('#ouvrir-filtres')
                page.wait_for_timeout(450)
                ouv = page.evaluate('() => document.getElementById("feuille").open')
                puces = page.eval_on_selector_all('#feuille-corps .puce', 'e => e.length')
                note(f'feuille filtres mobile [{largeur}]', ouv and puces > 0,
                     f'ouverte={ouv}, {puces} puces dans la feuille')
                page.keyboard.press('Escape')
                page.wait_for_timeout(300)
                rendu = page.eval_on_selector_all('#ancre-filtres .puce', 'e => e.length')
                note(f'panneau rendu au rail [{largeur}]', rendu > 0,
                     f'{rendu} puces revenues dans le rail')

            if not rapide:
                mesurer_contraste(page, f'page {largeur}')

            note(f'console propre [{largeur}]',
                 not erreurs and not avertissements and not echecs_reseau,
                 f'{len(erreurs)} err, {len(avertissements)} warn, {len(echecs_reseau)} réseau'
                 + (f' → {erreurs[:2] or echecs_reseau[:2]}' if (erreurs or echecs_reseau) else ''))
            ctx.close()
            print()

        # -- mouvement réduit : testé, pas supposé
        print(f'{GRIS}── prefers-reduced-motion {"─" * 38}{RAZ}')
        ctx = nav.new_context(viewport={'width': 1440, 'height': 900},
                              reduced_motion='reduce', device_scale_factor=1, locale='fr-FR')
        page = ctx.new_page()
        page.goto(base, wait_until='networkidle')
        page.wait_for_timeout(300)
        invisibles = page.evaluate(r"""
          () => {
            let n = 0;
            document.querySelectorAll('.entree, .hero__titre, .editorial__nom, section')
              .forEach((el) => {
                const cs = getComputedStyle(el);
                if (parseFloat(cs.opacity) < 0.99) n++;
              });
            return n;
          }
        """)
        anim = page.evaluate(
            '() => document.getAnimations().filter(a => a.playState === "running").length')
        note('reduced-motion : contenu visible', invisibles == 0,
             f'{invisibles} élément(s) sous opacité 1')
        note('reduced-motion : rien ne tourne', anim == 0, f'{anim} animation(s) en cours')
        ctx.close()

        nav.close()
    srv.shutdown()

    # ---------------------------------------------------------------- bilan
    print(f'\n{GRIS}{"═" * 72}{RAZ}')
    ko = [r for r in resultats if not r[1] and not r[3]]
    tol = [r for r in resultats if not r[1] and r[3]]
    print(f'{len(resultats) - len(ko) - len(tol)}/{len(resultats)} OK'
          + (f', {len(tol)} tolérés' if tol else '')
          + (f', {ROUGE}{len(ko)} FAIL{RAZ}' if ko else f' — {VERT}aucun échec{RAZ}'))
    for z, _, d, _ in ko:
        print(f'  {ROUGE}✗{RAZ} {z} — {d}')
    return 1 if ko else 0


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--rapide', action='store_true',
                    help='saute la mesure de contraste (la plus lente)')
    sys.exit(auditer(ap.parse_args().rapide))
