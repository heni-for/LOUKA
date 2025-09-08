import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TOKEN_CACHE_FILE = PROJECT_ROOT / "assistant" / ".token_cache.bin"

MS_CLIENT_ID = os.getenv("MS_CLIENT_ID", "")
MS_TENANT_ID = os.getenv("MS_TENANT_ID", "common")
MS_AUTH_MODE = os.getenv("MS_AUTH_MODE", "device")
MS_SCOPES = [
    "https://graph.microsoft.com/Mail.Read",
    "https://graph.microsoft.com/Mail.ReadWrite",
    "offline_access",
    "openid",
    "profile",
]

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "")
DEFAULT_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
