import sqlite3
import json
from datetime import datetime

from analyzer.behavior_features import extract_behavior_features
from analyzer.risk_scoring import assign_risk_score

DB_PATH = "ai_cydece.db"


def summarize_sessions():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    cur.execute("""
        SELECT id, source, reference, start_time, end_time
        FROM sessions
    """)

    summaries = []

    for row in cur.fetchall():
        session = dict(row)

        # 1. Extract features
        features = extract_behavior_features(session)

        # 2. Assign risk
        risk = assign_risk_score(features)

        risk_level = risk["risk_level"]
        reason = risk["reason"]

        # 3. Persist analysis (idempotent)
        cur.execute("""
            SELECT 1 FROM session_analysis WHERE session_id = ?
        """, (session["id"],))

        if not cur.fetchone():
            cur.execute("""
                INSERT INTO session_analysis
                (session_id, features, risk_level, reason, analyzed_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                session["id"],
                json.dumps(features),
                risk_level,
                reason,
                datetime.utcnow().isoformat(timespec="seconds")
            ))

        # 4. API output
        session["features"] = features
        session["risk_level"] = {
            "risk_level": risk_level,
            "reason": reason
        }

        summaries.append(session)

    con.commit()
    con.close()
    return summaries


if __name__ == "__main__":
    for s in summarize_sessions():
        print(s)
