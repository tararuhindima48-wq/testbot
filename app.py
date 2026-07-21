import os
import requests
from flask import Flask, request, jsonify
from telegram import Update
from bot import application

app = Flask(__name__)

# Устанавливаем вебхук при старте
TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_TOKEN не установлен")

WEBHOOK_URL = os.environ.get("RENDER_EXTERNAL_URL") + "/webhook"
# Если RENDER_EXTERNAL_URL нет (локально), используем ngrok или localhost
if not WEBHOOK_URL or "localhost" in WEBHOOK_URL:
    WEBHOOK_URL = "https://your-ngrok-url.ngrok.io/webhook"  # для локального теста

def set_webhook():
    url = f"https://api.telegram.org/bot{TOKEN}/setWebhook"
    response = requests.post(url, json={"url": WEBHOOK_URL})
    print(f"Webhook set: {response.json()}")

set_webhook()

@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(), application.bot)
    application.process_update(update)
    return jsonify({"status": "ok"})

@app.route("/")
def home():
    return jsonify({"status": "Bot is running with webhook!"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
