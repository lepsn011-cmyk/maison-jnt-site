# PRODUCT.md — Maison JNT

> Contexte de projet pour les skills de design (`impeccable`, `ui-ux-pro-max`).
> Écrit **avant** la première ligne de HTML, conformément à `CLAUDE.md` §1.1 et §2 Phase 1.

## Register

**`brand`** — le design EST le produit.

Ce n'est pas un outil ni une application : c'est la vitrine d'un commerce physique. La page doit
donner envie de pousser la porte de la boutique. Le catalogue n'est pas un tunnel de conversion,
c'est un **argumentaire de choix** : montrer l'étendue de ce qu'on trouve en rayon.

## Purpose

Faire venir en boutique. Trois usages réels, dans cet ordre :

1. **« Est-ce qu'ils ont *ce* parfum ? »** — le visiteur a une marque ou un nom en tête. Il doit
   pouvoir vérifier en quelques secondes. C'est pourquoi la navigation **par marque** compte autant
   que par catégorie : c'est un revendeur multi-marques, pas une maison à parfum unique.
2. **« Qu'est-ce qui me plairait ? »** — le visiteur ne sait pas. Il navigue par **famille
   olfactive**, par genre, par concentration. Le filtrage est la colonne vertébrale du site, pas un
   accessoire.
3. **« Où et quand j'y vais ? »** — adresse, horaires, itinéraire. La boutique est un actif
   éditorial de plein droit, pas une note de bas de page.

Le site ne vend rien en ligne. Aucun panier, aucun paiement, aucune commande.

## Users

- **Le client qui connaît** : cherche une référence précise (« vous avez le Khamrah ? »). Entre par
  la recherche ou par la marque. Veut une réponse, pas une découverte.
- **Le curieux** : sait qu'il aime « le boisé » ou « quelque chose de sucré », pas les noms.
  Entre par la famille olfactive. La **pyramide olfactive** (tête / cœur / fond) est son outil :
  c'est le vocabulaire du métier, et l'afficher signale une vraie expertise.
- **Le passant local** : a vu la devanture ou l'Instagram. Vient vérifier les horaires. Doit
  trouver l'information en un écran, sans scroller le catalogue.

Tous les trois sont majoritairement sur **mobile**. Le site est conçu mobile-first, sans exception.

## Brand personality

La demande du client, verbatim : **« direction similaire aux grandes parfumeries, mais sans trop
abuser du luxe »**. Un peu de luxe, pas trop.

Traduction opérationnelle — le site doit se situer entre deux repoussoirs :

- **Trop bas** : la grande surface parfumerie. Bandeaux défilants, prix barrés, pastilles de
  remise, badges de réassurance, pop-up newsletter. Refusé explicitement par le client.
- **Trop haut** : la maison de luxe parisienne. Noir et or, page contemplative, trois flacons par
  écran, silence et vide. Ce serait un mensonge sur ce qu'est cette boutique.

**Le bon registre : le commerce spécialisé bien tenu.** Soigné, dense, compétent. Quelqu'un qui
connaît ses produits et en a beaucoup.

## Ce que la boutique physique nous apprend

La photo d'intérieur analysée montre : des murs entiers de flacons, un éclairage chaud, une forte
densité de références. **La promesse n'est pas la rareté, c'est le choix et l'abondance.**

Conséquence de design, non négociable : la grille catalogue est **généreuse et dense**. Pas une
galerie contemplative à trois produits par écran. La densité *est* l'argument commercial — la
traduire en vide serait trahir le commerce.

## Anti-références

Sources analysées, et ce qu'on en prend / ce qu'on refuse.

**`pds-shop.fr`** (même métier : revendeur multi-marques avec boutique physique)
- ✅ La boutique traitée en actif éditorial
- ✅ La navigation par marque en plus des catégories
- ✅ Le segment produit (source des données de démonstration)

**`parfumscollectionprivee.fr`**
- ✅ **Uniquement** la taxonomie : Homme / Femme / Unisexe / Nouveautés / Édition limitée
- ❌ Tout le reste

**Interdits absolus** — issus des deux sites, refusés nommément par le client :
- Bandeau défilant chargé (livraison / avis / paiement)
- Prix barrés, pastilles de remise, mentions de promotion
- « Ajouter au panier », tout vocabulaire de e-commerce
- Newsletter −10 %
- Badges de réassurance (paiement sécurisé, satisfait ou remboursé…)

C'est du e-commerce assumé — l'exact opposé du registre demandé. **Vérifié par grep sur le texte
rendu, pas par relecture visuelle** (`CLAUDE.md` §5).

## Principes

1. **La densité est un choix, pas un défaut.** Le catalogue montre beaucoup. Le rythme vient de la
   typographie et des bandes tonales, pas du vide.
2. **Le filtrage est un produit, pas un widget.** Compteur en direct, état vide avec issue réelle,
   URL partageable, retour navigateur qui restaure l'état.
3. **La pyramide olfactive est la preuve d'expertise.** Elle est la pièce maîtresse de la fiche, pas
   une ligne de spécifications.
4. **Aucune donnée inventée.** Les 20 parfums sont réels, avec leurs vraies pyramides et une source
   vérifiable. Les prix sont inconnus → ils s'effacent au profit d'un contact. L'adresse est
   inconnue → elle s'affiche comme champ à confirmer, jamais comme une fausse adresse.
5. **Rien ne bouge sans raison.** Filtrer est un geste répété : il est instantané. Le mouvement est
   réservé à ce qui est occasionnel (ouverture d'une fiche).

## Accessibilité

Cible **WCAG AA, mesurée au pixel composite** — jamais un calcul théorique token contre token.

- Texte courant ≥ 4.5:1, texte large ≥ 3:1
- Toutes les cibles tactiles ≥ 44 × 44 px
- Focus visible partout, jamais supprimé
- `prefers-reduced-motion` : contenu 100 % visible sans JS ni animation
- La couleur ne porte jamais seule une information (les familles olfactives ne sont pas codées par
  couleur — elles sont nommées)
- Compteur de résultats en `aria-live="polite"`
- Français : `lang="fr"`, contenu et libellés en français
