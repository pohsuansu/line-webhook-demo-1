from flask import Flask, request
import json
import os
import requests

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "QuYgSEeRhgixlG463SUEPex6LYs8gyg/ww8kGLEn+elpT3uURIYdDfktgty06X4oPKQjL+9DhCR2OHORTyVcbxzTZgzY3TblmTb/x9kPolAAWh43jRhj9kRaIFJ96mHa6Elbm+HTAU+CoBOvFRdFtAdB04t89/1O/w1cDnyilFU=")

@app.route("/", methods=["GET"])
def keep_alive():
    return "✅ I am alive!", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.get_json()
    events = body.get("events", [])
    known_users = set()

    if os.path.exists("user_ids.txt"):
        with open("user_ids.txt", "r") as f:
            for line in f:
                known_users.add(line.strip())

    for event in events:
        if event["type"] == "message":
            user_id = event["source"]["userId"]
            print("📩 收到訊息，使用者 ID:", user_id)

            # 推播訊息
            message = "✅ 這是 push 測試訊息（debug 版）"
            res = push_message(user_id, message)

            print("📤 Push 狀態碼:", res.status_code)
            print("📤 Push 回應:", res.text)

            if user_id not in known_users:
                with open("user_ids.txt", "a") as f:
                    f.write(user_id + "\n")
                known_users.add(user_id)

    return "OK"

def push_message(user_id, message):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + CHANNEL_ACCESS_TOKEN
    }

    payload = {
        "to": user_id,
        "messages": [{
            "type": "text",
            "text": message
        }]
    }

    print("📤 Push Headers:")
    for k, v in headers.items():
        print(f"  {k}: {v}")

    print("📤 Push Payload:")
    print(json.dumps(payload, indent=2, ensure_ascii=False))

    return requests.post(url, headers=headers, json=payload)
