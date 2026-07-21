import os
import sys
import requests
from flask import Flask, request, jsonify
from telegram import Update
from bot import application

app = Flask(__name__)

print("=== STARTING APP ===", flush=True)

TOKEN = os.environ.get("TELEGRAM_TOKEN")
print(f"TOKEN: {'set' if TOKEN else 'NOT SET'}", flush=True)
if not TOKEN:
    print("FATAL: TELEGRAM_TOKEN not set", file=sys.stderr, flush=True)
    sys.exit(1)

RENDER_EXTERNAL_URL = os.environ.get("RENDER_EXTERNAL_URL")
print(f"RENDER_EXTERNAL_URL: {RENDER_EXTERNAL_URL}", flush=True)
if not RENDER_EXTERNAL_URL:
    # fallback: попробуем использовать RENDER_SERVICE_URL или сгенерировать
    RENDER_EXTERNAL_URL = os.environ.get("RENDER_SERVICE_URL")
    if not RENDER_EXTERNAL_URL:
        print("ERROR: Cannot determine external URL", file=sys.stderr, flush=True)
        sys.exit(1)

WEBHOOK_URL = RENDER_EXTERNAL_URL + "/webhook"
print(f"WEBHOOK_URL: {WEBHOOK_URL}", flush=True)

def set_webhook():
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/setWebhook"
        response = requests.post(url, json={"url": WEBHOOK_URL})
        print(f"Webhook set response: {response.json()}", flush=True)
    except Exception as e:
        print(f"Failed to set webhook: {e}", flush=True)
        sys.exit(1)

print("Setting webhook...", flush=True)
set_webhook()
print("Webhook set successfully", flush=True)

@app.route("/webhook", methods=["POST"])
def webhook():
    print("Received update", flush=True)
    update = Update.de_json(request.get_json(), application.bot)
    application.process_update(update)
    return jsonify({"status": "ok"})

@app.route("/")
def home():
    return jsonify({"status": "Bot is running with webhook!"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting Flask on port {port}", flush=True)
    app.run(host="0.0.0.0", port=port)
