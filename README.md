# Outlook AI Assistant (Windows)

A simple Siri-like assistant to organize your Outlook email with Microsoft Graph, read messages aloud, and generate example email drafts with an LLM.

## Features
- Login via Microsoft account (Device Code Flow)
- List and read your inbox emails
- Summarize and categorize emails with AI
- Move emails to folders (e.g., Archive, Important)
- Text-to-Speech to read an email aloud (Windows SAPI5)
- Draft example emails and replies via LLM
- Voice assistant with wake word ("hey luca") for hands-free control

## Prerequisites
- Windows 10/11 with Python 3.10+
- A Microsoft account with Outlook/Exchange Online
- Azure App Registration (to access Microsoft Graph)
- Optional: OpenAI API key (or Azure OpenAI) for drafting/summarization

## Quick Start

1) Create and activate a virtual environment (recommended)

```powershell
cd C:\Users\Heni2\luca
py -3.11 -m venv .venv
. .venv\Scripts\Activate.ps1
```

2) Install dependencies

```powershell
pip install -r requirements.txt
```

3) Register an Azure AD app
- Go to Azure Portal → App registrations → New registration
- Name: Outlook AIAssistant (any name)
- Supported account types: Accounts in any organizational directory and personal Microsoft accounts
- Redirect URI: Public client/native (mobile & desktop) → `http://localhost`
- After creating, copy the Application (client) ID
- API Permissions → Add a permission → Microsoft Graph → Delegated
  - Mail.Read
  - Mail.ReadWrite
  - offline_access
  - openid, profile (usually included)
- Click Grant admin consent if available (for work/school); for personal accounts, consent at login

4) Configure environment

Create a `.env` file in the project root:

```env
MS_CLIENT_ID=your_client_id_here
MS_TENANT_ID=common
MS_AUTH_MODE=device
# Optional LLM provider (OpenAI or Azure OpenAI)
OPENAI_API_KEY=sk-...
# If using Azure OpenAI instead of OpenAI:
# AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
# AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
```

5) Local Outlook mode (no Azure)
- You can use the assistant with the Outlook desktop app without Graph.
- Commands add a `mode` parameter where applicable, defaulting to `local`.

6) Run examples

```powershell
# List inbox (local Outlook mode)
python -m assistant.cli inbox
# Read a message by EntryID
python -m assistant.cli read <EntryID>
# Organize (dry-run)
python -m assistant.cli organize
# Draft with AI and open in Outlook
python -m assistant.cli draft "Ask for a project update for client ABC"
```

## Voice Assistant (wake word: "hey luca")

1) Download a Vosk model (offline speech-to-text):
- `vosk-model-small-en-us-0.15` from `https://alphacephei.com/vosk/models`
- Unzip the folder into the project root so the path is `vosk-model-small-en-us-0.15`

2) Start the voice assistant
```powershell
python -m assistant.voice
```
- Say: "hey luca" then commands like:
  - "inbox"
  - "read <EntryID>"
  - "organize"
  - "draft follow up with client about timeline"

## Notes
- Tokens are cached locally in `assistant/.token_cache.bin`.
- The assistant uses device-code flow by default so there is no secret stored.
- TTS uses `pyttsx3` with SAPI5 voices available on Windows.

## Uninstall / Clean up
```powershell
Remove-Item .venv -Recurse -Force
Remove-Item assistant\.token_cache.bin -Force -ErrorAction SilentlyContinue
```
