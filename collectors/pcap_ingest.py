from pathlib import Path
import sqlite3
from datetime import datetime

PCAP_DIR = Path("data/pcaps")
DB_PATH = "ai_cydece.db"


def ensure_db():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS pcap_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pcap_file TEXT,
            ingested_at TEXT,
            source TEXT
        )
    """)
    con.commit()
    con.close()


def ingest_pcap(pcap_path: Path):
    metadata = {
        "pcap_file": pcap_path.name,
        "ingested_at": datetime.now().isoformat(timespec="seconds"),
        "source": "pcap"
    }

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Insert into pcap_metadata
    cur.execute(
        """
        INSERT INTO pcap_metadata (pcap_file, ingested_at, source)
        VALUES (?, ?, ?)
        """,
        (
            metadata["pcap_file"],
            metadata["ingested_at"],
            metadata["source"]
        )
    )

    # Insert ONE logical session per PCAP
    cur.execute(
        """
        INSERT INTO sessions (source, reference, start_time, end_time)
        VALUES (?, ?, ?, ?)
        """,
        (
            "pcap",
            pcap_path.name,
            metadata["ingested_at"],
            metadata["ingested_at"]
        )
    )

    conn.commit()
    conn.close()

    print(f"[+] Ingested metadata for {pcap_path.name}")



def main():
    ensure_db()

    for pcap in PCAP_DIR.glob("*.pcap"):
        ingest_pcap(pcap)


if __name__ == "__main__":
    main()
