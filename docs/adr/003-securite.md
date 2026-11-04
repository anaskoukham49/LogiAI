# ADR 003 : Sécurisation de l'API LogiAI

## Contexte
L'API REST LogiAI expose des modèles de prédiction de retard et doit être protégée contre les accès non autorisés tout en restant accessible aux clients web légitimes.

## Décisions

1. **Transmission de la clé API via l'en-tête `X-API-Key`**
   - *Choix :* Utiliser un en-tête HTTP personnalisé `X-API-Key`.
   - *Conséquence de l'autre option (dans l'URL ou le corps) :* Transmettre la clé dans l'URL l'exposerait dans les journaux du serveur (logs) et l'historique du navigateur, ce qui présente un risque critique de fuite de secrets.

2. **Restriction des origines CORS (`ALLOWED_ORIGINS`)**
   - *Choix :* Restreindre les origines autorisées à une liste précise (ex: `http://localhost:5500`).
   - *Conséquence de l'autre option (autoriser `*` pour tout le monde) :* Permettre à n'importe quel site web malveillant d'interagir directement avec l'API au nom d'un utilisateur authentifié, ouvrant la voie à des attaques de type CSRF / abus de ressources.

## Statut
Accepté et implémenté.