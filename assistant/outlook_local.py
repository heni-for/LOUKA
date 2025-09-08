from __future__ import annotations

from typing import List, Optional

import win32com.client


def _get_outlook():
	# Dispatch Outlook application
	return win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")


def list_inbox(top: int = 10) -> List[dict]:
	"""Return a list of recent inbox messages using local Outlook MAPI."""
	ns = _get_outlook()
	inbox = ns.GetDefaultFolder(6)  # 6 = olFolderInbox
	items = inbox.Items
	items.Sort("[ReceivedTime]", True)
	messages = []
	for i, item in enumerate(items):
		if i >= top:
			break
		try:
			messages.append({
				"entry_id": item.EntryID,
				"subject": item.Subject or "",
				"sender": getattr(item, "SenderEmailAddress", ""),
				"received": str(getattr(item, "ReceivedTime", "")),
				"unread": bool(getattr(item, "UnRead", False)),
			})
		except Exception:
			continue
	return messages


def get_message(entry_id: str) -> dict:
	"""Get full message by EntryID."""
	ns = _get_outlook()
	item = ns.GetItemFromID(entry_id)
	body = getattr(item, "Body", "") or getattr(item, "HTMLBody", "")
	return {
		"entry_id": entry_id,
		"subject": item.Subject or "",
		"sender": getattr(item, "SenderEmailAddress", ""),
		"body": body,
	}


def ensure_folder(display_name: str):
	"""Ensure or create a mail folder at root level."""
	ns = _get_outlook()
	root = ns.GetDefaultFolder(6).Parent  # Inbox's parent store
	for f in root.Folders:
		if f.Name == display_name:
			return f
	return root.Folders.Add(display_name)


def move_to_folder(entry_id: str, folder_name: str) -> None:
	ns = _get_outlook()
	item = ns.GetItemFromID(entry_id)
	folder = ensure_folder(folder_name)
	item.Move(folder)


def create_draft(to: str, subject: str, body: str, display_only: bool = True) -> None:
	"""Create a draft email in Outlook. If display_only is True, open the window; else save in Drafts."""
	app = win32com.client.Dispatch("Outlook.Application")
	mail = app.CreateItem(0)  # olMailItem
	mail.To = to
	mail.Subject = subject
	mail.Body = body
	if display_only:
		mail.Display(False)
	else:
		mail.Save()
