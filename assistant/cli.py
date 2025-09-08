from __future__ import annotations

import sys
from rich import print
from rich.table import Table

from .auth import get_access_token
from .graph import list_inbox_messages, get_message as get_msg_graph, ensure_folder as ensure_folder_graph, move_message as move_message_graph
from .tts import speak
from .llm import summarize_email, categorize_email, draft_email
from .outlook_local import list_inbox as list_inbox_local, get_message as get_msg_local, move_to_folder as move_local, create_draft as create_draft_local


def login() -> None:
	"""Sign in using device code and cache the token (Graph mode)."""
	# Access token fetch triggers device code flow internally
	_ = get_access_token()
	print("[green]Login successful.[/green]")


def inbox(top: int = 10, mode: str = "local") -> None:
	"""List recent inbox messages. mode: local | graph"""
	if mode == "graph":
		token = get_access_token()
		msgs = list_inbox_messages(token, top=top)
		table = Table(title="Inbox (Graph)")
		for m in msgs:
			mid = m.get("id", "")
			frm = m.get("from", {}).get("emailAddress", {}).get("address", "")
			sub = m.get("subject", "")
			is_read = "Yes" if m.get("isRead") else "No"
			if len(table.columns) == 0:
				table.add_column("ID", overflow="fold", max_width=20)
				table.add_column("From")
				table.add_column("Subject")
				table.add_column("Read")
			table.add_row(mid, frm, sub, is_read)
		print(table)
	else:
		msgs = list_inbox_local(top=top)
		table = Table(title="Inbox (Local Outlook)")
		table.add_column("EntryID", overflow="fold", max_width=20)
		table.add_column("From")
		table.add_column("Subject")
		table.add_column("Unread")
		for m in msgs:
			mid = m.get("entry_id", "")
			frm = m.get("sender", "")
			sub = m.get("subject", "")
			is_read = "No" if m.get("unread") else "Yes"
			table.add_row(mid, frm, sub, is_read)
		print(table)


def read_message(message_id: str, speak_out: bool = True, mode: str = "local") -> None:
	"""Fetch and read a message; optionally speak it aloud."""
	if mode == "graph":
		token = get_access_token()
		msg = get_msg_graph(token, message_id)
		subject = msg.get("subject", "(no subject)")
		body = msg.get("body", {}).get("content", "")
	else:
		msg = get_msg_local(message_id)
		subject = msg.get("subject", "(no subject)")
		body = msg.get("body", "")
	print(f"[bold]Subject:[/bold] {subject}")
	print()
	print(body)
	if speak_out:
		speak(f"Subject: {subject}")
		summary = summarize_email(subject, body)
		speak(f"Summary: {summary}")


def organize(dry_run: bool = True, mode: str = "local") -> None:
	"""Categorize a few inbox emails and optionally move them into folders."""
	if mode == "graph":
		token = get_access_token()
		msgs = list_inbox_messages(token, top=10)
		folders = {}
		for m in msgs:
			mid = m.get("id")
			subject = m.get("subject", "")
			full = get_msg_graph(token, mid)
			body_text = full.get("bodyPreview", "") or full.get("body", {}).get("content", "")
			category = categorize_email(subject, body_text)
			print(f"[cyan]{subject}[/cyan] -> {category}")
			if not dry_run:
				folder_name = category
				if folder_name not in folders:
					f = ensure_folder_graph(token, folder_name)
					folders[folder_name] = f.get("id")
				move_message_graph(token, mid, folders[folder_name])
				print(f"Moved to {folder_name}")
	else:
		msgs = list_inbox_local(top=10)
		for m in msgs:
			mid = m.get("entry_id")
			subject = m.get("subject", "")
			full = get_msg_local(mid)
			body_text = full.get("body", "")
			category = categorize_email(subject, body_text)
			print(f"[cyan]{subject}[/cyan] -> {category}")
			if not dry_run:
				move_local(mid, category)
				print(f"Moved to {category}")


def draft(prompt: str, to: str = "", display_only: bool = True, mode: str = "local") -> None:
	"""Generate an email draft from a prompt and open in Outlook."""
	text = draft_email(prompt)
	if mode == "graph":
		print("Draft (Graph mode):\n")
		print(text)
	else:
		subject = "Draft: " + prompt[:60]
		create_draft_local(to=to, subject=subject, body=text, display_only=display_only)
		print("Opened a draft in Outlook.")


def main():
	"""Main CLI entry point."""
	if len(sys.argv) < 2:
		print("Usage: python -m assistant.cli <command> [args]")
		print("Commands: login, inbox, read, organize, draft")
		return
	
	command = sys.argv[1]
	
	if command == "login":
		login()
	elif command == "inbox":
		top = int(sys.argv[2]) if len(sys.argv) > 2 else 10
		mode = sys.argv[3] if len(sys.argv) > 3 else "local"
		inbox(top, mode)
	elif command == "read":
		if len(sys.argv) < 3:
			print("Usage: python -m assistant.cli read <id> [local|graph]")
			return
		message_id = sys.argv[2]
		mode = sys.argv[3] if len(sys.argv) > 3 else "local"
		read_message(message_id, True, mode)
	elif command == "organize":
		mode = sys.argv[2] if len(sys.argv) > 2 else "local"
		organize(True, mode)
	elif command == "draft":
		if len(sys.argv) < 3:
			print("Usage: python -m assistant.cli draft <prompt> [to_email]")
			return
		prompt = " ".join(sys.argv[2:])
		to = ""
		create_draft = True
		draft(prompt, to, True, "local")
	else:
		print(f"Unknown command: {command}")
		print("Commands: login, inbox, read, organize, draft")


if __name__ == "__main__":
	main()
