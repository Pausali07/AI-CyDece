import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load the API key from .env
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("❌ OpenAI API key not found. Please set it in .env")

# Initialize client
client = OpenAI(api_key=openai_api_key)

def analyze_with_llm(prompt: str) -> str:

    prompt = f"""
You are a senior Cyber Threat Intelligence (CTI) analyst.

Analyze the following honeypot log data and provide a full cybersecurity report with these sections:

### 1. Attack Summary
### 2. Attacker Intent
### 3. Technique Breakdown
### 4. MITRE ATT&CK Mapping
### 5. Severity Score (1–10)
### 6. Recommended Defense Actions

Here is the honeypot log data:

{prompt}

Provide a structured cybersecurity analysis in clear Markdown.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a cybersecurity analysis assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ LLM Analysis Error: {e}"
