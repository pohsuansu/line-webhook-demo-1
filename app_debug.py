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

    if os.path.exists("user_ids.txt"):
        with open("user_ids.txt", "r") as f:
            for line in f:
                known_users.add(line.strip())

    for event in events:
        if event["type"] == "message":
            user_id = event["source"]["userId"]
            reply_token = event["replyToken"]
            print("📩 收到訊息，使用者 ID:", user_id)
            print("🔁 回傳用的 replyToken:", reply_token)

            # 回覆訊息
            res = send_reply(reply_token, "✅ 這是 debug 測試訊息：你已註冊成功！")
            print("🔁 回覆狀態碼:", res.status_code)
            print("📩 回覆內容:", res.text)

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

    # 顯示 headers（檢查 token 是否有非 ASCII 字元）
    print("📦 Headers:")
    for k, v in headers.items():
        try:
            v.encode('latin-1')
        except Exception as e:
            print(f"⚠️ Header {k} 非法字元: {e}")
        print(f"  {k}: {v}")

    payload = {
        "replyToken": token,
        "messages": [{
            "type": "text",
            "text": message
        }]
    }

    return requests.post(url, headers=headers, json=payload)
