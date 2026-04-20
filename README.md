# 💹 MarketSense: Real-Time Financial Intelligence Engine
### High-Concurrency MLOps Pipeline | FinBERT Sentiment Analysis | Live WebSocket Alerts

MarketSense is a production-grade data platform that processes live financial news into actionable sentiment signals. Built with a **Cloud-Native Architecture**, this system is engineered to serve low-latency insights to 100+ concurrent users simultaneously.

---

## 🏗️ System Design: Built for Scale
Most portfolio projects use local files (CSV/SQLite) which fail under concurrent load. MarketSense is designed for production reliability:

* **The Ingestion Engine:** A robust collector pulling from **AlphaVantage** and **yfinance**, utilizing **Pydantic** for strict data-contract enforcement and schema validation.
* **The Intelligence Layer:** Specialized **FinBERT** (Financial BERT) inference to detect nuanced market tones that generic NLP models often misinterpret.
* **The High-Concurrency Core:** Built on **PostgreSQL (Supabase)** with **Supavisor** connection pooling. This allows the system to handle 100+ simultaneous user connections without database locks.
* **The Edge Broadcaster:** Uses **Postgres Change Data Capture (CDC)** to push live sentiment shifts to users via WebSockets as they happen.

---

## 🛠️ The Engineering Stack
| Component       | Technology           | Why? |
| :-------------- | :------------------- | :--- |
| **Language** | Python 3.12          | Standard for AI/Data Engineering. |
| **Orchestration**| Prefect 3.0          | Provides observability and auto-retries for scraping tasks. |
| **NLP Model** | FinBERT              | Specialized for financial context (bearish/bullish detection). |
| **Database** | Supabase (Postgres)  | Cloud-scale relational storage with real-time capabilities. |
| **Scaling** | Supavisor            | Connection pooling to support 100+ concurrent sessions. |
| **API** | FastAPI              | High-performance asynchronous framework for data serving. |

---

## 📂 Project Structure
```text
fin-intel-engine/
├── src/
│   ├── ingestion/    # Live news collectors & schema validation
│   ├── brain/        # FinBERT scoring & LLM signal reasoning
│   ├── api/          # FastAPI server with connection pooling
│   └── dashboard/    # Real-time WebSocket-enabled UI
├── .github/workflows/ # Automation & CI/CD
├── database/         # Migrations & indexing strategies for 100+ users
└── config/           # Pydantic settings & API management
```

---

## 🚀 Vision & Roadmap
MarketSense is a foundation for automated trading signals and sentiment monitoring.
- [ ] **Phase 1:** End-to-end ingestion and FinBERT scoring.
- [ ] **Phase 2:** WebSocket implementation for live 100+ user broadcasting.
- [ ] **Phase 3:** RAG-based search for querying historical news trends.

---
##  System Architecture so far

<img width="8191" height="707" alt="Data Ingestion and-2026-04-20-174006" src="https://github.com/user-attachments/assets/dade69aa-40fe-44f2-b2cb-2176ec346220" />



## ⚖️ License
Distributed under the MIT License.

**Built by Aditya Shashank Chinta** | [LinkedIn](https://www.linkedin.com/in/aditya-shashank/)
