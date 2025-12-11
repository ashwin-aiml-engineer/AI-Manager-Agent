# 🤖 The Sovereign AI Agency (Local)

A secure, **100% Offline** AI Agency Manager powered by **Local LLMs (Qwen, Llama, Gemma)**.
This application runs entirely on your local machine (Air-Gapped ready), ensuring total data privacy for sensitive workflows. It transforms your laptop into a private server capable of Legal Research, Data Analysis, and Hiring Automation.

> **Current Version:** v1.1 (Enterprise Update) - *Dec 11, 2025*

## 🚀 Key Features

### 1. 💾 Long-Term Memory (New!)
- **Tech:** SQLite Database (Local).
- **Capability:** The AI remembers past conversations even after you restart the computer.
- **Management:** Full **CRUD** support (Create, Read, Update, Delete) — view past case files or delete sensitive history instantly.

### 2. 📂 Universal Knowledge Portal (New!)
- **Tech:** LangChain `Smart Ingestion`.
- **Capability:** Drag-and-drop **PDFs, Word Docs (.docx), Text files, or PPTs** directly into the sidebar.
- **Smart Learning:** The system uses **Incremental Ingestion**—it only "reads" new files, updating its knowledge base in seconds without rebuilding the whole database.

### 3. 🎙️ Voice Command Interface
- **Model:** `OpenAI Whisper (Base)` running locally.
- **Capabilities:**
  - **Speech-to-Text:** Talk to your AI instead of typing.
  - **Offline Processing:** No audio data is ever sent to the cloud.
  - **"WhatsApp-Style" Layout:** Voice recorder sits naturally above the chat input.

### 4. 🧠 The Intelligent Manager (Router)
- **Model:** `qwen2.5-coder:32b` (Pro) / `llama3.1` (Lite)
- **Role:** The "Boss." It analyzes your request, determines intent, and routes tasks to the correct specialist department (Legal, Data, or HR).

### 5. 📊 Data Analyst Agent (Pro Only)
- **Model:** `Python Sandbox` (Managed by Qwen)
- **Capabilities:**
  - **Persistent Analysis:** Upload a CSV once; it stays available across sessions.
  - **Automated Charting:** Generates bar charts, line graphs, and heatmaps instantly.
  - **Safe Execution:** Runs real Python code locally to calculate trends.

---

## ⚙️ Configuration (Pro vs. Lite)
This system features a **Config Switch** (`config.py`) to adapt to your hardware:

| Feature | **LITE TIER** (8GB RAM) | **PRO TIER** (32GB RAM) |
| :--- | :--- | :--- |
| **Primary Model** | Llama 3.1 (8B) | Qwen 2.5 Coder (32B) |
| **Resume Model** | Llama 3.1 (8B) | Gemma 2 (9B) |
| **Data Analysis** | ❌ Disabled | ✅ Enabled |
| **Voice Mode** | ✅ Enabled | ✅ Enabled |

*To switch versions, simply edit `VERSION_TIER = "PRO"` in `config.py`.*

---

## 🛠️ Tech Stack
- **Language:** Python 3.10
- **Containerization:** Docker
- **Models:** Qwen 2.5 (32B), Llama 3.1 (8B), Gemma 2 (9B), Whisper
- **Orchestration:** LangChain & Ollama
- **Database:** - **Vector:** ChromaDB (for Documents/RAG)
  - **Relational:** SQLite (for Chat History)
- **Frontend:** Streamlit

---

## 💻 How to Run (Option A: One-Click Launcher 🚀)
*For Windows Users*

1. **Prerequisite:** Ensure Ollama is installed.
2. **Run:** Double-click `start_agency.bat`.
   - This script automatically activates the environment, checks if Ollama is running, and launches the app.

---

## 💻 How to Run (Option B: Manual Python 🐍)
For developers who want to modify the code.

1. **Clone the repository**
   ```bash
   git clone https://github.com/ashwin-aiml-engineer/AI-Manager-Agent.git
   cd AI-Manager-Agent
   ```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Install AI Models (Ollama)**
```bash
ollama pull llama3.1
ollama pull qwen2.5-coder:32b
ollama pull nomic-embed-text
ollama pull gemma2:9b
```

4. **Launch**
```bash
streamlit run app.py
```
Note: You can add files to the Knowledge Base directly via the app's sidebar.

---

## 📂 Project Structure

AI-Manager-Agent/
├── app.py              # Main Application (UI & Logic)
├── ingest.py           # Smart Knowledge Loader (Incremental)
├── db.py               # SQLite Database Manager
├── config.py           # Hardware Profile Switcher
├── router.py           # Intelligent Intent Router
├── voice.py            # Whisper Voice Recorder
├── ats.py              # Resume Optimizer Module
├── start_agency.bat    # Windows Launcher
├── data/               # (Auto-Created) Stores PDFs/Docs
├── uploads/            # (Auto-Created) Stores Analysis CSVs
└── vector_db/          # (Auto-Created) ChromaDB Storage

---
**Author: Ashwin Shetty**




