# Database Schema – AI-CyDece

This document describes the SQLite database schema used in the AI-CyDece project.

---

## 1. pcap_metadata

Stores file-level metadata for ingested PCAP files.

| Column        | Type    | Description |
|--------------|---------|-------------|
| id           | INTEGER | Primary key |
| pcap_file    | TEXT    | PCAP filename |
| ingested_at  | TEXT    | Ingestion timestamp |
| source       | TEXT    | Data source (pcap) |

---

## 2. sessions

Represents a logical security session derived from PCAPs or honeypot activity.

| Column      | Type    | Description |
|------------|---------|-------------|
| id         | INTEGER | Primary key |
| source     | TEXT    | pcap / honeypot |
| reference  | TEXT    | PCAP filename or session ID |
| start_time | TEXT    | Session start time |
| end_time   | TEXT    | Session end time |

---

## Notes

- PCAPs are first ingested into `pcap_metadata`
- Each PCAP is also mapped to a logical session in `sessions`
- Future versions will link Zeek logs and honeypot transcripts to sessions
