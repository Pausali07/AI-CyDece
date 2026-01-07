from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse
import sqlite3
import os
import json

from analyzer.session_summary import summarize_sessions

# -------------------------
# Database
# -------------------------
DB_PATH = "ai_cydece.db"

def query(sql):
    """Run SQL query and return rows as dictionaries."""
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(sql)
    rows = [dict(row) for row in cur.fetchall()]
    con.close()
    return rows


# -------------------------
# FastAPI App
# -------------------------
app = FastAPI(title="AI-CyDece API")

@app.get("/sessions/summary")
def get_session_summaries():
    return summarize_sessions()

@app.get("/analysis")
def get_session_analysis():
    sql = """
    SELECT
        s.id as session_id,
        s.reference,
        a.features,
        a.risk_level,
        a.reason,
        a.analyzed_at
    FROM session_analysis a
    JOIN sessions s ON a.session_id = s.id
    ORDER BY a.analyzed_at DESC
    """
    rows = query(sql)

    # Convert stored JSON string back to dict
    for r in rows:
        if r.get("features"):
            r["features"] = json.loads(r["features"])

    return rows

@app.get("/analysis/summary")
def get_analysis_summary():
    sql = """
    SELECT
        COUNT(*) as total,
        SUM(CASE WHEN risk_level = 'low' THEN 1 ELSE 0 END) as low,
        SUM(CASE WHEN risk_level = 'medium' THEN 1 ELSE 0 END) as medium,
        SUM(CASE WHEN risk_level = 'high' THEN 1 ELSE 0 END) as high,
        SUM(CASE WHEN risk_level = 'unknown' THEN 1 ELSE 0 END) as unknown
    FROM session_analysis
    """

    rows = query(sql)

    # rows[0] because aggregation returns single row
    summary = rows[0]

    return {
        "total_sessions": summary["total"],
        "low": summary["low"],
        "medium": summary["medium"],
        "high": summary["high"],
        "unknown": summary["unknown"]
    }


# -------------------------
# Static Files Setup
# -------------------------
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

# Ensure /api/static exists
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

# Mount the static directory for UI + icons
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# -------------------------
# Favicon
# -------------------------
@app.get("/favicon.ico")
async def favicon():
    """Serve favicon to prevent browser 404 spam."""
    return FileResponse(os.path.join(STATIC_DIR, "favicon.ico"))


# -------------------------
# API Endpoints
# -------------------------

@app.get("/")
def index():
    """Landing route for testing."""
    return {"message": "AI-CyDece API is running!"}


@app.get("/sessions")
def get_sessions():
    """Return list of honeypot sessions."""
    return query("SELECT * FROM sessions ORDER BY id DESC")


@app.get("/pcaps")
def get_pcaps():
    """Return metadata for all PCAP files."""
    return query("SELECT * FROM pcap_metadata ORDER BY id DESC")


@app.get("/reports")
def get_reports():
    """Return generated AI reports (optional future expansion)."""
    return query("SELECT * FROM reports ORDER BY id DESC")


# -------------------------
# Optional Test HTML Page
# -------------------------
@app.get("/test", response_class=HTMLResponse)
def test_page():
    """Simple browser test page."""
    html = """
    <html>
    <head>
        <title>AI-CyDece Test</title>
        <link rel="icon" href="/favicon.ico">
    </head>
    <body style="font-family: Arial; background:#111; color:#eee; padding:20px;">
        <h1>API is working 🎉</h1>
        <p>Try:</p>
        <ul>
            <li><a href="/sessions" style="color:#0af">/sessions</a></li>
            <li><a href="/pcaps" style="color:#0af">/pcaps</a></li>
        </ul>
    </body>
    </html>
    """
    return HTMLResponse(html)
