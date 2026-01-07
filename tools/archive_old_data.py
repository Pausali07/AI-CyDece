import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path

# Paths
BASE_DIR = Path.home() / "AI-CyDece"
LOG_DIR = BASE_DIR / "data" / "honeypot_logs"
PCAP_DIR = BASE_DIR / "data" / "pcaps"
REPORT_DIR = BASE_DIR / "data" / "reports"
ARCHIVE_DIR = BASE_DIR / "archive"

# Create archive directory if not exists
ARCHIVE_DIR.mkdir(exist_ok=True)

# Files older than 1 day
THRESHOLD = datetime.now() - timedelta(days=1)

def archive_folder(src_dir, folder_name):
    """Archive files older than 1 day."""
    print(f"[+] Checking {folder_name} for files to archive...")

    for file in src_dir.iterdir():
        if file.is_file():
            mtime = datetime.fromtimestamp(file.stat().st_mtime)
            if mtime < THRESHOLD:
                archive_subdir = ARCHIVE_DIR / folder_name
                archive_subdir.mkdir(exist_ok=True)

                dest = archive_subdir / file.name

                print(f"[→] Archiving {file} → {dest}")
                shutil.move(str(file), str(dest))


def compress_archives():
    """Compress archive folder daily."""
    zip_path = ARCHIVE_DIR / f"archive_{datetime.now().strftime('%Y-%m-%d')}.zip"
    print(f"[+] Compressing archive to {zip_path} ...")
    shutil.make_archive(str(zip_path).replace(".zip", ""), "zip", ARCHIVE_DIR)


def main():
    print("\n=== Daily Archive Job Running ===\n")

    archive_folder(LOG_DIR, "logs")
    archive_folder(PCAP_DIR, "pcaps")
    archive_folder(REPORT_DIR, "reports")

    compress_archives()

    print("\n[✓] Archive complete.\n")


if __name__ == "__main__":
    main()
