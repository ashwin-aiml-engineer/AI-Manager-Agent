# 🤖 The Sovereign AI Agency (Local)

A secure, **100% Offline** AI Agency Manager powered by **Local LLMs (Qwen, Llama, Gemma)**.
This application runs entirely on your local machine (Air-Gapped ready), ensuring total data privacy for sensitive workflows. It includes a Voice Interface, Resume ATS Optimizer, and Data Analysis tools.


## 🚀 Features

### 1. 🎙️ Voice Command Interface (New!)
- **Model:** `OpenAI Whisper (Base)` running locally.
- **Capabilities:**
  - **Speech-to-Text:** Talk to your AI instead of typing.
  - **Offline Processing:** No audio data is ever sent to the cloud.
  - **"WhatsApp-Style" Layout:** Voice recorder sits naturally above the chat input.

### 2. 🧠 The Intelligent Manager (Router)
- **Model:** `qwen2.5-coder:32b` (Pro) / `llama3.1` (Lite)
- **Role:** The "Boss." It analyzes your request, determines intent, and routes tasks to the correct specialist department (Legal, Data, or HR).

### 3. 📄 Resume ATS Agent (HR Dept)
- **Model:** `gemma2:9b`
- **Capabilities:**
  - **Analysis:** Scans resumes against job descriptions.
  - **Optimization:** Rewrites bullet points to beat ATS (Applicant Tracking Systems).
  - **Scoring:** Provides a match percentage score.

### 4. ⚖️ Legal Advisor Agent
- **Model:** `llama3.1:8b`
- **Capabilities:**
  - **RAG Engine:** Scans the *Industrial Disputes Act* (or any PDF) to answer queries with citations.
  - **Drafting:** Auto-generates legal notices and letters.

### 5. 📊 Data Analyst Agent (Pro Only)
- **Model:** `Python Sandbox` (Managed by Qwen)
- **Capabilities:**
  - **Automated Charting:** Reads CSV files and generates charts instantly.
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
- **Containerization:** Docker
- **Models:** Qwen 2.5 (32B), Llama 3.1 (8B), Gemma 2 (9B), Whisper
- **Orchestration:** LangChain & Ollama
- **Vector DB:** ChromaDB
- **Frontend:** Streamlit

---

## 💻 How to Run (Option A: Docker 🐳) - *Recommended*
*No Python installation required. Just Docker and Ollama.*

1. **Pull the image (or build it)**
   ```bash
   docker build -t ai-agency-manager .
   ```

2. **Run the Container** 
Note: This command connects the container to your host's Ollama instance.

```bash
docker run -p 8501:8501 -e OLLAMA_API_BASE="[http://host.docker.internal:11434](http://host.docker.internal:11434)" ai-agency-manager
```

3. **Access the App**
Open your browser to http://localhost:8501.

---
## 💻 How to Run (Option B: Python Source 🐍)
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
3. **Install AI Models (Ollama) You need Ollama installed.**
```bash
ollama pull llama3.1
ollama pull qwen2.5-coder:32b
ollama pull nomic-embed-text
ollama pull gemma2:9b
```
4.**Prepare the Brain Place your PDF in the root folder, rename it to data.pdf, and run:**
```bash
python ingest.py
```
5.**Launch**
```bash
streamlit run app.py
```
---
**Author: Ashwin Shetty**