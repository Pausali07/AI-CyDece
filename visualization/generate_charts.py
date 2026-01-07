#!/usr/bin/env python3
"""
generate_charts.py
Reads text reports in data/reports/ (report_YYYY-MM-DD_HH-MM-SS.txt)
and creates charts in data/reports/charts/
Requires: pandas, matplotlib
"""
import os, re, json
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime

REPORT_DIR = Path.home() / "AI-CyDece" / "data" / "reports"
CHART_DIR = REPORT_DIR / "charts"
CHART_DIR.mkdir(parents=True, exist_ok=True)

def parse_report_text(path):
    # naive parsing: tries to extract Severity and Commands
    text = path.read_text()
    # find severity like "Severity: 4/10" or "Severity Score (1–10): 4"
    sev = None
    m = re.search(r"Severity[: ]+([0-9]{1,2})", text)
    if m: sev = int(m.group(1))
    # find commands (lines that look like command names or `ls`, `whoami`...)
    cmds = re.findall(r"`([^`]{1,200})`", text)  # backtick-enclosed commands if any
    # fallback: look for words after "Commands:" line
    if not cmds:
        m = re.search(r"Commands[:\s]*(.*)", text)
        if m:
            cmdline = m.group(1).strip()
            cmds = [c.strip() for c in re.split(r'[,\|;]', cmdline) if c.strip()]
    # timestamp from filename
    ts = None
    try:
        name = path.stem  # report_YYYY-MM-DD_HH-MM-SS
        ts_str = name.replace("report_", "")
        ts = datetime.strptime(ts_str, "%Y-%m-%d_%H-%M-%S")
    except Exception:
        ts = None
    return {"path": str(path), "severity": sev or 0, "commands": cmds, "timestamp": ts}

def build_dataframe():
    files = sorted(REPORT_DIR.glob("report_*.txt"))
    rows = [parse_report_text(p) for p in files]
    if not rows:
        print("No reports found in", REPORT_DIR)
        return None
    df = pd.DataFrame(rows)
    return df

def plot_severity_over_time(df):
    df = df.dropna(subset=["timestamp"])
    if df.empty:
        print("No timestamps found for severity plot.")
        return
    plt.figure(figsize=(8,4))
    plt.plot(df['timestamp'], df['severity'], marker='o', linestyle='-')
    plt.xlabel('Time')
    plt.ylabel('Severity')
    plt.title('Severity Over Time')
    plt.xticks(rotation=25)
    plt.tight_layout()
    out = CHART_DIR / "severity_over_time.png"
    plt.savefig(out)
    plt.close()
    print("Saved", out)

def plot_top_commands(df):
    all_cmds = []
    for cmds in df['commands'].tolist():
        if isinstance(cmds, list):
            all_cmds.extend(cmds)
    if not all_cmds:
        print("No commands found for top-commands plot.")
        return
    c = Counter(all_cmds)
    top = c.most_common(10)
    names = [x[0] for x in top]
    counts = [x[1] for x in top]
    plt.figure(figsize=(8,4))
    plt.barh(names[::-1], counts[::-1])
    plt.xlabel('Count')
    plt.title('Top Commands')
    plt.tight_layout()
    out = CHART_DIR / "top_commands.png"
    plt.savefig(out)
    plt.close()
    print("Saved", out)

def plot_attack_counts(df):
    df2 = df.copy()
    df2['date'] = df2['timestamp'].dt.date
    counts = df2.groupby('date').size() if 'timestamp' in df2.columns else None
    if counts is None or counts.empty:
        print("No date counts for attack frequency.")
        return
    plt.figure(figsize=(8,3))
    counts.plot(kind='bar')
    plt.xlabel('Date')
    plt.ylabel('Number of Reports')
    plt.title('Attack Frequency by Date')
    plt.tight_layout()
    out = CHART_DIR / "attack_frequency.png"
    plt.savefig(out)
    plt.close()
    print("Saved", out)

def build_charts():
    df = build_dataframe()
    if df is None:
        return
    plot_severity_over_time(df)
    plot_top_commands(df)
    plot_attack_counts(df)
    print("Charts generated in", CHART_DIR)

if __name__ == "__main__":
    build_charts()
