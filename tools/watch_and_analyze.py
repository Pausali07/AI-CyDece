import os
import time
import subprocess

LOG_DIR = os.path.expanduser("~/AI-CyDece/data/honeypot_logs")
CHECK_INTERVAL = 5  # seconds

def run_analysis(log_file):
    print(f"\n🆕 New log detected: {log_file}")
    print("➡ Running analyzer…\n")

    # Run the analyzer
    subprocess.run(
        ['/home/pausali/AI-CyDece/venv/bin/python3', "analyzer/analyze_logs.py"],
        cwd=os.path.expanduser("~/AI-CyDece"),
        check=False
    )

    # === Auto-generate charts ===
    print("📊 Generating visualizations...")
    try:
        subprocess.run(
            ['/home/pausali/AI-CyDece/venv/bin/python3', "visualization/plot_charts.py"],
            cwd=os.path.expanduser("~/AI-CyDece"),
            check=False
        )
        print("✔ Charts generated successfully.")
    except Exception as e:
        print("⚠ Chart generation failed:", e)


def rotate_logs():
    subprocess.run(
        ["/home/pausali/AI-CyDece/venv/bin/python3", "tools/log_rotate.py"],
        cwd=os.path.expanduser("~/AI-CyDece"),
        check=False
    )

def main():
    print("👁  Watching for new honeypot logs...")
    seen = set(os.listdir(LOG_DIR))

    while True:
        time.sleep(CHECK_INTERVAL)

        rotate_logs()

        now = set(os.listdir(LOG_DIR))
        new_files = now - seen

        if new_files:
            for nf in new_files:
                run_analysis(nf)

        seen = now

if __name__ == "__main__":
    main()
