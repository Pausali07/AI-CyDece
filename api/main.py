from fastapi import FastAPI
import sqlite3

app = FastAPI()

DB_PATH = "ai_cydece.db"

@app.get("/")
def home():
    return {"message": "AI-CyDeception API is running"}

@app.get("/analysis")
def get_analysis():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT session_id, risk_level, reason
        FROM session_analysis
    """)

    rows = cursor.fetchall()
    conn.close()

    result = []
    for row in rows:
        result.append({
            "session_id": row[0],
            "risk": row[1],
            "reason": row[2]
        })

    return result
