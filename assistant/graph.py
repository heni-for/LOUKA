from __future__ import annotations

import requests
from typing import Dict, List, Optional

GRAPH_BASE = "https://graph.microsoft.com/v1.0"


def _headers(token: str) -> Dict[str, str]:
	return {
		"Authorization": f"Bearer {token}",
		"Accept": "application/json",
	}


def list_inbox_messages(token: str, top: int = 10) -> List[dict]:
	url = f"{GRAPH_BASE}/me/mailFolders/Inbox/messages?$top={top}&$select=id,subject,from,receivedDateTime,bodyPreview,isRead"
	r = requests.get(url, headers=_headers(token), timeout=60)
	r.raise_for_status()
	return r.json().get("value", [])


def get_message(token: str, message_id: str) -> dict:
	url = f"{GRAPH_BASE}/me/messages/{message_id}"
	r = requests.get(url, headers=_headers(token), timeout=60)
	r.raise_for_status()
	return r.json()


def _get_mail_folders(token: str) -> List[dict]:
	url = f"{GRAPH_BASE}/me/mailFolders"
	r = requests.get(url, headers=_headers(token), timeout=60)
	r.raise_for_status()
	return r.json().get("value", [])


def ensure_folder(token: str, display_name: str) -> dict:
	folders = _get_mail_folders(token)
	for f in folders:
		if f.get("displayName") == display_name:
			return f
	# create
	url = f"{GRAPH_BASE}/me/mailFolders"
	r = requests.post(url, headers=_headers(token), json={"displayName": display_name}, timeout=60)
	r.raise_for_status()
	return r.json()


def move_message(token: str, message_id: str, dest_folder_id: str) -> dict:
	url = f"{GRAPH_BASE}/me/messages/{message_id}/move"
	r = requests.post(url, headers=_headers(token), json={"destinationId": dest_folder_id}, timeout=60)
	r.raise_for_status()
	return r.json()
