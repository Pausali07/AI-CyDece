import os
import shutil
import time
from datetime import datetime, timedelta

LOG_DIR = os.path.expanduser("~/AI-CyDece/data/honeypot_logs")
ARCHIVE_DIR = os.path.expanduser("~/AI-CyDece/data/archive_logs")

os.makedirs(ARCHIVE_DIR, exist_ok=True)

RETENTION_DAYS = 7

def rotate_logs():
    cutoff = datetime.now() - timedelta(days=RETENTION_DAYS)

    for filename in os.listdir(LOG_DIR):
        file_path = os.path.join(LOG_DIR, filename)
        if not filename.endswith(".json"):
            continue

        file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))

        if file_mtime < cutoff:
            print(f"📦 Archiving old log: {filename}")
            shutil.move(file_path, os.path.join(ARCHIVE_DIR, filename))

    print("✔ Log rotation check complete.\n")

if __name__ == "__main__":
    rotate_logs()
