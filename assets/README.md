# assets/

## Ce que contient ce dossier aujourd'hui

```
fonts/    6 fichiers .woff2 — polices auto-hébergées (166 Ko au total)
```

Les polices ne sont **pas** chargées depuis Google : elles sont servies par le
site lui-même. Trois raisons, dans cet ordre :

1. **Vérifiabilité.** L'environnement de recette n'atteint pas
   `fonts.googleapis.com` : les captures de contrôle auraient montré des polices
   de repli en laissant croire au rendu réel.
2. **Vie privée.** Aucune requête du visiteur vers un tiers — la CNIL a
   sanctionné l'appel Google Fonts côté client sur des sites français.
3. **Performance.** Plus de résolution DNS ni de connexion externe au chargement.

Signature `wOF2` de chacun des 6 fichiers vérifiée à l'octet, taille déclarée
égale à la taille réelle. Ils ne sont pas à remplacer.

## Ce qui manque, et que seul le client peut fournir

Ces deux fichiers n'existent pas encore. Le site fonctionne sans eux et affiche
un emplacement nommé à leur place — il ne prétend jamais qu'ils existent.

### `logo-jnt.svg` (ou un PNG détouré haute définition)

En attendant, le wordmark « JNT Maison / Fragrance House » est une
**reconstruction typographique** (Bodoni Moda + Italianno). Elle est isolée dans
un seul composant `.marque` d'`index.html` : la remplacer par le vrai fichier est
une édition, pas un chantier.

Ce fichier verrouille aussi la **valeur exacte du beige**. Le token `--beige`
d'`index.html` est aujourd'hui *estimé visuellement* depuis une capture
Instagram — pas mesuré au pixel, faute de fichier source. C'est **une seule
ligne** à corriger à réception :

```css
--beige: oklch(0.902 0.014 52);   /* ← à remplacer par la valeur mesurée */
```

### `boutique-interieur.jpg`

La photo d'intérieur de la boutique. L'emplacement est déjà réservé au ratio
**4/5** dans la section « La boutique » : l'intégration ne décalera rien sur la
page.

Avant intégration, vérifier le **format réel** du fichier fourni (`PIL.Image.open(...).format`),
jamais son extension — un `.jpg` peut être un PNG renommé et peser dix fois trop
lourd. Convertir en JPEG progressif optimisé, viser < 300 Ko.

## Rappel

Le poids total de `assets/` doit rester sous ~2 Mo. Aujourd'hui : 166 Ko.
