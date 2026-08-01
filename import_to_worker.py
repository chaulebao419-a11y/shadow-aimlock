import json, urllib.request

WORKER_URL = "https://aimlock-key-bot.chaulebao419.workers.dev/import"
IMPORT_TOKEN = "ALB-2026-RESERVE-x9f2k7"

with open("bot_keys.json", "r", encoding="utf-8") as f:
    keys = json.load(f)

body = json.dumps({"token": IMPORT_TOKEN, "keys": keys}).encode()
req = urllib.request.Request(WORKER_URL, data=body, headers={
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36",
})
with urllib.request.urlopen(req, timeout=120) as r:
    print(r.read().decode())
