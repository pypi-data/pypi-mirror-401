from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests

from daisy_sdk.utils import DEFAULT_TOKEN_PATH, read_toml, write_toml

SUPABASE_URL = "https://hspktpexpqzhqidtwnaq.supabase.co"
SUPABASE_ANON_KEY = "sb_publishable_FUQr2cDzXf-2kl5q9RF7cQ_ZNTsrS20"


@dataclass
class TokenData:
    access_token: str
    refresh_token: str
    expires_at: int | None = None
    token_type: str | None = None


def _extract_auth(raw: dict[str, Any]) -> tuple[dict[str, Any], bool]:
    auth = raw.get("auth")
    if isinstance(auth, dict):
        return auth, True
    return raw, False


def _parse_tokens(raw: dict[str, Any]) -> tuple[TokenData, bool] | None:
    data, nested = _extract_auth(raw)
    access_token = data.get("access_token")
    refresh_token = data.get("refresh_token")
    if not access_token or not refresh_token:
        return None
    return (
        TokenData(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=data.get("expires_at"),
            token_type=data.get("token_type"),
        ),
        nested,
    )


def _write_tokens(tokens: TokenData, *, nested: bool) -> None:
    payload = {
        "access_token": tokens.access_token,
        "refresh_token": tokens.refresh_token,
    }
    if tokens.expires_at is not None:
        payload["expires_at"] = tokens.expires_at
    if tokens.token_type is not None:
        payload["token_type"] = tokens.token_type
    data = {"auth": payload} if nested else payload
    write_toml(DEFAULT_TOKEN_PATH, data)


def _validate_access_token(access_token: str) -> bool:
    url = f"{SUPABASE_URL}/auth/v1/user"
    headers = {
        "Content-Type": "application/json",
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {access_token}",
    }
    response = requests.get(url, headers=headers, timeout=30)
    if response.status_code == 200:
        return True
    if response.status_code in (401, 403):
        return False
    raise RuntimeError(
        f"Token validation failed: {response.status_code} {response.text.strip()}"
    )


def _refresh_tokens(refresh_token: str) -> TokenData:
    print("Access token invalid or expired. Refreshing...")
    url = f"{SUPABASE_URL}/auth/v1/token?grant_type=refresh_token"

    headers = {
        "Content-Type": "application/json",
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {refresh_token}",
    }
    response = requests.post(url, json={"refresh_token": refresh_token}, headers=headers, timeout=30)
    if not response.ok:
        raise RuntimeError(
            f"Token refresh failed: {response.status_code} {response.text.strip()}"
        )

    data = response.json()
    access_token = data.get("access_token")
    new_refresh_token = data.get("refresh_token", refresh_token)
    if not access_token:
        raise RuntimeError("Token refresh response missing access_token")

    tokens = TokenData(
        access_token=access_token,
        refresh_token=new_refresh_token,
        expires_at=data.get("expires_at"),
        token_type=data.get("token_type"),
    )
    return tokens


def get_valid_access_token() -> str:
    print("Validating access token...")
    raw = read_toml(DEFAULT_TOKEN_PATH)
    parsed = _parse_tokens(raw)
    if not parsed:
        raise RuntimeError(
            f"Missing tokens in {DEFAULT_TOKEN_PATH}. Expected access_token and refresh_token."
        )
    tokens, nested = parsed

    if _validate_access_token(tokens.access_token):
        print("Access token is valid.")
        return tokens.access_token

    tokens = _refresh_tokens(tokens.refresh_token)
    _write_tokens(tokens, nested=nested)
    print("Token refresh complete.")
    return tokens.access_token
