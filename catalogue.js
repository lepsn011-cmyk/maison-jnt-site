/* ============================================================================
   catalogue.js — LA source de donnée du site Maison JNT
   ----------------------------------------------------------------------------
   Le site est piloté à 100 % par ce fichier. index.html ne contient aucune
   référence de parfum en dur : ajouter, retirer ou modifier une entrée ici
   suffit, aucune retouche de code n'est nécessaire.

   VOLONTAIREMENT un .js (et non un .json chargé par fetch) : un fetch() échoue
   en file:// — le client doit pouvoir ouvrir index.html par double-clic.

   ---------------------------------------------------------------------------
   DONNÉES RÉELLES, PAS INVENTÉES
   Les 20 parfums existent, sont distribués sur le segment visé, et chaque
   pyramide olfactive provient d'une source publique vérifiée (champ `source`).
   Aucun nom, aucune note, aucune marque n'a été inventé.

   Deux erreurs évitées par la vérification, à ne pas réintroduire :
     - « Philos Jade » (Maison Alhambra) N'EXISTE PAS. Le nom paraissait
       plausible ; la recherche l'a infirmé. Remplacé par Salvo et
       Philos Messenger, réels.
     - « Ameerat Al Arab » est d'ASDAAF (groupe Lattafa), pas de Paris Corner.

   PRIX : inconnus à ce stade → tous à `null`. Voir prixOuContact() dans
   index.html : `null` affiche un appel au contact, jamais « 0 € » ni « null ».
   Ne PAS remplir au jugé — un montant faux publié se remarque.

   FAMILLES : florale | boisee | ambree | hesperidee | fougere | chypree
   GENRES   : homme | femme | mixte
   CONCENTR.: EDT | EDP | Extrait
   ========================================================================== */

