#!/usr/bin/env python3
"""
parse_transcripts.py
- Pretty-print the latest transcript
- Extract credentials to data/creds.csv (timestamp, session_id, peer, username, password)
- Produce redacted JSON copies (password replaced with "<REDACTED>" and a password_hash)
"""

import json, csv, os, sys, hashlib
from glob import glob
from pathlib import Path

BASE = Path.home() / "AI-CyDece"
LOGDIR = BASE / "data" / "honeypot_logs"
OUTCSV = BASE / "data" / "creds.csv"
REDACTED_DIR = LOGDIR / "redacted"
REDACTED_DIR.mkdir(parents=True, exist_ok=True)

def list_transcripts():
    files = sorted(LOGDIR.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    return files

def pretty_print(file_path):
    with open(file_path, 'r') as f:
        obj = json.load(f)
    print(json.dumps(obj, indent=2))

def extract_creds(all_files, outcsv=OUTCSV):
    rows = []
    for p in all_files:
        try:
            obj = json.load(open(p))
        except Exception as e:
            print("skip", p.name, ":", e); continue
        sid = obj.get("id", p.stem)
        peer = obj.get("peer", "")
        for cred in obj.get("creds", []):
            rows.append({
                "session_id": sid,
                "peer": peer,
                "ts": cred.get("ts",""),
                "username": cred.get("username",""),
                "password": cred.get("password","")
            })
    if rows:
        with open(outcsv, "w", newline="") as csvf:
            writer = csv.DictWriter(csvf, fieldnames=["session_id","peer","ts","username","password"])
            writer.writeheader()
            writer.writerows(rows)
        print(f"Wrote {len(rows)} credential rows to {outcsv}")
    else:
        print("No credentials found in transcripts.")

def create_redacted(all_files):
    for p in all_files:
        try:
            obj = json.load(open(p))
        except Exception as e:
            print("skip redaction", p.name, e); continue
        if "creds" in obj:
            for c in obj["creds"]:
                pwd = c.get("password", "")
                if pwd:
                    h = hashlib.sha256(pwd.encode("utf-8")).hexdigest()
                    c["password_hash"] = h
                c["password"] = "<REDACTED>"
        out = REDACTED_DIR / p.name
        with open(out, "w") as f:
            json.dump(obj, f, indent=2)
    print("Redacted copies written to", REDACTED_DIR)

if __name__ == "__main__":
    files = list_transcripts()
    if not files:
        print("No transcript JSON files found in", LOGDIR); sys.exit(1)

    latest = files[0]
    print("=== Latest transcript:", latest.name, "===\n")
    try:
        pretty_print(latest)
    except Exception as e:
        print("Could not pretty print:", e)

    extract_creds(files)
    create_redacted(files)
