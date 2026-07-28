import os, threading, logging
from flask import Flask, jsonify

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

web_app = Flask(__name__)

@web_app.route("/")
def home():
    return jsonify({"status": "ok", "bot": "running"})

@web_app.route("/health")
def health():
    return jsonify({"status": "ok"})

def run_bot():
    try:
        from aimlock_bot import main as bot_main
        bot_main()
    except Exception as e:
        logger.error(f"Bot error: {e}")

threading.Thread(target=run_bot, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host="0.0.0.0", port=port)
