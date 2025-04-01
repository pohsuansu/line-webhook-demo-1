from flask import Flask, request
import json

app = Flask(__name__)
@app.route("/", methods=["GET"])
def keep_alive():
    return "✅ I am alive!", 200


@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.get_json()
    events = body.get("events", [])
    for event in events:
        if event["type"] == "message":
            user_id = event["source"]["userId"]
            print("📩 收到訊息，使用者 ID:", user_id)
            with open("user_ids.txt", "a") as f:
                f.write(user_id + "\n")
    return "OK"
