from analyzer.llm_analysis import llm_analyze
import sqlite3
import os
from datetime import datetime

DB = "ai_cydece.db"
print("Using DB:", DB)
PCAP_DIR = "data/pcaps"

def extract_features(reference):
    return {
        "static_duration": True,
        "contains_http": "http" in reference.lower(),
        "automation_pattern": "capture" in reference.lower()
    }

def classify(features):
    if features["contains_http"]:
        return "Medium", "HTTP interaction detected"
    elif features["automation_pattern"]:
        return "Low", "Automated interaction pattern detected"
    else:
        return "Unknown", "Insufficient data"

conn = sqlite3.connect(DB)
cursor = conn.cursor()

# Create tables if not exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT,
    reference TEXT,
    start_time TEXT,
    end_time TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS session_analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER,
    risk_level TEXT,
    reason TEXT,
    analyzed_at TEXT
)
""")

cursor.execute("SELECT id, reference FROM sessions")

rows = cursor.fetchall()

for row in rows:
    session_id = row[0]
    reference = row[1]

    features = extract_features(reference)

    risk, rule_reason = classify(features)

    try:
        ai_reason = llm_analyze(features)
    except:
        ai_reason = "LLM unavailable"

    reason = f"Rule: {rule_reason} | LLM: {ai_reason}"

    cursor.execute("""
    INSERT INTO session_analysis (session_id, risk_level, reason, analyzed_at)
    VALUES (?, ?, ?, datetime('now'))
    """, (session_id, risk, reason))

conn.commit()
conn.close()

print("Sessions and analysis created successfully")
