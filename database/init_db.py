import sqlite3

DB_PATH = "ai_cydece.db"

con = sqlite3.connect(DB_PATH)
cur = con.cursor()

# Honeypot + LLM sessions
cur.execute("""
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_ip TEXT,
    first_seen TEXT,
    commands TEXT,
    severity INTEGER,
    report_path TEXT
)
""")

# PCAP metadata (already used by pcap_ingest.py but safe to keep here too)
cur.execute("""
CREATE TABLE IF NOT EXISTS pcap_metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pcap_file TEXT,
    packet_count INTEGER,
    first_ts TEXT,
    last_ts TEXT
)
""")

con.commit()
con.close()
print("DB initialized.")
