import os
import threading
from flask import Flask, jsonify
from bot import run_bot

app = Flask(__name__)

def start_bot():
    run_bot()

threading.Thread(target=start_bot).start()

@app.route('/')
def home():
    return jsonify({"status": "Bot is running!"})

@app.route('/health')
def health():
    return jsonify({"status": "OK"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
