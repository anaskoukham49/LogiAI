
# COMPTE RENDU TECHNIQUE
## Conteneurisation et déploiement de l'application LogiAI avec Docker

**Étudiant :** Anas Koukham  
**Projet :** LogiAI  
**Sujet :** Déploiement avec Docker, Docker Compose et Nginx  
**Date :** Novembre 2026

---

## 1. Introduction

Ce compte rendu présente le travail réalisé pour conteneuriser et déployer l'application LogiAI à l'aide de Docker.

L'objectif est de faciliter l'exécution de l'application en séparant ses principaux composants dans deux conteneurs indépendants :

- **Backend :** développé avec FastAPI, il assure le traitement des requêtes et les prédictions du modèle de Machine Learning.
- **Frontend :** servi par Nginx, il permet aux utilisateurs d'accéder à l'interface web.

La configuration permet également d'accéder à l'application depuis un autre appareil connecté au même réseau local.

## 2. Architecture de l'application

L'application repose sur une architecture composée de deux services :

- **FastAPI :** expose les endpoints de l'API et exécute les opérations de prédiction.
- **Nginx :** distribue les fichiers du frontend et joue le rôle de reverse proxy pour transmettre les requêtes API au backend.

Les deux services communiquent à travers le réseau interne créé automatiquement par Docker Compose.

### Figure 1 – Architecture générale de LogiAI

<!-- INSÉRER LA CAPTURE : schéma de l'architecture -->

![Architecture LogiAI](screenshots/01-architecture.png)

## 3. Configuration Docker

### 3.1. Conteneurisation du backend

Un fichier `Dockerfile` a été créé à la racine du projet à partir de l'image Python 3.11.

Il permet de :

- Installer les dépendances définies dans `requirements.txt`.
- Copier les fichiers nécessaires au fonctionnement de l'application.
- Démarrer le serveur FastAPI avec Uvicorn.
- Exposer le port 8000 à l'intérieur du conteneur.

### Figure 2 – Dockerfile du backend

<!-- INSÉRER LA CAPTURE DU DOCKERFILE PRINCIPAL -->

![Dockerfile backend](screenshots/02-backend-dockerfile.png)

### 3.2. Conteneurisation du frontend

Le frontend utilise l'image officielle `nginx:alpine`.

Le fichier `web/Dockerfile` permet de copier :
- Le fichier HTML de l'interface.
- La configuration Nginx personnalisée.

Le serveur Nginx écoute sur le port 80 à l'intérieur du conteneur.

### Figure 3 – Dockerfile du frontend

<!-- INSÉRER LA CAPTURE DE web/Dockerfile -->

![Dockerfile frontend](screenshots/03-frontend-dockerfile.png)

### 3.3. Configuration Nginx et reverse proxy

Nginx assure deux fonctions principales :

1. Servir l'interface web.
2. Transférer les requêtes commençant par `/api/` vers le backend FastAPI.

Le backend est accessible depuis Nginx grâce au nom du service Docker `api`.

Cette configuration permet au frontend d'utiliser une URL relative, comme `/api/v1/predict`, sans avoir à définir directement l'adresse interne du backend.

### Figure 4 – Configuration Nginx

<!-- INSÉRER LA CAPTURE DE nginx/default.conf -->

![Configuration Nginx](screenshots/04-nginx-config.png)

### 3.4. Orchestration avec Docker Compose

Le fichier `docker-compose.yml` permet de gérer les deux services dans un environnement commun.

Configuration des ports :

| Service | Port du conteneur | Port de la machine |
|---|---:|---:|
| Backend FastAPI | 8000 | 8001 |
| Frontend Nginx | 80 | 8080 |

Le fichier comprend également :

- Un contrôle de santé (*health check*) pour le backend.
- Une dépendance entre le frontend et le backend.
- La configuration des variables d'environnement.
- Le montage des dossiers `models` et `data` dans le conteneur backend.

Les clés API et autres informations sensibles sont fournies à travers les variables d'environnement et ne doivent pas être publiées dans le dépôt Git.

### Figure 5 – Configuration Docker Compose

<!-- INSÉRER LA CAPTURE DE docker-compose.yml -->

![Docker Compose](screenshots/05-docker-compose.png)

## 4. Construction et démarrage des conteneurs

La commande suivante permet de construire les images et de démarrer les services en arrière-plan :

```powershell
docker compose up --build -d
```

Pour vérifier l'état des conteneurs :

```powershell
docker compose ps
```

Après le démarrage, les résultats obtenus étaient :

- `logiai-api` : état `healthy`.
- `logiai-web` : état `running`.

Le backend était accessible sur le port 8001 et le frontend sur le port 8080 de la machine hôte.

### Figure 6 – État des conteneurs Docker

<!-- INSÉRER LA CAPTURE DE docker compose ps -->

![État des conteneurs](screenshots/06-docker-compose-ps.png)

## 5. Tests fonctionnels

### 5.1. Accès à l'interface web

Après le démarrage des conteneurs, l'application a été ouverte depuis le navigateur à l'adresse :

`http://localhost:8080`

Cette vérification permet de confirmer que le frontend est correctement servi par Nginx.

### Figure 7 – Interface LogiAI en local

<!-- INSÉRER UNE CAPTURE DE L'APPLICATION DANS LE NAVIGATEUR -->

![Interface LogiAI](screenshots/07-application-local.png)

### 5.2. Vérification du backend

Le backend expose une route `/health` permettant de vérifier son état de fonctionnement.

La réponse obtenue confirmait :

- Le fonctionnement du service.
- Le chargement du modèle de Machine Learning.
- La configuration de l'authentification.

### Figure 8 – Vérification de l'API

<!-- INSÉRER LA CAPTURE DE LA RÉPONSE /health -->

![API Health Check](screenshots/08-api-health.png)

## 6. Accès depuis un autre appareil du réseau local

Afin de permettre l'accès depuis un autre appareil, l'adresse IP locale de la machine hébergeant les conteneurs a été utilisée à la place de `localhost`.

Lors du test, l'adresse utilisée était :

`http://172.20.10.2:8080`

Une règle entrante du pare-feu Windows a été créée afin d'autoriser les connexions TCP au port 8080 depuis le sous-réseau local.

L'application a ensuite été ouverte avec succès depuis un deuxième appareil connecté au même réseau Wi-Fi.

### Figure 9 – Accès depuis un autre appareil

<!-- INSÉRER UNE CAPTURE DE L'APPLICATION SUR LE DEUXIÈME APPAREIL -->

![Accès réseau local](screenshots/09-acces-autre-appareil.png)

**Remarque :** l'adresse IP utilisée est privée et peut changer selon le réseau auquel la machine est connectée. Cette méthode permet un accès sur le réseau local, mais ne rend pas automatiquement l'application accessible depuis Internet.

## 7. Gestion du code source avec Git et GitHub

Les modifications relatives au déploiement ont été regroupées dans une branche Git dédiée :

`feature/docker-deployment`

Un commit a été créé avec le message :

`Add Docker deployment configuration sans compte rendu`

La branche a ensuite été publiée sur GitHub.

- **Dépôt :** https://github.com/anaskoukham49/LogiAI
- **Branche :** https://github.com/anaskoukham49/LogiAI/tree/feature/docker-deployment
- **Commit :** `d37d2d9`

Cette organisation permet de séparer les modifications du déploiement de la branche principale.

### Figure 10 – Publication de la branche sur GitHub

<!-- INSÉRER UNE CAPTURE DE LA BRANCHE GITHUB -->

![Branche GitHub](screenshots/10-github-branch.png)

## 8. Conclusion

Ce travail a permis de mettre en place un environnement de déploiement Docker pour l'application LogiAI en séparant le backend FastAPI et le frontend Nginx.

Docker Compose facilite la construction, le démarrage et la gestion des deux services. La configuration Nginx assure la distribution de l'interface web ainsi que le transfert des requêtes API vers le backend.

Les tests réalisés ont confirmé le bon fonctionnement des conteneurs, l'accès à l'interface web et l'accessibilité de l'application depuis un autre appareil connecté au même réseau local.

Cette configuration constitue une base reproductible pour exécuter l'application dans un environnement conteneurisé.

## Annexe – Commandes utilisées

```powershell
# Construire et démarrer les conteneurs
docker compose up --build -d

# Vérifier les conteneurs
docker compose ps

# Consulter les journaux
docker compose logs

# Arrêter les conteneurs
docker compose down

# Vérifier la branche Git
git branch --show-current

# Publier la branche sur GitHub
git push -u origin feature/docker-deployment
```

---

## Liste des captures d'écran à ajouter

Créer un dossier `screenshots` à la racine du projet et y placer les images suivantes :

| Nom du fichier | Contenu |
|---|---|
| `01-architecture.png` | Schéma de l'architecture |
| `02-backend-dockerfile.png` | Dockerfile backend |
| `03-frontend-dockerfile.png` | Dockerfile frontend |
| `04-nginx-config.png` | Configuration Nginx |
| `05-docker-compose.png` | Configuration Docker Compose |
| `06-docker-compose-ps.png` | État des conteneurs |
| `07-application-local.png` | Interface dans le navigateur |
| `08-api-health.png` | Vérification de l'API |
| `09-acces-autre-appareil.png` | Accès depuis un autre appareil |
| `10-github-branch.png` | Branche GitHub publiée |

**Consigne de sécurité :** ne jamais inclure le fichier `.env`, les clés API ou d'autres informations confidentielles dans les captures d'écran.
