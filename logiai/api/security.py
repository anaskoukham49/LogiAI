"""Gestion de l'authentification et de la sécurité par clé API."""

import secrets
from fastapi import Depends, Header, HTTPException
from logiai import config


def _egal(a: str | None, b: str | None) -> bool:
    """Compare deux chaînes de manière sécurisée contre les attaques temporelles."""
    if not a or not b:
        return False
    return secrets.compare_digest(a.encode("utf-8"), b.encode("utf-8"))


def verify_api_key(x_api_key: str | None = Header(default=None)) -> str:
    """Vérifie l'en-tête X-API-Key et retourne le rôle ('admin' ou 'user')."""
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Clé API manquante")

    if config.ADMIN_KEY and _egal(x_api_key, config.ADMIN_KEY):
        return "admin"
    if config.API_KEY and _egal(x_api_key, config.API_KEY):
        return "user"

    raise HTTPException(status_code=401, detail="Clé API invalide")


def require_admin(role: str = Depends(verify_api_key)) -> str:
    """Vérifie que l'utilisateur authentifié possède le rôle 'admin' (sinon 403)."""
    if role != "admin":
        raise HTTPException(
            status_code=403, detail="Accès réservé à l'administrateur"
        )
    return role