# AI-Powered Cyber Deception Framework (AICyDece)
Smart honeypots that engage attackers and automatically generate analysis reports using LLMs.

## Overview
This project aims to build an AI-driven deception environment that:
- Captures attacker interactions (SSH/HTTP/IoT honeypots)
- Uses LLMs to analyze behaviors and generate automated cyber intelligence reports
- Presents insights via a dashboard

## Tech Stack
Python 3.11+, Docker, Zeek, FastAPI, LLM API (OpenAI/local)

### 📘 Documentation
- [Project Scope](docs/project_scope.md)
- [Architecture](docs/architecture.md)
- [Ethical & Legal Considerations](docs/ethical_legal.md)

## Known Issues

⚠️ Zeek log persistence to host volumes may vary across environments.  
Zeek execution and PCAP parsing were validated; log export is pending refinement.
- Zeek log export is pending refinement; current validation focuses on PCAP ingestion and session abstraction


### PCAP Processing Scope
- PCAP metadata ingestion is implemented and validated
- Current implementation focuses on file-level metadata (filename, timestamps, source)
- Full Zeek log correlation and export are planned for later refinement

## Session Abstraction & Analysis

- Raw PCAP files are ingested and normalized into logical security sessions
- Each session represents a high-level interaction derived from network traffic
- Session summaries are exposed via a REST API endpoint (`/sessions/summary`)
- This abstraction layer enables future behavioral analysis and AI/LLM-based threat interpretation

### Session Analysis Storage
The analysis layer persists derived intelligence separately from raw telemetry to support auditability and future ML workflows.

- Introduced a dedicated `session_analysis` table
- Stores extracted behavioral features, computed risk level, and reasoning per session
- Enables persistent and reproducible analysis independent of raw PCAP files

### Analysis & Evaluation Layer
- Session-level behavioral features are extracted without deep packet inspection
- Risk levels are assigned using deterministic rules
- Analysis results are stored in a dedicated `session_analysis` table
- Read-only APIs expose both detailed analysis (`/analysis`) and aggregated metrics (`/analysis/summary`)
- This enables reproducible, explainable, and auditable security analysis

