# 🤖 AI-Manager-Agent (Local)

A secure, offline AI Agency Manager powered by **Llama 3.1** and **Python**.
This application runs entirely on your local machine, ensuring 100% data privacy for sensitive legal and financial documents.

## 🚀 Features

### 1. ⚖️ Legal Advisor Agent
- **Contract Review:** Scans entire agreements for red flags and risks using Llama 3.1's 128k context window.
- **Drafting:** Auto-generates legal notices and letters.
- **General Advice:** Provides legal information based on Indian context.

### 2. 📊 Data Analyst Agent
- **Automated Charts:** plots bar charts, line graphs, and histograms from CSV files.
- **Natural Language Q&A:** Ask questions like "What is the total sales for Product A?" and get instant answers.
- **Privacy First:** No data leaves the laptop. Everything is processed locally.

## 🛠️ Tech Stack
- **Engine:** Llama 3.1 (8B) via Ollama
- **Frontend:** Streamlit
- **Orchestration:** LiteLLM
- **Language:** Python 3.12+

## 💻 How to Run Locally

1. **Clone the repository**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/ai-agency-manager.git](https://github.com/YOUR_USERNAME/ai-agency-manager.git)
   ```

2. **Install Dependencies**

```bash
pip install streamlit pandas matplotlib seaborn pandasai-litellm
```

3.**Install Llama 3.1 Download Ollama and run:**

```bash
ollama pull llama3.1
```

4. **Launch the Agent**

```bash
streamlit run app.py
```
---
Author: Ashwin Shetty