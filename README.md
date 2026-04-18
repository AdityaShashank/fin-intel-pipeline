# 📈 Financial Signal Intelligence (FSI)
### Autonomous MLOps Pipeline | Real-time Market Sentiment | Scalable Architecture

[![Pipeline Status](https://github.com/YOUR_USERNAME/fin-intel-pipeline/actions/workflows/main.yml/badge.svg)](https://github.com/YOUR_USERNAME/fin-intel-pipeline/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)

FSI is a production-grade intelligence system designed to bridge the gap between raw financial news and actionable market signals. Built for high-concurrency (100+ users), this autonomous pipeline ingests, analyzes, and broadcasts market-moving insights using domain-specific AI.

---

## 🏗️ System Architecture



The system is designed with a **Producer-Consumer** architecture to ensure scalability:
1. **The Producer:** An idempotent ingestion engine (Python/Pydantic) that scrapes financial news.
2. **The Brain:** A domain-specific NLP layer using **FinBERT** for sentiment and **Groq (Llama 3.3)** for narrative summarization.
3. **The Warehouse:** A scalable **PostgreSQL (Supabase)** instance with connection pooling for 100+ users.
4. **The Broadcaster:** Real-time data delivery via **WebSockets** for zero-latency updates.

---

## 🌟 Key Engineering Features

* **High-Concurrency Design:** Optimized to handle 100+ concurrent users using **Supavisor connection pooling**, preventing database bottlenecks during peak market hours.
* **Domain-Specific NLP:** Leverages **FinBERT**, a model pre-trained on financial corpora, ensuring accurate sentiment extraction where general models (like DistilBERT) fail.
* **Self-Healing Pipeline:** Orchestrated via **Prefect** and **GitHub Actions** with automated retries, exponential backoff for API rate limits, and graceful degradation.
* **Statistical Anomaly Detection:** Implements rolling **Z-score analysis** to filter out market noise and highlight statistically significant sentiment shifts.
* **Data Integrity First:** Strict schema enforcement using **Pydantic** models to ensure the "Source of Truth" remains unpolluted by malformed API responses.

---

## 🛠️ Tech Stack

| Layer               | Technology                                                                 |
|---------------------|----------------------------------------------------------------------------|
| **Language** | Python 3.12                                                                |
| **AI / NLP** | FinBERT (HuggingFace), Groq API (Llama 3.3 70B)                           |
| **Database** | Supabase (PostgreSQL) + PgVector                                          |
| **Orchestration** | Prefect, GitHub Actions                                                    |
| **API / Backend** | FastAPI, Pydantic                                                          |
| **Frontend** | Streamlit (Real-time Dashboard)                                            |

---

## 🚀 Getting Started

### 1. Prerequisites
* Python 3.12+
* Supabase Account
* API Keys for: Alpha Vantage, Groq

### 2. Installation
```bash
# Clone the repository
git clone [https://github.com/YOUR_USERNAME/fin-intel-pipeline.git](https://github.com/YOUR_USERNAME/fin-intel-pipeline.git)
cd fin-intel-pipeline

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
