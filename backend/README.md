# RAN Catalogue — Backend

API FastAPI du catalogue de robots FANUC reconditionnés (RAN), construite
selon le cahier des charges v1.1 et branchée sur le frontend Vue.js
existant (contrat JSON identique, aucune modification frontend requise).

## Stack

- **FastAPI** (async) + **SQLAlchemy 2.0** (async) + **Pydantic v2**
- **SQLite** en développement (`aiosqlite`), compatible **PostgreSQL** en
  production (`asyncpg`) via simple changement de `DATABASE_URL`
- **JWT** (accès, 15 min) + **refresh token opaque** en cookie httpOnly
  (rotation à chaque renouvellement)
- **bcrypt** (passlib) pour le hachage des mots de passe
- **slowapi** pour le rate-limiting (`/auth/login`, `/devis`)

## Démarrage rapide

```bash
cd backend
pip install -r requirements.txt --break-system-packages   # ou: pip install -e .

cp .env.example .env
# Éditer .env : générer une vraie SECRET_KEY avec
#   python -c "import secrets; print(secrets.token_urlsafe(64))"

# Créer les comptes de démonstration + quelques robots publiés
python -m scripts.seed

# Lancer le serveur (recrée les tables si absentes au démarrage)
python -m uvicorn src.main:app --reload --port 8000
```

Documentation interactive : http://localhost:8000/docs

### Comptes de démonstration (créés par `scripts/seed.py`)

| Rôle             | Email                              | Mot de passe        |
|------------------|-------------------------------------|----------------------|
| Commercial       | commercial@fanuc-ran.example        | Commercial#2026      |
| Responsable RAN  | responsable@fanuc-ran.example       | ResponsableRAN#2026  |

## Architecture

```
src/
├── main.py            # Assemblage app, création auto de la BDD, sécurité transverse
├── config.py           # Settings (pydantic-settings), lues depuis .env
├── database.py          # Engine async + Base déclarative + get_db()
├── security.py           # Hash mots de passe, JWT, refresh tokens
├── auth/                  # Comptes, login/refresh/logout, dépendances RBAC
├── robots/                 # Catalogue : vue commerciale vs vue client, CRUD back-office
├── coming_soon/              # Section "Coming Soon" (vue commerciale uniquement)
├── devis/                      # Demandes de devis + assignation commerciale
├── imports/                     # Import Excel back-office (création de fiches en masse)
└── shared/                       # Enums, exceptions, schémas Pydantic communs
```

Chaque domaine suit la même structure : `models.py` (SQLAlchemy),
`schemas.py` (Pydantic, alias camelCase pour matcher le frontend),
`service.py` (logique métier), `router.py` (endpoints + dépendances de
sécurité). C'est la couche `service.py` qui décide quelle vue (client ou
commerciale) construire — jamais le frontend.

## Sécurité — points clés

- **Séparation stricte des vues** : `RobotClientResponse` ne contient
  structurellement pas les champs commerciaux (prix, stock, marges) — ce
  n'est pas un filtrage a posteriori, ces champs n'existent pas dans le
  schéma. Impossible d'en faire fuiter un par oubli.
- **RBAC par dépendance** (`require_roles(...)`) sur chaque route
  sensible ; vérifié côté serveur uniquement, indépendamment de ce
  qu'affiche ou cache le frontend.
- **Mots de passe** : bcrypt (jamais en clair, jamais journalisés),
  verrouillage de compte après 5 échecs (15 min), message d'erreur
  générique identique que l'email existe ou non (anti-énumération).
- **Sessions** : JWT d'accès courte durée en mémoire côté frontend,
  refresh token opaque en cookie `httpOnly` + `Secure` (prod) +
  `SameSite=Strict`, avec rotation à chaque refresh et révocation stockée
  en base (logout = révocation immédiate).
