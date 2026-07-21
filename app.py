import os
import threading
import sys
from flask import Flask, jsonify
from bot import run_bot

app = Flask(__name__)

def start_bot():
    try:
        print("Поток бота запущен. Вызываю run_bot()...", flush=True)
        run_bot()
    except Exception as e:
        print(f"КРИТИЧЕСКАЯ ОШИБКА В БОТЕ: {e}", flush=True)
        import traceback
        traceback.print_exc(file=sys.stdout)

thread = threading.Thread(target=start_bot)
thread.daemon = True  # чтобы поток завершился при остановке Flask
thread.start()
print("Поток бота создан", flush=True)

@app.route('/')
def home():
    return jsonify({"status": "Bot is running!"})

@app.route('/health')
def health():
    return jsonify({"status": "OK"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
