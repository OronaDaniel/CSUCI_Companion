# 🐬 Phin: The CSUCI Companion

> **A Retrieval-Augmented Generation (RAG) Assistant for CSU Channel Islands**

**Phin** is an AI-powered academic assistant designed to help students at **CSUCI** navigate their academic journey. Built on the **OpenAI Assistants API** (GPT-4 Turbo), Phin replaces static keyword searches with natural conversation, offering tailored course recommendations, natural language scheduling, and real-time answers to campus queries.

---

## 📸 Demo

<p align="center">
  <img src="images/start_page.png" width="700" alt="Home UI">
</p>

<p align="center">
  <img src="images/AI_electives_example_prompts.png" width="45%" alt="Electives assistant">
  &nbsp; &nbsp;
  <img src="images/campus_activites_example_prompt.png" width="45%" alt="Campus activities query">
</p>

<p align="center">
  <i>Left: Natural Language Course Recs | Right: RAG-based Event Retrieval</i>
</p>

---

## 🚀 Key Features

* **🎓 Intelligent Course Recommendations:** Suggests classes based on major, interests, and prerequisites.
* **🗓️ Natural Language Scheduling:** "Agentic" scheduling that optimizes class times based on personal constraints (e.g., "Keep my Fridays free").
* **🏫 Real-Time Campus Knowledge:** RAG pipeline integrated with scraping to answer questions about clubs, events, and deadlines.
* **🔗 Deep Integration:** Custom-built data ingestion pipeline for up-to-date course catalogs and event data.

---

## 🛠️ Architecture

```mermaid
flowchart TB
  U([User]) -->|Query| T[Create/Retrieve Thread]
  T --> P{{Phin}}

  %% CSUCI-specific retrieval
  P -->|CSUCI Specific| KR[Query CSUCI Data Sources]
  KR --> IDX[Retrieve from CSUCI Knowledge Base]
  IDX --> LLM

  %% General
  P -->|General Query| LLM[Use GPT-4 Turbo Model]

  %% Analytical / code
  P -->|Analytical| CI[Code Interpreter]
  CI --> SETUP[Setup Environment & Execute Code]
  SETUP --> LLM

  %% Output
  LLM --> GEN[Generate / Format Response]
  GEN --> D([Display to User])
```

**Tech Stack: Flask · LangChain · OpenAI Assistants API · Scrapy · Twisted**

---

## 🕷️ Data Engineering

Unlike generic chatbots, Phin relies on ground-truth data directly from the university. We engineered a custom ETL pipeline to ensure accuracy:

### Course Catalog Scraper
* **Tooling**: Utilized **Scrapy** for its asynchronous event-driven architecture (Twisted reactor).
* **Logic**: The crawler systematically traverses the CSUCI course catalog hierarchy (Subjects → Course Details), parsing HTML structures to extract prerequisites, units, and descriptions.
* **Output**: Exports standardized **JSON feeds** (see `data/samples/sample_output.json`) which are then indexed for retrieval by the RAG system.

*Check the `data-ingestion/course-scraper` directory for the crawler implementation.*

---

## 📂 Repository Structure
```text
CSUCI_Companion/
├── app.py                      # Flask application entry point
├── requirements.txt            # Dependencies
├── data-ingestion/
│   └── course-scraper/         # Custom Scrapy crawler (Async/Twisted)
├── data/
│   └── samples/                # Sample JSON outputs from scraper
├── static/                     # CSS/JS assets
├── images/                     # Documentation images
└── README.md                 
```

---

## ⚡ Quickstart
**Prerequisites**: Python 3.10+, OpenAI API Key, and Assistant ID.

```bash
# 1) Create & activate a virtual env
python -m venv .venv
source .venv/bin/activate

# 2) Install libraries
pip install -r requirements.txt

# 3) Add your keys (secret.py is gitignored)
cat > secret.py <<'PY'
api_key = "sk-..."
assistant_id = "asst_..."
secret_key = "change-me"
PY

# 4) Run the app
flask --app app run --port 8000
# visit http://localhost:8000
```

#### Environment Variables (secret.py)

| Variable | Required | Description |
|------|:--------|----------------|
| `api_key` | ✅ |OpenAI API Key |
| `assistant_id` | ✅ | OpenAI Assistant ID to run |
| `secret_key` | ⚙️ | Flask session security string |

---

#### ℹ️ Project Origin
*Developed as a Computer Science Capstone at CSU Channel Islands.*
 
