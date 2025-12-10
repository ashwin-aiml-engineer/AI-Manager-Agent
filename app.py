import os
import sys

# ==============================================================================
# 🛠️ CRITICAL WINDOWS DLL FIXES (MUST BE FIRST)
# ==============================================================================

# 1. Force Windows to look in the Conda "Library/bin" folder for missing DLLs
try:
    if sys.platform == "win32":
        conda_bin_path = os.path.join(sys.prefix, 'Library', 'bin')
        if os.path.exists(conda_bin_path):
            os.add_dll_directory(conda_bin_path)
except Exception as e:
    print(f"⚠️ Warning: Could not add DLL directory: {e}")

# 2. Allow duplicate OpenMP libraries
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# 3. Docker/Windows Database Fix
try:
    __import__('pysqlite3')
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass

# --- SYSTEM CONFIG ---
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["OLLAMA_NUM_GPU"] = "0"

# ==============================================================================
# 2. IMPORTS & DEPENDENCIES
# ==============================================================================
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO
from contextlib import redirect_stdout
from litellm import completion

# --- INTERNAL MODULES ---
import ats          # HR Dept
import voice        # The Ears
from config import CURRENT_CONFIG
from router import route_query

# --- VECTOR DATABASE ---
try:
    from langchain.vectorstores import Chroma
    from langchain.embeddings import OllamaEmbeddings
except ImportError:
    from langchain_community.vectorstores import Chroma
    from langchain_community.embeddings import OllamaEmbeddings

# ==============================================================================
# 3. PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title=CURRENT_CONFIG["system_name"], 
    page_icon="🤖", 
    layout="wide"
)

st.title(f"🤖 {CURRENT_CONFIG['system_name']}")

# ==============================================================================
# 4. SIDEBAR NAVIGATION
# ==============================================================================
st.sidebar.title("🏢 Department Directory")
page = st.sidebar.radio(
    "Go to Department:", 
    ["Chat Manager (Main)", "Resume ATS (HR Dept)"]
)

# ==============================================================================
# 5. PAGE ROUTING LOGIC
# ==============================================================================

if page == "Resume ATS (HR Dept)":
    ats.render_ats_page()

else:
    # --- MODE B: CHAT MANAGER (The Main App) ---
    st.markdown("### 💬 Central Command")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # ==========================================================================
    # 6. HELPER FUNCTIONS
    # ==========================================================================
    
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

    def ask_legal_agent(query):
        legal_db = get_legal_db()
        if not legal_db:
            return "⚠️ Legal System Offline. Check terminal."
        try:
            results = legal_db.similarity_search(query, k=3)
            context = "\n".join([doc.page_content for doc in results])
            prompt = f"You are a Corporate Lawyer. Answer based ONLY on this context:\n{context}\nUser Question: {query}"
            ollama_url = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")
            response = completion(
                model=f"ollama/{CURRENT_CONFIG['manager_model']}", 
                messages=[{"role": "user", "content": prompt}],
                api_base=ollama_url,
                options={"num_gpu": 0}
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            return f"❌ Legal Agent Crash: {e}"

    def ask_data_agent(query, df):
        if not CURRENT_CONFIG["allow_data_analysis"]:
            return "🔒 **RESTRICTED FEATURE:** Data Analysis is only available in the PRO version."

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
                model=f"ollama/{CURRENT_CONFIG['data_agent_model']}", 
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

    # ==========================================================================
    # 7. SIDEBAR DATA
    # ==========================================================================
    with st.sidebar:
        st.markdown("---")
        st.header("📂 Data Center")
        uploaded_file = st.file_uploader("Upload CSV for Analysis", type=["csv"])
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.success(f"Loaded: {len(df)} rows")
        else:
            df = None

    # ==========================================================================
    # 8. LAYOUT ARCHITECTURE (The Fix)
    # ==========================================================================
    
    # We define the containers FIRST so we can fill them in any order we want.
    chat_container = st.container()   # 1. Top Area (History)
    voice_container = st.container()  # 2. Middle Area (Recorder)
    # 3. Bottom Area is automatically handled by st.chat_input pinning itself.

    # ==========================================================================
    # 9. RENDER HISTORY (Inside the Top Container)
    # ==========================================================================
    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                if isinstance(msg["content"], dict) and msg["content"].get("type") == "image":
                    st.image(msg["content"]["path"])
                    if msg["content"]["text"]: st.write(msg["content"]["text"])
                else:
                    st.write(msg["content"])

    # ==========================================================================
    # 10. RENDER INPUTS
    # ==========================================================================
    
    # A. Voice Recorder (Inside Middle Container)
    with voice_container:
        voice_text = voice.record_voice_widget()
    
    # B. Text Input (Pinned to Bottom)
    chat_input = st.chat_input("Type a message...")

# ==========================================================================
    # 11. PROCESSING LOGIC (Priority: Text > Voice)
    # ==========================================================================
    
    # CRITICAL FIX: We check Text FIRST. 
    # If the user hit Enter on the keyboard, that is the clear intent.
    if chat_input:
        prompt = chat_input
    elif voice_text:
        prompt = voice_text
    else:
        prompt = None

    if prompt:
        # 1. Add User Message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # If voice was used (and not overridden by text), show the bubble
        if voice_text and not chat_input:
             with st.chat_message("user"):
                st.write(prompt)

        # B. Process (The Brain)
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
                ollama_url = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")
                try:
                    response = completion(
                        model=f"ollama/{CURRENT_CONFIG['manager_model']}", 
                        messages=[{"role": "user", "content": prompt}],
                        api_base=ollama_url,
                        options={"num_gpu": 0}
                    )
                    response_content = response['choices'][0]['message']['content']
                except Exception as e:
                    response_content = f"❌ General Chat Error: {e}"

        # C. Add AI Response (AND write it visually to the Top Container immediately)
        st.session_state.messages.append({"role": "assistant", "content": response_content})
        
        # Again, force it into the top container so it stays above the recorder
        with chat_container:
            with st.chat_message("assistant"):
                if isinstance(response_content, dict) and response_content.get("type") == "image":
                    st.image(response_content["path"])
                    if response_content["text"]: st.write(response_content["text"])
                else:
                    st.write(response_content)