import json
import requests
from pathlib import Path

API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "xiaomi/mimo-v2-flash:free"

SYSTEM_PROMPT = """
You are M2H AI, created by M2H Web Solution.

Expertise:
- Web Development
- APIs & Backend
- Cyber Security & Defense
- Automation & DevOps

Be concise, practical, and production-ready.
"""

CONFIG_FILE = Path.home() / ".m2h-ai" / "config.json"


def get_api_key():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            return json.load(f).get("api_key")
    return None


def ask_ai(prompt: str) -> str:
    api_key = get_api_key()
    if not api_key:
        return "❌ No API key found. Restart the CLI."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://m2hgamerz.site",
        "X-Title": "M2H AI CLI"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    r = requests.post(API_URL, headers=headers, json=payload, timeout=60)

    if r.status_code != 200:
        return f"API Error: {r.text}"

    return r.json()["choices"][0]["message"]["content"]
