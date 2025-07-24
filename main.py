#!/usr/bin/env python3
import os, urllib.request, urllib.parse, json, ssl, time

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("Set env var BOT_TOKEN")

API = f"https://api.telegram.org/bot{TOKEN}"

BANNER = r"""
 ____        _   _                 _       _   _             
|  _ \ _   _| |_| |__   ___  _ __ (_) __ _| |_(_) ___  _ __  
| |_) | | | | __| '_ \ / _ \| '_ \| |/ _` | __| |/ _ \| '_ \ 
|  __/| |_| | |_| | | | (_) | | | | | (_| | |_| | (_) | | | |
|_|    \__, |\__|_| |_|\___/|_| |_|_|\__,_|\__|_|\___/|_| |_|
       |___/                                                 
"""

print(BANNER)

def tg(method, payload=None):
    data = json.dumps(payload).encode() if payload else None
    req = urllib.request.Request(f"{API}/{method}", data=data)
    req.add_header("Content-Type", "application/json")
    return json.loads(urllib.request.urlopen(req, context=ssl.create_default_context()).read())

def main():
    offset = 0
    while True:
        try:
            updates = tg("getUpdates", {"offset": offset, "timeout": 30})
            for u in updates["result"]:
                offset = u["update_id"] + 1
                msg = u.get("message", {})
                if msg.get("text", "").strip() == "/start":
                    chat_id = msg["chat"]["id"]
                    tg("sendMessage", {"chat_id": chat_id, "text": "hello"})
        except Exception as e:
            print("Error:", e)
            time.sleep(1)

if __name__ == "__main__":
    main()
