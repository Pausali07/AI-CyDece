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
│ ├── session_summary.py
│ ├── llm_analysis.py
│
├── collectors/
│ ├── pcap_ingest.py
│
├── api/
│ ├── main.py
│
├── data/
│ └── pcaps/
│
├── docker-compose.yml
├── ai_cydece.db

---

## 🚀 How to Run

Follow the steps below to execute the complete cyber deception pipeline from data collection to analysis and visualization:

🔹 Step 1: Start the Honeypot Environment

Initialize the honeypot and packet capture services using Docker. This will simulate a vulnerable system to capture attacker interactions.

docker-compose up -d

🔹 Step 2: Ingest PCAP Data

Process the captured network traffic (PCAP files) and store session-level metadata in the database.

python3 collectors/pcap_ingest.py

🔹 Step 3: Perform Analysis (Rule-Based + LLM)

Analyze the ingested sessions by extracting behavioral features, classifying risk levels using rule-based logic, and generating explanations using an LLM.

python3 -m analyzer.session_summary

🔹 Step 4: Start the API Server

Launch the FastAPI server to expose the processed data and analysis results through REST endpoints.

uvicorn api.main:app --reload

🔹 Step 5: Access the API Interface

Open the interactive Swagger UI in your browser to view and test the available endpoints.

http://127.0.0.1:8000/docs

---

## 🔮 Future Scope

This project can be further enhanced in multiple directions:

-Extend support to multi-protocol honeypots such as HTTP, FTP, and IoT-based systems
-Integrate more advanced LLM models for deeper behavioral and intent analysis
-Develop a real-time monitoring dashboard for live attack visualization
-Deploy the system in cloud environments for scalability and accessibility
-Integrate with SIEM platforms for enterprise-level security monitoring

---

## 📌 Conclusion

This project demonstrates how cyber deception, when combined with artificial intelligence and large language models, can transform raw attacker interaction data into structured, interpretable, and actionable cybersecurity insights. By combining rule-based detection with LLM-driven reasoning, the system enhances both analytical accuracy and explainability, making it highly relevant for modern security analysis and research.
