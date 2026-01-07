#!/usr/bin/env python3
import json
import matplotlib.pyplot as plt
from pathlib import Path
import os

LOG_DIR = Path.home() / "AI-CyDece" / "data" / "honeypot_logs"
OUT_DIR = Path.home() / "AI-CyDece" / "visualizations"
OUT_DIR.mkdir(exist_ok=True)

def load_logs():
    logs = []
    for file in LOG_DIR.glob("*.json"):
        with open(file) as f:
            logs.append(json.load(f))
    return logs

def plot_ip_frequency(logs):
    ips = [log.get("source_ip", "unknown") for log in logs]
    ip_counts = {ip: ips.count(ip) for ip in set(ips)}

    plt.figure(figsize=(8, 5))
    plt.bar(ip_counts.keys(), ip_counts.values())
    plt.title("Attack Frequency by Source IP")
    plt.xlabel("Source IP")
    plt.ylabel("Number of Attacks")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(OUT_DIR / "ip_frequency.png")
    plt.close()

def plot_command_usage(logs):
    commands = []
    for log in logs:
        for event in log.get("events", []):
            commands.append(event.get("cmd", ""))

    cmd_counts = {c: commands.count(c) for c in set(commands)}

    plt.figure(figsize=(10, 5))
    plt.barh(list(cmd_counts.keys()), list(cmd_counts.values()))
    plt.title("Frequency of Commands Executed")
    plt.xlabel("Count")
    plt.tight_layout()
    plt.savefig(OUT_DIR / "command_usage.png")
    plt.close()

def main():
    logs = load_logs()
    plot_ip_frequency(logs)
    plot_command_usage(logs)
    print("✔ Charts saved inside visualization/")

if __name__ == "__main__":
    main()
