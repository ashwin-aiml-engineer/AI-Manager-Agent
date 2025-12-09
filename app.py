# --- DOCKER DATABASE FIX (Conditional) ---
# We wrap this in try-except so it doesn't crash on Windows
try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    # This means we are on Windows (or the package isn't installed).
    # We pass and rely on the standard sqlite3 library.
    pass
# -----------------------------------------------------
import os
# DISABLE CHROMA TELEMETRY
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["OLLAMA_NUM_GPU"] = "0" 

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO
from contextlib import redirect_stdout
from litellm import completion
import ats  # <--- Imported correctly

# --- 🛠️ CRITICAL FIX: Use Old Stable Imports ---
try:
    from langchain.vectorstores import Chroma
    from langchain.embeddings import OllamaEmbeddings
except ImportError:
    from langchain_community.vectorstores import Chroma
    from langchain_community.embeddings import OllamaEmbeddings

from router import route_query

# 1. Page Config
st.set_page_config(page_title="AI Agency Manager", page_icon="🤖", layout="wide")
st.title("🤖 AI Agency Manager")

# 2. Sidebar Navigation
st.sidebar.title("🏢 Department Directory")
page = st.sidebar.radio(
    "Go to Department:", 
    ["Chat Manager (Main)", "Resume ATS (HR Dept)"]
)

# ---------------------------------------------------------
# 🚦 PAGE ROUTING LOGIC (The Fix)
# ---------------------------------------------------------

if page == "Resume ATS (HR Dept)":
    # --- MODE A: RESUME TOOL ---
    # We call the function from ats.py and STOP here. 
    # We do NOT show the chat interface.
    ats.render_ats_page()

else:
    # --- MODE B: CHAT MANAGER (The original app) ---
    
    st.markdown("### 💬 Central Command")
    
    # 3. Session State (Only needed for Chat Mode)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 4. Safe Brain Loading
    def get_legal_db():
        if not os.path.exists("vector_db"):
            st.error("❌ Error: 'vector_db' folder not found.")
            return None
        try:
            ollama_url = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")
            embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url=ollama_url)
            db = Chroma(persist_directory="vector_db", embedding_function=embeddings)
            return db
        except Exception as e:
            st.error(f"❌ Database Error: {e}")
            return None

    # 5. Helper: Legal Agent
    def ask_legal_agent(query):
        legal_db = get_legal_db()
        if not legal_db:
            return "⚠️ Legal System Offline. Check terminal."
        
        try:
            results = legal_db.similarity_search(query, k=3)
            context = "\n".join([doc.page_content for doc in results])
            
            prompt = f"""
            You are a Corporate Lawyer. Answer based ONLY on this context:
            {context}
            User Question: {query}
            """
            ollama_url = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")
            
            response = completion(
                model="ollama/llama3.1", 
                messages=[{"role": "user", "content": prompt}],
                api_base=ollama_url,
                options={"num_gpu": 0}
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            return f"❌ Legal Agent Crash: {e}"

    # 6. Helper: Data Agent
    def ask_data_agent(query, df):
        prompt = f"""
        You are a Python Data Analyst. 
        DataFrame columns: {df.columns.tolist()}
        User Request: {query}
        Write PYTHON code to solve this. 
        - If plotting, save to 'exports/charts/chart.png'.
        - If calculating, print the answer.
        - OUTPUT ONLY CODE.
        """
        ollama_url = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")

        try:
            response = completion(
                model="ollama/qwen2.5-coder:32b", 
                messages=[{"role": "user", "content": prompt}],
                api_base=ollama_url,
                options={"num_gpu": 0} 
            )
            
            code = response['choices'][0]['message']['content'].replace("```python", "").replace("```", "").strip()
            
            output_buffer = StringIO()
            chart_file = "exports/charts/chart.png"
            if not os.path.exists("exports/charts"): os.makedirs("exports/charts")
            if os.path.exists(chart_file): os.remove(chart_file)
            
            with redirect_stdout(output_buffer):
                exec(code, {"df": df, "pd": pd, "plt": plt, "sns": sns})
                    
            result_text = output_buffer.getvalue()
            if os.path.exists(chart_file):
                return {"type": "image", "path": chart_file, "text": result_text}
            return result_text
        except Exception as e:
            return f"❌ Data Logic Error: {e}"

    # 7. Sidebar Data Upload (Only for Chat Mode)
    with st.sidebar:
        st.markdown("---")
        st.header("📂 Data Center")
        uploaded_file = st.file_uploader("Upload CSV for Analysis", type=["csv"])
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.success(f"Loaded: {len(df)} rows")
        else:
            df = None

    # 8. Chat Display Loop
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            if isinstance(msg["content"], dict) and msg["content"].get("type") == "image":
                st.image(msg["content"]["path"])
                if msg["content"]["text"]: st.write(msg["content"]["text"])
            else:
                st.write(msg["content"])

    # 9. Input Handling & Routing
    if prompt := st.chat_input("How can I help you?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.spinner("🤖 Routing request..."):
            department = route_query(prompt)
            response_content = ""
            
            if department == "legal":
                st.toast("⚖️ Transferred to Legal Dept.")
                response_content = ask_legal_agent(prompt)
                
            elif department == "data":
                if df is not None:
                    st.toast("📊 Transferred to Data Dept.")
                    response_content = ask_data_agent(prompt, df)
                else:
                    response_content = "⚠️ Please upload a CSV file to use the Data Agent."
            
            else:
                # General Chat
                ollama_url = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")
                try:
                    response = completion(
                        model="ollama/llama3.1", 
                        messages=[{"role": "user", "content": prompt}],
                        api_base=ollama_url,
                        options={"num_gpu": 0}
                    )
                    response_content = response['choices'][0]['message']['content']
                except Exception as e:
                    response_content = f"❌ General Chat Error: {e}"

        # Display Response
        st.session_state.messages.append({"role": "assistant", "content": response_content})
        with st.chat_message("assistant"):
            if isinstance(response_content, dict) and response_content.get("type") == "image":
                st.image(response_content["path"])
                if response_content["text"]: st.write(response_content["text"])
            else:
                st.write(response_content)