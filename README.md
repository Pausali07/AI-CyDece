# 🛡️ AI-CyDece: AI-Based Cyber Deception Framework

## 📌 Overview
AI-CyDece is a cyber deception framework that uses a honeypot to capture attacker interactions and convert raw network data into structured cybersecurity intelligence.

It combines **rule-based risk classification** with **LLM-based reasoning** to provide both detection and human-readable explanations of attacker behavior.

---

## 🎯 Objectives
- Capture attacker activity using a honeypot  
- Convert raw PCAP data into structured sessions  
- Extract behavioral features  
- Perform risk classification  
- Generate explanations using LLM  

---

## ⚙️ Technologies Used
- Python  
- Docker (Honeypot)  
- SQLite  
- FastAPI (Swagger UI)  
- LLM Integration  

---

## 📁 Project Structure
AI-CyDece/
├── analyzer/
├── collectors/
├── api/
├── data/pcaps/
├── docker-compose.yml
├── ai_cydece.db

## 🚀 How to Run

### 1. Start Honeypot
```bash
docker-compose up -d

### 2. Ingest PCAP Data
'''bash
python3 collectors/pcap_ingest.py

### 3. Run Analysis (Rule + LLM)
'''bash
python3 -m analyzer.session_summary

### 4. Start API
'''bash
uvicorn api.main:app --reload
Open in browser:
http://127.0.0.1:8000/docs

## Sample Output

'''1 | Low | Rule: Automated interaction detected | LLM: Indicates scanning behavior
2 | Medium | Rule: HTTP interaction detected | LLM: Suggests probing activity

## Key Features

'''- Session-based attacker behavior analysis  
- Rule-based risk classification  
- LLM-based explanation generation  
- Structured data storage (SQLite)  
- API-based result access (FastAPI)

## Role of LLM

'''The LLM enhances the system by:
- Providing human-readable explanations  
- Interpreting attacker behavior patterns  
- Improving understanding of raw security data  
- Supporting explainable cybersecurity analysis  

## Future Scope

'''- Multi-protocol honeypots (HTTP, FTP)  
- Advanced LLM-based threat reasoning  
- Real-time monitoring dashboard  
- Cloud deployment  
- Integration with SIEM tools  

## Conclusion

'''This project demonstrates how cyber deception combined with AI and LLMs can transform raw attacker interaction data into structured and interpretable cybersecurity insights.
