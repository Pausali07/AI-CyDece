from fastapi import FastAPI
import sqlite3
import json

app = FastAPI(
    title="AI-CyDece API",
    description="Cyber Deception Analysis with Rule-Based + LLM Reasoning",
    version="1.0"
)

DB = "ai_cydece.db"

# -----------------------------
# Database Connection
# -----------------------------
def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

# -----------------------------
# Get All Sessions
# -----------------------------
@app.get("/sessions")
def get_sessions():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM sessions")
    rows = cursor.fetchall()

    result = [dict(row) for row in rows]

    conn.close()
    return result

# -----------------------------
# Get Analysis (Main Endpoint)
# -----------------------------
@app.get("/analysis")
def get_analysis():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 
        sa.session_id,
        s.reference,
        sa.risk_level,
        sa.reason,
        sa.features,
        sa.analyzed_at
    FROM session_analysis sa
    JOIN sessions s ON sa.session_id = s.id
    ORDER BY sa.session_id
    """)

    rows = cursor.fetchall()

    result = []

    for row in rows:
        # Split Rule + LLM
        reason_parts = row["reason"].split("|") if row["reason"] else []

        result.append({
            "session_id": row["session_id"],
            "reference": row["reference"],
            "risk_level": row["risk_level"],
            "features": json.loads(row["features"]) if row["features"] else {},
            "rule_reason": reason_parts[0].strip() if len(reason_parts) > 0 else "",
            "llm_reason": reason_parts[1].strip() if len(reason_parts) > 1 else "",
            "analyzed_at": row["analyzed_at"]
        })

    conn.close()
    return result
