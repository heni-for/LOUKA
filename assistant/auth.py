from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import msal

from .config import MS_CLIENT_ID, MS_TENANT_ID, MS_SCOPES, TOKEN_CACHE_FILE


class TokenStore:
	def __init__(self, path: Path) -> None:
		self.path = path
		self.path.parent.mkdir(parents=True, exist_ok=True)

	def load(self) -> Optional[msal.SerializableTokenCache]:
		cache = msal.SerializableTokenCache()
		if self.path.exists():
			cache.deserialize(self.path.read_text(encoding="utf-8"))
		return cache

	def save(self, cache: msal.SerializableTokenCache) -> None:
		if cache.has_state_changed:
			self.path.write_text(cache.serialize(), encoding="utf-8")


def _build_app(cache: msal.SerializableTokenCache) -> msal.PublicClientApplication:
	authority = f"https://login.microsoftonline.com/{MS_TENANT_ID}"
	return msal.PublicClientApplication(client_id=MS_CLIENT_ID, authority=authority, token_cache=cache)


def acquire_token_interactive() -> dict:
	store = TokenStore(TOKEN_CACHE_FILE)
	cache = store.load()
	app = _build_app(cache)

	result = app.acquire_token_interactive(scopes=MS_SCOPES)
	store.save(cache)
	return result


def acquire_token_device_code() -> dict:
	store = TokenStore(TOKEN_CACHE_FILE)
	cache = store.load()
	app = _build_app(cache)

	flow = app.initiate_device_flow(scopes=MS_SCOPES)
	if "user_code" not in flow:
		raise RuntimeError("Failed to create device flow. Check client ID and network.")
	print(f"To sign in, visit {flow['verification_uri']} and enter code: {flow['user_code']}")
	result = app.acquire_token_by_device_flow(flow)
	store.save(cache)
	return result


def acquire_token_silent() -> Optional[dict]:
	store = TokenStore(TOKEN_CACHE_FILE)
	cache = store.load()
	app = _build_app(cache)
	a_accounts = app.get_accounts()
	if a_accounts:
		result = app.acquire_token_silent(scopes=MS_SCOPES, account=a_accounts[0])
		store.save(cache)
		return result
	return None


def get_access_token() -> str:
	result = acquire_token_silent()
	if not result:
		# Default to device code for simplicity
		result = acquire_token_device_code()
	if "access_token" not in result:
		raise RuntimeError(f"Auth failed: {result.get('error_description', 'unknown error')}")
	return result["access_token"]
