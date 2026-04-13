"""
Helpers de seguridad (API key)
"""
from fastapi import Header, HTTPException, status

from .settings import settings


def require_api_key(x_api_key: str = Header(None)) -> None:
    """
    Validar API key para endpoints sensibles.

    Si API_KEY no esta configurada, no bloquea (modo desarrollo).
    """
    expected = settings.API_KEY
    if not expected:
        if settings.ENVIRONMENT.lower() == "production":
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Security configuration error",
            )
        return

    if x_api_key != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )