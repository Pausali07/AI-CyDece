#!/usr/bin/env python3
import json, os, glob, sqlite3
from datetime import datetime
from llm_wrapper import analyze_with_llm

LOG_DIR = os.path.expanduser("~/AI-CyDece/data/honeypot_logs")
REPORT_DIR = os.path.expanduser("~/AI-CyDece/data/reports")
DB_PATH = os.path.expanduser("~/AI-CyDece/ai_cydece.db")

os.makedirs(REPORT_DIR, exist_ok=True)

def get_latest_log():
    logs = glob.glob(os.path.join(LOG_DIR, "*.json"))
    if not logs:
        return None
    return max(logs, key=os.path.getctime)

def save_timestamped_report(analysis_text):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_path = os.path.join(REPORT_DIR, f"report_{timestamp}.txt")
    with open(report_path, "w") as f:
        f.write(analysis_text)
    print(f"\n📄 Report saved to: {report_path}\n")
    return report_path, timestamp

def extract_session_fields(log_path):
    try:
        with open(log_path, "r") as f:
            data = json.load(f)
    except:
        return None, ""
    
    src_ip = data.get("source_ip", "unknown")
    cmds = []
    for ev in data.get("events", []):
        cmd = ev.get("cmd")
        if cmd:
            cmds.append(cmd)
    return src_ip, ", ".join(cmds)

def insert_session_row(source_ip, first_seen, commands, report_path, severity=0):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""
        INSERT INTO sessions (source_ip, first_seen, commands, severity, report_path)
        VALUES (?, ?, ?, ?, ?)
    """, (source_ip, first_seen, commands, severity, report_path))
    con.commit()
    con.close()

def main():
    latest_log = get_latest_log()
    if not latest_log:
        print("No logs found.")
        return

    print(f"Analyzing latest log: {latest_log}\n")
    with open(latest_log, "r") as f:
        log_data = f.read()

    print("🧠 Sending data to LLM for analysis...\n")
    analysis = analyze_with_llm(log_data)

    print("\n═══ AI Analysis ═══\n")
    print(analysis)

    report_path, timestamp = save_timestamped_report(analysis)

    # Extract details from JSON log
    src_ip, cmd_str = extract_session_fields(latest_log)

    insert_session_row(src_ip, timestamp, cmd_str, report_path)
    print("🗄 Stored session metadata into SQLite.")

if __name__ == "__main__":
    main()
