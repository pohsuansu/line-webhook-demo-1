from flask import Flask, request
import json
import os
import requests

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "你的 Channel Access Token")

@app.route("/", methods=["GET"])
def keep_alive():
    return "✅ I am alive!", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.get_json()
    events = body.get("events", [])
    known_users = set()

    # 若已有紀錄檔，先讀入現有 userIds
    if os.path.exists("user_ids.txt"):
        with open("user_ids.txt", "r") as f:
            for line in f:
                known_users.add(line.strip())

    for event in events:
        if event["type"] == "message":
            user_id = event["source"]["userId"]
            reply_token = event["replyToken"]
            print("📩 收到訊息，使用者 ID:", user_id)

            # 回覆歡迎訊息
            send_reply(reply_token, "您的 LINE 已註冊成功，謝謝！")

            # 如果是新使用者才記錄
            if user_id not in known_users:
                with open("user_ids.txt", "a") as f:
                    f.write(user_id + "\n")
                known_users.add(user_id)

    return "OK"

def send_reply(token, message):
    url = "https://api.line.me/v2/bot/message/reply"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + CHANNEL_ACCESS_TOKEN
    }
    payload = {
        "replyToken": token,
        "messages": [{
            "type": "text",
            "text": message
        }]
    }
    requests.post(url, headers=headers, data=json.dumps(payload).encode("utf-8"))
