# 🤖 AI-Manager-Agent (Local)

A secure, offline AI Agency Manager powered by **Local LLMs (Qwen & Llama)** and **Docker**.
This application runs entirely on your local machine (Air-Gapped ready), ensuring 100% data privacy for sensitive legal and financial workflows.

## 🚀 Features

### 1. 🧠 The Intelligent Manager (Router)
- **Model:** `qwen2.5-coder:32b`
- **Role:** The "Boss." It analyzes your request, determines intent, and automatically routes tasks to the correct specialist agent (Legal vs. Data).

### 2. ⚖️ Legal Advisor Agent
- **Model:** `llama3.1:8b`
- **Capabilities:**
  - **RAG Engine:** Scans the *Industrial Disputes Act* (or any PDF) to answer queries with citations.
  - **Drafting:** Auto-generates legal notices and letters.

### 3. 📊 Data Analyst Agent
- **Model:** `Python Sandbox` (Managed by Qwen)
- **Capabilities:**
  - **Automated Charting:** Reads CSV files and generates bar charts/histograms instantly.
  - **Analysis:** Executes real Python code to calculate sums, averages, and trends locally.

---

## 🛠️ Tech Stack
- **Containerization:** Docker
- **Models:** Qwen 2.5 (32B), Llama 3.1 (8B)
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