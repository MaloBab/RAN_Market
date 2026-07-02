# Catalogue robot RAN — Frontend (Vue 3 + TS + Tailwind v4)

## Démarrer
```bash
npm install
npm run dev
```

## Build
```bash
npm run build
```

## Arborescence
```
src/
  types/          Interfaces TS (Robot, Filtres, Utilisateur, Devis, Import)
  services/       Couche API mockée (DIP: contrats + implémentations mock)
  stores/         Pinia (auth, robots, devis, backoffice)
  composables/    Logique métier (useViewStrategy = pattern Strategy, filtres, devis form)
  components/
    ui/           Composants mutualisés (Button, Badge, Card, Modal, RedactedField…)
    layout/       Header, toggle Vue Commerciale/Client
    catalogue/    Filtres, grille, carte robot, comparateur
    robot/        Galerie, specs, panneau commercial, niveaux de rénovation
    backoffice/   Import Excel avec progression + rapport
    devis/        Formulaire de demande de devis
  views/          Pages routées
  router/         Vue Router + guards de rôle
```

## Authentification

Comptes de démonstration (pseudo base de données en dur, mots de passe
hashés en PBKDF2-SHA256, jamais stockés en clair — voir
`src/services/mocks/users.mock.ts` et `src/utils/crypto.ts`) :

| Rôle | Email | Mot de passe |
|---|---|---|
| Commercial | commercial@fanuc-ran.example | Commercial#2026 |
| Responsable RAN | responsable@fanuc-ran.example | ResponsableRAN#2026 |

La session est un token opaque généré côté "serveur" (mock), stocké en
`sessionStorage` (effacé à la fermeture de l'onglet), revalidé à chaque
navigation. Les routes `/back-office`, `/coming-soon`, `/comparateur`
sont protégées par rôle via les guards de `src/router/index.ts`.

⚠️ Cette vérification reste exécutée dans le bundle JS livré au
navigateur : c'est un mock pédagogique, pas un mécanisme de sécurité de
production. Un vrai backend doit vérifier les identifiants côté serveur
et émettre un cookie httpOnly + secure.

## Ajout de robot au catalogue

Connecté en Responsable RAN → `/back-office` → bouton « Créer une fiche
manuellement » (formulaire structuré, CDC §2.3) ou glisser un fichier
Excel (import en masse, CDC §3.6). Dans les deux cas la fiche est créée
en statut « Brouillon ».
