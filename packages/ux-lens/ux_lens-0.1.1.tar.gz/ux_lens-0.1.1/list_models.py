from google import genai
import os
from pathlib import Path

config_path = Path.home() / ".ux-watcher" / "config"
api_key = None
if config_path.exists():
    for line in config_path.read_text().splitlines():
        if line.startswith("GEMINI_API_KEY="):
            api_key = line.split("=", 1)[1].strip()
            break
api_key = api_key or os.getenv("GEMINI_API_KEY")

if not api_key:
    print("No API key")
    exit(1)

client = genai.Client(api_key=api_key)
for m in client.models.list():
    if "gemini" in m.name.lower():
        print(m.name)
