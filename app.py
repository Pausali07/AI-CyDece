from flask import Flask
import logging
import os

# Ensure log directory exists
os.makedirs("logs", exist_ok=True)

# Configure Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(filename="logs/honeypot.log", level=logging.INFO,
                    format="%(asctime)s - %(message)s")

@app.route('/')
def index():
    logging.info("Connection attempt detected!")
    return "This is a fake SSH honeypot service. Your actions are being logged."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=22)