window.CATALOGUE = [

  /* ---------------------------------------------------------------- LATTAFA */
  {
    slug: 'lattafa-khamrah',
    nom: 'Khamrah',
    marque: 'Lattafa',
    annee: 2022,
    genre: 'mixte',
    concentration: 'EDP',
    famille: 'ambree',
    nouveaute: false,
    editionLimitee: false,
    prix: null,
    notes: {
      tete: ['Cannelle', 'Muscade', 'Bergamote'],
      coeur: ['Datte', 'Praline', 'Tubéreuse', 'Mahonial'],
      fond: ['Vanille', 'Fève tonka', 'Amberwood', 'Myrrhe', 'Benjoin', 'Akigalawood']
    },
    description: "Une ouverture d'épices chaudes qui glisse vers la datte et la praline, puis s'installe longuement sur la vanille et les baumes. Le gourmand oriental qui a fait la réputation de la maison.",
    source: 'https://www.fragrantica.com/perfume/Lattafa-Perfumes/Khamrah-78539.html'
  },
  {
    slug: 'lattafa-yara',
    nom: 'Yara',
    marque: 'Lattafa',
    annee: 2020,
    genre: 'femme',
    concentration: 'EDP',
    famille: 'ambree',
    nouveaute: false,
    editionLimitee: false,
    prix: null,
    notes: {
      tete: ['Orchidée', 'Héliotrope', 'Mandarine'],
      coeur: ['Accord gourmand', 'Fruits tropicaux'],
      fond: ['Vanille', 'Musc', 'Santal']
    },
    description: "Crémeux, sucré, très enveloppant. La mandarine et l'orchidée s'effacent vite devant un fond de vanille et de santal qui tient toute la journée.",
    source: 'https://www.fragrantica.com/perfume/Lattafa-Perfumes/Yara-76880.html'
  },
  {
    slug: 'lattafa-asad',
    nom: 'Asad',
    marque: 'Lattafa',
    annee: 2021,
    genre: 'homme',
    concentration: 'EDP',
    famille: 'ambree',
    nouveaute: false,
    editionLimitee: false,
    prix: null,
    notes: {
      tete: ['Poivre noir', 'Tabac', 'Ananas'],
      coeur: ['Patchouli', 'Café', 'Iris'],
      fond: ['Vanille', 'Ambre', 'Bois secs', 'Benjoin', 'Labdanum']
    },
    description: "Le contraste ananas-tabac à l'ouverture, puis un cœur de café et de patchouli. Un ambré masculin franc, sans détour.",
    source: 'https://www.fragrantica.com/perfume/Lattafa-Perfumes/Asad-72821.html'
  },
  {
    slug: 'lattafa-embrace',
    nom: 'Embrace',
    marque: 'Lattafa',
    annee: 2025,
    genre: 'mixte',
    concentration: 'EDP',
    famille: 'chypree',
    nouveaute: true,
    editionLimitee: false,
    prix: null,
    notes: {
      tete: ['Gingembre', 'Bergamote', 'Armoise'],
      coeur: ['Patchouli', 'Sapin baumier', 'Encens'],
      fond: ['Benjoin', 'Ambre gris', 'Mousse de chêne']
    },
    description: "Un chypré boisé contemporain : bergamote et gingembre sur une base de mousse de chêne et d'ambre gris. L'encens et le sapin lui donnent une tenue résineuse peu commune à ce niveau de prix.",
    source: 'https://www.fragrantica.com/perfume/Lattafa-Perfumes/Embrace-121613.html'
  },
  {
    slug: 'lattafa-fakhar-rose',
    nom: 'Fakhar Rose',
    marque: 'Lattafa',
    annee: 2022,
    genre: 'femme',
    concentration: 'EDP',
    famille: 'florale',
    nouveaute: false,
    editionLimitee: false,
    prix: null,
    notes: {
      tete: ['Fruits', 'Lys', 'Grenade', 'Aldéhydes'],
      coeur: ['Tubéreuse', 'Jasmin', 'Gardénia', 'Ylang-ylang', 'Rose', 'Chèvrefeuille', 'Pivoine'],
      fond: ['Vanille', 'Musc blanc', 'Santal', 'Ambroxan']
    },
    description: "Un grand bouquet blanc — sept fleurs au cœur — posé sur un fond vanillé et musqué. Le floral le plus généreux du rayon.",
    source: 'https://www.fragrantica.com/perfume/Lattafa-Perfumes/Fakhar-Rose-70466.html'
  },

  /* -------------------------------------------------------- MAISON ALHAMBRA */
  {
    slug: 'maison-alhambra-jean-lowe-ombre',
    nom: 'Jean Lowe Ombre',
    marque: 'Maison Alhambra',
    annee: 2023,
    genre: 'homme',
    concentration: 'EDP',
    famille: 'boisee',
    nouveaute: false,
    editionLimitee: false,
    prix: null,
    notes: {
      tete: ['Oud', 'Encens'],
      coeur: ['Rose', 'Safran', 'Framboise', 'Bouleau'],
      fond: ['Ambre', 'Benjoin', 'Géranium']
    },
    description: "L'oud et l'encens d'emblée, adoucis par une rose safranée. Boisé fumé, sombre, à réserver aux soirées fraîches.",
    source: 'https://www.fragrantica.com/perfume/Maison-Alhambra/Jean-Lowe-Ombre-91352.html'
  },
  {
    slug: 'maison-alhambra-salvo',
    nom: 'Salvo',
    marque: 'Maison Alhambra',
    annee: 2022,
    genre: 'homme',
    concentration: 'EDP',
    famille: 'fougere',
    nouveaute: false,
    editionLimitee: false,
    prix: null,
    notes: {
      tete: ['Bergamote'],
      coeur: ['Lavande', 'Poivre de Sichuan', 'Anis étoilé', 'Muscade'],
      fond: ['Ambroxan', 'Vanille']
    },
    description: "Fougère orientale : la lavande tient le cœur, relevée au poivre de Sichuan et à l'anis, sur un fond d'ambroxan très présent.",
    source: 'https://www.fragrantica.com/perfume/Maison-Alhambra/Salvo-93538.html'
  },
  {
    slug: 'maison-alhambra-philos-messenger',
    nom: 'Philos Messenger',
    marque: 'Maison Alhambra',
    annee: 2022,
    genre: 'mixte',
    concentration: 'EDP',
    famille: 'hesperidee',
    nouveaute: false,
    editionLimitee: false,
    prix: null,
    notes: {
      tete: ['Pamplemousse', 'Bergamote', 'Gingembre'],
      coeur: ['Magnolia', 'Jasmin', 'Iris'],
      fond: ['Ambre', 'Notes boisées']
    },
    description: "Ouverture agrumes-gingembre nette, cœur floral discret, fond ambré boisé. Le plus facile à porter au bureau de la sélection.",
    source: 'https://www.fragrantica.com/perfume/Maison-Alhambra/Philos-Messenger-112537.html'
  },
  {
    slug: 'maison-alhambra-grise',
    nom: 'Grise',
    marque: 'Maison Alhambra',
    annee: 2022,
    genre: 'mixte',
    concentration: 'EDP',
    famille: 'chypree',
    nouveaute: false,
    editionLimitee: false,
    prix: null,
    notes: {
      tete: ['Rose', 'Bergamote'],
      coeur: ['Patchouli', 'Cèdre'],
      fond: ['Mousse de chêne', 'Santal', 'Ambre']
    },
    description: "Un chypre au sens classique : bergamote et rose en tête, mousse de chêne en fond. La rose y est traitée en accord neutre, jamais démonstrative.",
    source: 'https://www.fragrantica.com/perfume/Maison-Alhambra/Grise-104251.html'
  },

  /* ------------------------------------------------------------------ ARMAF */
  {
    slug: 'armaf-club-de-nuit-intense-man',
    nom: 'Club de Nuit Intense Man',
    marque: 'Armaf',
    annee: 2015,
    genre: 'homme',
    concentration: 'EDT',
    famille: 'boisee',
    nouveaute: false,
    editionLimitee: false,
    prix: null,
    notes: {
      tete: ['Citron', 'Ananas', 'Bergamote', 'Cassis', 'Pomme'],
      coeur: ['Bouleau', 'Jasmin', 'Rose'],
      fond: ['Musc', 'Ambre gris', 'Patchouli', 'Vanille']
    },
    description: "L'ananas et la pomme sur un fond de bouleau fumé. Boisé épicé, projection forte — la référence la plus demandée du rayon depuis dix ans.",
    source: 'https://www.fragrantica.com/perfume/Armaf/Club-de-Nuit-Intense-Man-34696.html'
  },
  {
    slug: 'armaf-club-de-nuit-woman',
    nom: 'Club de Nuit Woman',
    marque: 'Armaf',
    annee: 2015,
    genre: 'femme',
    concentration: 'EDP',
    famille: 'florale',
    nouveaute: false,
    editionLimitee: false,
    prix: null,
    notes: {
      tete: ['Bergamote', 'Pamplemousse', 'Pêche', 'Orange'],
      coeur: ['Géranium', 'Jasmin', 'Litchi', 'Rose'],
      fond: ['Musc', 'Patchouli', 'Vanille', 'Vétiver']
    },
    description: "Floral fruité lumineux : pêche et litchi sur un cœur de rose et de jasmin, tenu par un fond patchouli-vétiver qui l'empêche de tourner au sucré.",
    source: 'https://www.fragrantica.com/perfume/Armaf/Club-de-Nuit-Woman-27655.html'
  },
  {
    slug: 'armaf-tres-nuit',
    nom: 'Tres Nuit',
    marque: 'Armaf',
    annee: 2015,
    genre: 'homme',
    concentration: 'EDT',
    famille: 'fougere',
    nouveaute: false,
    editionLimitee: false,
    prix: null,
    notes: {
      tete: ['Iris', 'Citron', 'Verveine'],
      coeur: ['Lavande', 'Violette', 'Notes épicées'],
      fond: ['Ambre gris', 'Santal']
    },
    description: "Structure de fougère aromatique : citron et verveine en tête, lavande et violette au cœur, santal en fond. Vert, propre, très printanier.",
    source: 'https://www.fragrantica.com/perfume/Armaf/Tres-Nuit-27711.html'
  },

  /* --------------------------------------------------- MAISON MASSIMO PARIS */
  {
    slug: 'maison-massimo-gold-signature',
    nom: 'Gold Signature',
    marque: 'Maison Massimo Paris',
    annee: 2024,
    genre: 'mixte',
    concentration: 'EDP',
    famille: 'ambree',
    nouveaute: true,
    editionLimitee: false,
    prix: null,
    notes: {
      tete: ['Rhubarbe', 'Miel', 'Bergamote', 'Orange'],
      coeur: ['Notes solaires', 'Framboise', 'Cèdre'],
      fond: ['Ambre gris', 'Musc', 'Patchouli', 'Vanille']
    },
    description: "La rhubarbe et le miel donnent une ouverture acidulée inhabituelle, avant un cœur solaire et un fond ambré. Parfumerie française de niche, sur une base ambrée classique.",
    source: 'https://www.fragrantica.com/perfume/Maison-Massimo/Gold-Signature-96748.html'
  },
  {
    slug: 'maison-massimo-voyage-de-nuit',
    nom: 'Voyage de Nuit',
    marque: 'Maison Massimo Paris',
    annee: 2024,
    genre: 'mixte',
    concentration: 'EDP',
    famille: 'ambree',
    nouveaute: true,
    editionLimitee: false,
    prix: null,
    notes: {
      tete: ['Ananas', 'Jacinthe'],
      coeur: ['Poivre rose', 'Jasmin', 'Iris'],
      fond: ['Ambre', 'Vanille', 'Musc', 'Patchouli']
    },
    description: "Ananas et jacinthe en ouverture, puis un cœur poivré-iris. Le fond ambre-vanille l'installe résolument du côté du soir.",
    source: 'https://www.fragrantica.com/perfume/Maison-Massimo/Voyage-de-Nuit-96747.html'
  },

  /* ----------------------------------------------------------------- RASASI */
  {
    slug: 'rasasi-hawas-for-him',
    nom: 'Hawas for Him',
    marque: 'Rasasi',
    annee: 2015,
    genre: 'homme',
    concentration: 'EDP',
    famille: 'hesperidee',
    nouveaute: false,
    editionLimitee: false,
    prix: null,
    notes: {
      tete: ['Pomme', 'Bergamote', 'Citron', 'Cannelle'],
      coeur: ['Fleur d\'oranger', 'Cardamome', 'Prune', 'Notes aquatiques'],
      fond: ['Patchouli', 'Ambre gris', 'Bois flotté', 'Musc']
    },
    description: "Hespéridé aquatique : agrumes et pomme sur des notes marines, fond de bois flotté et d'ambre gris. Le passe-partout de l'été, avec une vraie tenue.",
    source: 'https://www.fragrantica.com/perfume/Rasasi/Hawas-for-Him-46890.html'
  },

  /* ------------------------------------------------------------------ AFNAN */
  {
    slug: 'afnan-9pm',
    nom: '9PM',
    marque: 'Afnan',
    annee: 2020,
    genre: 'homme',
    concentration: 'EDP',
    famille: 'ambree',
    nouveaute: false,
    editionLimitee: false,
    prix: null,
    notes: {
      tete: ['Pomme', 'Cannelle', 'Lavande sauvage', 'Bergamote'],
      coeur: ['Fleur d\'oranger', 'Muguet'],
      fond: ['Vanille', 'Fève tonka', 'Ambre', 'Patchouli']
    },
    description: "Pomme et cannelle sur une base vanille-tonka très douce. Ambré accessible, souvent le premier parfum oriental d'un client.",
    source: 'https://www.fragrantica.com/perfume/Afnan/9pm-65414.html'
  },

  /* -------------------------------------------------------- FRAGRANCE WORLD */
  {
    slug: 'fragrance-world-barakkat-rouge-540',
    nom: 'Barakkat Rouge 540',
    marque: 'Fragrance World',
    annee: 2024,
    genre: 'mixte',
    concentration: 'Extrait',
    famille: 'boisee',
    nouveaute: true,
    editionLimitee: false,
    prix: null,
    notes: {
      tete: ['Amande amère', 'Safran'],
      coeur: ['Cèdre', 'Jasmin'],
      fond: ['Notes boisées', 'Ambre gris', 'Musc']
    },
    description: "Amande amère et safran sur un fond boisé ambré. Version extrait : concentration plus élevée, sillage plus dense, tenue nettement supérieure à l'eau de parfum.",
    source: 'https://www.fragrantica.com/perfume/Fragrance-World/Barakkat-Rouge-540-Extrait-de-Parfum-107710.html'
  },

  /* ------------------------------------------------------------ AL HARAMAIN */
  {
    slug: 'al-haramain-amber-oud-gold-edition',
    nom: 'Amber Oud Gold Edition',
    marque: 'Al Haramain',
    annee: 2022,
    genre: 'mixte',
    concentration: 'EDP',
    famille: 'ambree',
    nouveaute: false,
    editionLimitee: false,
    prix: null,
    notes: {
      tete: ['Notes vertes', 'Bergamote'],
      coeur: ['Notes sucrées', 'Melon', 'Ananas', 'Cèdre', 'Ambre'],
      fond: ['Notes boisées', 'Musc', 'Vanille', 'Myrrhe']
    },
    description: "Fruité en tête, ambré en fond : melon et ananas sur cèdre, puis vanille et myrrhe. Le plus solaire des ambrés de la sélection.",
    source: 'https://www.fragrantica.com/perfume/Al-Haramain-Perfumes/Amber-Oud-Gold-Edition-51816.html'
  },

  /* ----------------------------------------------------------- PARIS CORNER */
  {
    slug: 'paris-corner-rifaaqat-adorn',
    nom: 'Rifaaqat Adorn',
    marque: 'Paris Corner',
    annee: 2024,
    genre: 'mixte',
    concentration: 'EDP',
    famille: 'chypree',
    nouveaute: true,
    editionLimitee: false,
    prix: null,
    notes: {
      tete: ['Poivre rose', 'Coriandre', 'Mandarine', 'Violette'],
      coeur: ['Patchouli', 'Cèdre', 'Mousse de chêne'],
      fond: ['Ambre gris', 'Benjoin', 'Vanille']
    },
    description: "Poivre rose et coriandre sur un cœur de patchouli et de mousse de chêne. Chypré boisé, plus sec et plus adulte que la moyenne du rayon.",
    source: 'https://www.fragrantica.com/perfume/PARIS-CORNER/Rifaaqat-Adorn-98136.html'
  },

  /* ----------------------------------------------------------------- ASDAAF */
  {
    slug: 'asdaaf-ameerat-al-arab',
    nom: 'Ameerat Al Arab',
    marque: 'Asdaaf',
    annee: 2022,
    genre: 'femme',
    concentration: 'EDP',
    famille: 'florale',
    nouveaute: false,
    editionLimitee: false,
    prix: null,
    notes: {
      tete: ['Agrumes', 'Bergamote'],
      coeur: ['Musc blanc', 'Aloe vera'],
      fond: ['Jasmin', 'Musc', 'Notes boisées', 'Oud']
    },
    description: "Floral clair et musqué : agrumes et aloe en ouverture, jasmin et une touche d'oud en fond. Léger pour un parfum oriental, taillé pour la journée.",
    source: 'https://www.fragrantica.com/perfume/Asdaaf/Ameerat-Al-Arab-81376.html'
  }
];

