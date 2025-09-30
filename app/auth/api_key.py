# app/auth/api_key.py
import os
from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv, find_dotenv

# Carrega o .env da raiz
load_dotenv(find_dotenv())

API_KEY_HEADER_NAME = "Api-Key"
api_key_scheme = APIKeyHeader(name=API_KEY_HEADER_NAME, auto_error=False)

def _get_api_key() -> str | None:
    key = os.getenv("API_KEY")
    if key is not None:
        key = key.strip()
    return key

def require_api_key(provided: str = Security(api_key_scheme)) -> str:
    configured = _get_api_key()
    if not configured:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API key is not configured on the server.",
        )
    if provided == configured:
        return provided
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API key.",
    )
