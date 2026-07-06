import type { ComingSoonEntry, Robot } from '@/types'

const PLACEHOLDER = (seed: string) =>
  `https://picsum.photos/seed/${seed}/640/420`

export const MOCK_ROBOTS: Robot[] = [
  {
    id: 'FANUC-2024-001',
    modele: 'ARC Mate 100iD',
    type: 'Soudure arc',
    categorie: 'Soudure',
    anneeMiseEnService: 2018,
    heuresUtilisation: 14500,
    descriptionCourte:
      'Robot de soudure compact, idéal pour cellules de production à cadence élevée.',
    caracteristiques: {
      payloadKg: 12,
      rayonActionMm: 1441,
      axes: 6,
      typeBaie: 'R-30iB Plus',
      protectionIp: 'IP67 (poignet)',
      montage: 'Sol / Plafond'
    },
    prestationsDisponibles: [
      { niveau: 'Standard', garantieMois: 3 },
      { niveau: 'Quasi Neuve', garantieMois: 12 }
    ],
    media: {
      photosAvant: [PLACEHOLDER('arcmate100-1'), PLACEHOLDER('arcmate100-2')],
      galerieAvantApres: [
        { avant: PLACEHOLDER('am100-before'), apres: PLACEHOLDER('am100-after') }
      ]
    },
    documentation: { datasheetUrl: '#', flyerUrl: '#' },
    commercial: {
      prixCatalogueEUR: 28000,
      remisePct: 20,
      quantiteStock: 3,
      nombreOffresEnCours: 2,
      historiqueVentes: [
        { periode: '2025-Q4', unitesVendues: 4 },
        { periode: '2026-Q1', unitesVendues: 6 }
      ]
    },
    statut: 'Publié'
  },
  {
    id: 'FANUC-2024-002',
    modele: 'M-710iC/50',
    type: 'Articulé',
    categorie: 'Manutention',
    anneeMiseEnService: 2016,
    heuresUtilisation: 22100,
    descriptionCourte:
      'Robot polyvalent grande portée, parfait pour manutention et applications lourdes.',
    caracteristiques: {
      payloadKg: 50,
      rayonActionMm: 2050,
      axes: 6,
      typeBaie: 'R-30iB',
      protectionIp: 'IP65',
      montage: 'Sol'
    },
    prestationsDisponibles: [{ niveau: 'Premium', garantieMois: 6 }],
    media: {
      photosAvant: [PLACEHOLDER('m710-1'), PLACEHOLDER('m710-2')],
      galerieAvantApres: [
        { avant: PLACEHOLDER('m710-before'), apres: PLACEHOLDER('m710-after') }
      ],
      videoUrl: '#'
    },
    documentation: { datasheetUrl: '#' },
    commercial: {
      prixCatalogueEUR: 34500,
      remisePct: 15,
      quantiteStock: 1,
      nombreOffresEnCours: 1
    },
    statut: 'Publié'
  },
  {
    id: 'FANUC-2023-014',
    modele: 'CRX-10iA/L',
    type: 'Collaboratif',
    categorie: 'Cobot',
    anneeMiseEnService: 2021,
    heuresUtilisation: 5200,
    descriptionCourte:
      'Cobot léger sans carter de sécurité, déploiement rapide en cellule mixte.',
    caracteristiques: {
      payloadKg: 10,
      rayonActionMm: 1418,
      axes: 6,
      typeBaie: 'R-30iB Plus',
      protectionIp: 'IP54',
      montage: 'Sol / Mural'
    },
    prestationsDisponibles: [
      { niveau: 'Quasi Neuve', garantieMois: 12 },
      { niveau: 'Extension de garantie', garantieMois: null }
    ],
    media: {
      photosAvant: [PLACEHOLDER('crx10-1'), PLACEHOLDER('crx10-2')],
      galerieAvantApres: [{ avant: PLACEHOLDER('crx-before'), apres: PLACEHOLDER('crx-after') }]
    },
    documentation: { datasheetUrl: '#', brochureUrl: '#' },
    commercial: {
      prixCatalogueEUR: 41000,
      remisePct: 10,
      quantiteStock: 5,
      nombreOffresEnCours: 3
    },
    statut: 'Publié'
  },
  {
    id: 'FANUC-2022-031',
    modele: 'P-250iB',
    type: 'Peinture',
    categorie: 'Peinture',
    anneeMiseEnService: 2014,
    heuresUtilisation: 31000,
    descriptionCourte: 'Robot de peinture haute cadence, baie antidéflagrante.',
    caracteristiques: {
      payloadKg: 25,
      rayonActionMm: 2509,
      axes: 6,
      typeBaie: 'R-30iA',
      protectionIp: 'IP65 ATEX',
      montage: 'Sol / Rail'
    },
    prestationsDisponibles: [{ niveau: 'Peinture', garantieMois: null }],
    media: {
      photosAvant: [PLACEHOLDER('p250-1')],
      galerieAvantApres: [{ avant: PLACEHOLDER('p250-before'), apres: PLACEHOLDER('p250-after') }]
    },
    documentation: {},
    commercial: {
      prixCatalogueEUR: 19500,
      remisePct: 25,
      quantiteStock: 2,
      nombreOffresEnCours: 0
    },
    statut: 'Publié'
  },
  {
    id: 'FANUC-2025-007',
    modele: 'M-2iA/3SL Delta',
    type: 'Delta',
    categorie: 'Picking',
    anneeMiseEnService: 2020,
    heuresUtilisation: 8900,
    descriptionCourte: 'Robot delta ultra-rapide pour pick & place agroalimentaire.',
    caracteristiques: {
      payloadKg: 3,
      rayonActionMm: 800,
      axes: 4,
      typeBaie: 'R-30iB Plus',
      protectionIp: 'IP69K',
      montage: 'Plafond'
    },
    prestationsDisponibles: [{ niveau: 'Standard', garantieMois: 3 }],
    media: {
      photosAvant: [PLACEHOLDER('delta-1')],
      galerieAvantApres: [{ avant: PLACEHOLDER('delta-before'), apres: PLACEHOLDER('delta-after') }]
    },
    documentation: { datasheetUrl: '#' },
    commercial: {
      prixCatalogueEUR: 22900,
      remisePct: 8,
      quantiteStock: 4,
      nombreOffresEnCours: 1
    },
    statut: 'Publié'
  },
  {
    id: 'FANUC-2021-098',
    modele: 'M-410iC/185',
    type: 'Palettisation',
    categorie: 'Palettisation',
    anneeMiseEnService: 2012,
    heuresUtilisation: 41200,
    descriptionCourte: 'Robot de palettisation haute capacité, structure renforcée.',
    caracteristiques: {
      payloadKg: 185,
      rayonActionMm: 3143,
      axes: 4,
      typeBaie: 'R-30iA',
      protectionIp: 'IP65',
      montage: 'Sol'
    },
    prestationsDisponibles: [{ niveau: 'Échange standard', garantieMois: null }],
    media: {
      photosAvant: [PLACEHOLDER('m410-1')],
      galerieAvantApres: [{ avant: PLACEHOLDER('m410-before'), apres: PLACEHOLDER('m410-after') }]
    },
    documentation: {},
    commercial: {
      prixCatalogueEUR: 16800,
      remisePct: 30,
      quantiteStock: 1,
      nombreOffresEnCours: 0
    },
    statut: 'Publié'
  }
]

export const MOCK_COMING_SOON: ComingSoonEntry[] = [
  {
    id: 'CS-001',
    modele: 'R-2000iC/210F',
    type: 'Articulé',
    disponibiliteEstimee: 'T1 2027',
    niveauRenovationPrevu: 'Premium'
  },
  {
    id: 'CS-002',
    modele: 'CR-15iA',
    type: 'Collaboratif',
    disponibiliteEstimee: 'T4 2026',
    niveauRenovationPrevu: 'Quasi Neuve'
  }
]