/* ============================================================================
   LA MAISON DU MOIS — section éditoriale
   Change de marque au gré du client. `parfums` liste des `slug` du catalogue :
   si un slug n'existe plus, il est simplement ignoré à l'affichage.
   ========================================================================== */
window.MAISON_DU_MOIS = {
  marque: 'Lattafa',
  origine: 'Dubaï, Émirats arabes unis',
  texte: "Fondée à Dubaï, Lattafa Perfumes est devenue en quelques années la maison la plus demandée du parfum oriental accessible — au point que ses best-sellers figurent aujourd'hui parmi les parfums les plus vendus au monde sur les grandes plateformes. Sa signature : des compositions ambrées généreuses, une tenue longue, et un rapport qualité-prix qui a redéfini les attentes du rayon. La maison édite également Maison Alhambra et Asdaaf, deux marques que vous retrouverez aussi dans nos rayons.",
  parfums: ['lattafa-khamrah', 'lattafa-asad', 'lattafa-fakhar-rose']
};

/* ============================================================================
   LA BOUTIQUE
   ----------------------------------------------------------------------------
   Les champs à `null` sont AFFICHÉS COMME « à confirmer » par le site — ils ne
   disparaissent pas et ne sont pas remplis au jugé. Renseigner une valeur la
   fait apparaître immédiatement, sans autre modification.

   Ces informations n'ont pas été inventées faute de source fiable : la bio
   Instagram transmise était tronquée sur la capture (adresse, horaires et
   pseudo coupés). Publier une fausse adresse pour un commerce réel serait une
   erreur bien plus coûteuse qu'un champ vide.
   ========================================================================== */
window.BOUTIQUE = {
  nom: 'Maison JNT',
  signature: 'Fragrance House',
  accroche: "Une centaine de références en rayon, et la seule façon de choisir un parfum : le sentir.",
  invitation: "Passez quand vous voulez. On vous fait sentir, on vous explique, et vous repartez avec ce qui vous va — pas avec ce qu'on veut vendre.",

  adresse: null,        // à confirmer avec le client
  codePostal: null,     // à confirmer
  ville: null,          // à confirmer
  telephone: null,      // à confirmer
  instagram: null,      // pseudo tronqué sur la capture — à confirmer
  horaires: null,       // à confirmer (ex. [{ jours: 'Lundi – Samedi', heures: '10h – 19h30' }])

  photo: 'assets/boutique-interieur.jpg'  // fichier non fourni → placeholder nommé
};
