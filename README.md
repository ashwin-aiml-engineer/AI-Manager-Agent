# 🤖 AI-Manager-Agent (Local)

A secure, offline AI Agency Manager powered by **Llama 3.1** and **Python**.
This application runs entirely on your local machine, ensuring 100% data privacy for sensitive legal and financial documents.

## 🚀 Features

### 1. ⚖️ Legal Advisor Agent
- **Contract Review:** Scans entire agreements for red flags and risks using Llama 3.1's 128k context window.
- **Drafting:** Auto-generates legal notices and letters.
- **General Advice:** Provides legal information based on Indian context.

### 2. 📊 Data Analyst Agent
- **Automated Charts:** Plots bar charts, line graphs, and histograms from CSV files.
- **Natural Language Q&A:** Ask questions like "What is the total sales for Product A?" and get instant answers.
- **Privacy First:** No data leaves the laptop. Everything is processed locally.

## 🛠️ Tech Stack
- **Engine:** Llama 3.1 (8B) & Qwen 2.5 (32B) via Ollama
- **Frontend:** Streamlit
- **Orchestration:** LiteLLM & LangChain
- **Vector DB:** ChromaDB
- **Language:** Python 3.10+

## 💻 How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/ai-agency-manager.git
cd ai-agency-manager
```

### 2. Install Dependencies
```bash
pip install streamlit pandas matplotlib seaborn litellm langchain-chroma langchain-ollama
```

### 3. Install AI Models
Download Ollama and pull the required brains:
```bash
ollama pull llama3.1
ollama pull qwen2.5-coder:32b
ollama pull nomic-embed-text
```

### 4. Build the Legal Brain (Optional)
Place your PDF in the root folder, rename it to data.pdf, and run:
```bash
python ingest.py
```

### 5. Launch the Agent
```bash
streamlit run app.py
```

---
*Author: Ashwin Shetty*