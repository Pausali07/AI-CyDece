from analyzer.llm_analysis import llm_analyze
import sqlite3
import os
import json
from datetime import datetime

DB = "ai_cydece.db"
PCAP_DIR = "data/pcaps"

# -----------------------------
# Feature Extraction
# -----------------------------
def extract_features(reference):
    return {
        "static_duration": True,
        "contains_http": "http" in reference.lower(),
        "automation_pattern": "capture" in reference.lower()
    }

# -----------------------------
# Rule-based Classification
# -----------------------------
def classify(features):
    if features["contains_http"]:
        return "Medium", "HTTP interaction detected"
    elif features["automation_pattern"]:
        return "Low", "Automated interaction pattern detected"
    else:
        return "Unknown", "Insufficient indicators for classification"

# -----------------------------
# Database Connection
# -----------------------------
conn = sqlite3.connect(DB)
cursor = conn.cursor()

# -----------------------------
# Create Tables
# -----------------------------
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
    features TEXT,
    analyzed_at TEXT
)
""")

# -----------------------------
# Fetch Sessions
# -----------------------------
cursor.execute("SELECT id, reference FROM sessions")
rows = cursor.fetchall()

# -----------------------------
# Process Each Session
# -----------------------------
for row in rows:
    session_id = row[0]
    reference = row[1]

    features = extract_features(reference)

    # Rule-based
    risk, rule_reason = classify(features)

    # LLM reasoning
    try:
        ai_reason = llm_analyze(features)
    except Exception:
        ai_reason = "LLM reasoning unavailable"

    # Combine
    reason = f"Rule: {rule_reason} | LLM: {ai_reason}"

    # Insert into DB
    cursor.execute("""
    INSERT INTO session_analysis (session_id, risk_level, reason, features, analyzed_at)
    VALUES (?, ?, ?, ?, datetime('now'))
    """, (session_id, risk, reason, json.dumps(features)))

# -----------------------------
# Save & Close
# -----------------------------
conn.commit()
conn.close()

print("✅ Sessions analyzed successfully with features + LLM")
