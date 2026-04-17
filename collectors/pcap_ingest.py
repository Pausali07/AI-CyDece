import os
import sqlite3
from datetime import datetime

PCAP_DIR = "data/pcaps"
DB = "ai_cydece.db"
print("Using DB:", DB)

conn = sqlite3.connect(DB)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT,
    reference TEXT,
    start_time TEXT,
    end_time TEXT
)
""")

for file in os.listdir(PCAP_DIR):
    start = datetime.now()
    end = datetime.now()

    cursor.execute("""
    INSERT INTO sessions (source, reference, start_time, end_time)
    VALUES (?, ?, ?, ?)
    """, ("pcap", file, start, end))

    print(f"[+] Ingested metadata for {file}")

conn.commit()
conn.close()
