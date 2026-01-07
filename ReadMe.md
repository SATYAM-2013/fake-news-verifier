📰 Fake News Verification System



Hybrid AI + Fact-Check Engine (FAANG-Style Project)



📌 Overview



The Fake News Verification System is a production-grade hybrid AI platform that verifies news claims by combining:



Transformer-based Machine Learning (DistilBERT)



Authoritative Fact-Check APIs



Deterministic Decision Logic



Explainability \& Confidence Scoring



Unlike traditional fake-news detectors that rely only on ML predictions, this system prioritizes verifiable evidence and handles uncertainty safely.



🚨 Problem Statement



Fake news detection is inherently difficult because:



ML models do not understand truth, only language patterns



Fact-check sources do not exist for every claim



High ML confidence ≠ factual correctness



Most existing systems:



Over-trust ML predictions



Fail silently when evidence is missing



Give misleading binary answers



✅ Solution Approach (Why This Project Is Different)



This project uses a Hybrid Decision Engine:



Layer	Responsibility

ML Model	Detect linguistic misinformation patterns

Fact-Check API	Verify real-world claims

Decision Engine	Combine both safely

Explainability	Justify every verdict



Rule:



Verified evidence always overrides AI suspicion.



🧠 System Architecture

User Input (Claim)

        │

        ▼

ML Predictor (DistilBERT)

        │

        ▼

Fact-Check Service (Google Fact Check API)

        │

        ▼

Decision Engine (Rule-based)

        │

        ▼

Final Verdict + Explanation



⚙️ Core Components

1️⃣ ML Predictor



Model: distilbert-base-uncased-finetuned-sst-2-english



Role:



Detects misleading language patterns



Outputs label + confidence



Guarantees:



No per-request reload



Deterministic output



2️⃣ Fact-Check Service



API: Google Fact Check Tools API



Trusted publishers only:



WHO



CDC



Reuters



AP News



BBC



FullFact



AFP Fact Check



Output:



supports, contradicts, mixed, none



3️⃣ Decision Engine (Critical Logic)



Priority Order



✅ Fact-check evidence



🤖 High-confidence AI



⚠️ Uncertain fallback



Example Rules



Fact-check contradicts → Fake News



Fact-check supports → Likely True News



Medical claim + no evidence → Fake News



Low confidence + no evidence → Uncertain



This logic is fully unit-tested.



🧪 Testing Strategy



pytest based testing



Covers:



Medical claims



High-confidence AI cases



Conflicting signals



No-evidence scenarios



✔️ All tests pass deterministically



🔌 API Interface (FastAPI)

Endpoint

POST /verify



Request

{

  "text": "WHO says COVID vaccines do not cause infertility"

}



Response

{

  "verdict": "Likely True News",

  "confidence": 0.85,

  "ml\_label": "real",

  "sources": \[

    "https://fullfact.org/health/vaccine-infertility/"

  ],

  "reason": "Verified fact-check sources support this claim."

}





📖 Interactive docs available at:



http://127.0.0.1:8000/docs



🖥️ User Interface (Streamlit)



Clean, minimal UI



Displays:



Final verdict



AI confidence bar



Explanation



Fact-check sources



Includes history tracking



🔍 Explainability



Every verdict is accompanied by:



ML label



Confidence score



Evidence presence



Clear reasoning



This satisfies Responsible AI \& Trust requirements.



🚀 Performance \& Scalability



Model loaded once per process



Stateless API design



Cache-friendly architecture



Docker-ready (optional)



⚠️ Limitations



Not all claims have fact-check coverage



ML confidence is probabilistic, not truth



API rate limits apply



🛡️ Design Principles (FAANG-Level)



Fail-safe defaults



Evidence > AI



Deterministic decisions



Test-driven logic



Explainability by design



🧩 Tech Stack

Layer	Technology

ML	HuggingFace Transformers

Backend	FastAPI

UI	Streamlit

Testing	Pytest

Env Mgmt	python-dotenv

Deployment	Docker (optional)

📈 Resume Impact (Why This Is FAANG-Level)



This project demonstrates:



System design thinking



Hybrid AI architecture



Responsible ML usage



API engineering



Test-driven development



Real-world constraints handling



💡 This is NOT a toy project.

It matches how real misinformation systems are built in industry.



🏁 How to Run

\# Activate virtual environment

source .venv/bin/activate



\# Run API

uvicorn api:app --reload



\# Run UI

streamlit run app.py



\# Run tests

pytest



📜 Disclaimer



This system assists in misinformation detection.

Always verify critical information using trusted news organizations.



⭐ Final Note



This project is intentionally designed to be:



Explainable



Auditable



Extendable



Interview-ready