- **Import Excel** : validation de signature de fichier (pas seulement
  l'extension), taille et nombre de lignes plafonnés, chaque ligne validée
  avec les mêmes règles Pydantic que la création manuelle.
- **Aucune fuite de stack trace** : toute exception non prévue est
  journalisée côté serveur et renvoyée au client sous forme générique.

## Base de données partagée — préfixe des tables

La base Azure SQL est mutualisée entre plusieurs applications de
l'entreprise. Pour éviter toute collision de nom, **toutes les tables de
ce projet sont préfixées `ranmarket_`** (`ranmarket_robots`,
`ranmarket_users`, `ranmarket_devis_requests`, ...). Le préfixe est défini
une seule fois, dans `src/database.py::TABLE_PREFIX`, et repris par chaque
modèle (`__tablename__` et `ForeignKey`) — pour le changer, une seule
ligne à modifier.

## Base de données : Azure SQL Database

Le projet cible SQL Server / Azure SQL Database via le dialecte async
`mssql+aioodbc` de SQLAlchemy (aucun autre changement de code nécessaire —
les enums sont volontairement stockés en `VARCHAR` plutôt qu'en type natif,
justement pour rester portables entre SQLite/PostgreSQL/SQL Server).

### 1. Dépendances Python

```bash
pip install -r requirements.txt --break-system-packages
# (aioodbc + pyodbc sont déjà dans requirements.txt)
```

### 2. Driver ODBC système (obligatoire, pas installable via pip)

`pyodbc` s'appuie sur le gestionnaire de drivers **unixODBC** + le
**pilote ODBC Microsoft pour SQL Server**, tous deux des paquets système,
pas des paquets Python :

```bash
# Debian/Ubuntu
sudo apt-get install -y unixodbc unixodbc-dev curl gnupg
curl https://packages.microsoft.com/keys/microsoft.asc | sudo tee /etc/apt/trusted.gpg.d/microsoft.asc
curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list
sudo apt-get update
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18
```

Si le déploiement cible **Azure App Service (Linux)**, le driver ODBC 18
est déjà préinstallé sur les images Python officielles — cette étape n'est
alors nécessaire qu'en local/CI ou sur un conteneur Docker custom.

### 3. Chaîne de connexion

```
DATABASE_URL=mssql+aioodbc://<user>:<password>@<server>.database.windows.net:1433/<database>?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=no&Encrypt=yes
```

- Mot de passe à URL-encoder s'il contient des caractères spéciaux.
- `Encrypt=yes` est exigé par Azure SQL (la connexion est refusée sans TLS).
- Autoriser l'IP sortante de l'API dans le pare-feu Azure SQL (ou activer
  *"Allow Azure services and resources to access this server"* si l'API
  est elle-même hébergée sur Azure).

### 4. Particularités gérées côté code

- `pool_pre_ping=True` + `pool_recycle=1800s` : Azure ferme parfois les
  connexions inactives côté serveur : ces options détectent une connexion
  morte et la renouvellent avant qu'elle ne fasse échouer une requête.
- Les comparaisons de dates (`RefreshToken.expires_at`, verrouillage de
  compte) normalisent explicitement les datetimes "naïfs" que peuvent
  renvoyer certains drivers (`src/auth/service.py::_as_aware`) — déjà
  couvert par les tests, cohérent quel que soit le moteur SQL utilisé.

> ⚠️ Cet environnement de développement n'a pas d'accès réseau sortant vers
> Azure : la connexion end-to-end à une vraie instance Azure SQL n'a donc
> pas pu être testée ici. Le moteur SQLAlchemy a été validé (construction
> de l'engine + dialecte `mssql+aioodbc` reconnu), mais teste la connexion
> réelle (`python -m scripts.seed`) dès que tu as les identifiants Azure en
> main — dis-moi si tu rencontres une erreur, la plupart viennent du driver
> ODBC système absent ou du pare-feu Azure SQL.

## Tests

```bash
python -m pytest tests/ -v
```

28 tests couvrant : authentification et verrouillage de compte, rotation
et révocation des refresh tokens, séparation vue client/commerciale,
contrôle d'accès par rôle sur chaque domaine, import Excel (création,
doublons, fichier invalide), devis (soumission publique, assignation).

## Vers la production

- Remplacer `Base.metadata.create_all` par des migrations **Alembic**
  versionnées avant tout déploiement en production.
- Passer `DATABASE_URL` sur PostgreSQL (`postgresql+asyncpg://...`).
- Définir `ENVIRONMENT=production`, une vraie `SECRET_KEY`, et
  `COOKIE_SECURE=true` (bloqué explicitement sinon au démarrage).
- Servir derrière HTTPS uniquement (les cookies `Secure` l'exigent).
- Brancher un vrai envoi d'email pour la confirmation de devis (actuellement
  la référence est générée et renvoyée en réponse HTTP, mais aucun email
  n'est envoyé — à ajouter selon le fournisseur SMTP retenu par FANUC).
