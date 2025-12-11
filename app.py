import os
import sys

# ==============================================================================
# 🛠️ CRITICAL WINDOWS DLL FIXES
# ==============================================================================
try:
    if sys.platform == "win32":
        conda_bin_path = os.path.join(sys.prefix, 'Library', 'bin')
        if os.path.exists(conda_bin_path):
            os.add_dll_directory(conda_bin_path)
except Exception as e:
    print(f"⚠️ Warning: Could not add DLL directory: {e}")

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

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
import db           # 💾 THE MEMORY
import ingest       # 🧠 THE BRAIN (Added this!)
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
    
    # 1. Initialize Session State
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "current_session_id" not in st.session_state:
        st.session_state.current_session_id = None

    # 2. Render Sidebar
    with st.sidebar:
        st.markdown("---")
        st.header("🗄️ Case Files (History)")
        
        if st.button("➕ Start New Case", use_container_width=True):
            st.session_state.messages = []
            st.session_state.current_session_id = None
            st.rerun()
            
        st.markdown("---")
        
        sessions = db.get_all_sessions()
        if not sessions:
            st.write("📭 No history found.")
        
        for s_id, title, date in sessions:
            col1, col2 = st.columns([0.85, 0.15])
            with col1:
                if st.button(f"📄 {title}", key=f"load_{s_id}", use_container_width=True):
                    st.session_state.messages = db.load_messages(s_id)
                    st.session_state.current_session_id = s_id
                    st.rerun()
            with col2:
                if st.button("🗑️", key=f"del_{s_id}"):
                    db.delete_session(s_id)
                    if st.session_state.current_session_id == s_id:
                        st.session_state.messages = []
                        st.session_state.current_session_id = None
                    st.toast(f"🗑️ Deleted: {title}")
                    st.rerun()

        # ==========================================
        # 📂 UNIVERSAL UPLOAD PORTAL (LOOP FIXED)
        # ==========================================
        st.markdown("---")
        st.header("📂 Upload Portal")
        
        # 1. Setup Folders
        if not os.path.exists("uploads"): os.makedirs("uploads")
        if not os.path.exists("data"): os.makedirs("data")
            
        DATA_PATH_CSV = "uploads/active_data.csv"
        
        # 2. Initialize State for Loop Prevention
        if "last_processed_file" not in st.session_state:
            st.session_state.last_processed_file = None

        # 3. File Uploader
        uploaded_file = st.file_uploader(
            "Upload Document / Dataset", 
            type=["csv", "pdf", "docx", "txt", "pptx"]
        )
        
        df = None
        if uploaded_file:
            file_ext = uploaded_file.name.split(".")[-1].lower()
            
            st.write("What should the AI do with this?")
            intent = st.radio(
                "Select Mode:",
                ["🧠 Add to Knowledge Base (Memory)", "📊 Load for Data Analysis (Charts)"],
                label_visibility="collapsed"
            )
            
            # === OPTION A: KNOWLEDGE BASE ===
            if "Knowledge" in intent:
                save_path = os.path.join("data", uploaded_file.name)
                
                # Button prevents loops automatically (Buttons reset to False on rerun)
                if st.button(f"📥 Ingest '{uploaded_file.name}'"):
                    with open(save_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    with st.spinner("Updating Brain..."):
                        try:
                            ingest.ingest()
                            st.success("✅ Saved to Long-Term Memory!")
                        except Exception as e:
                            st.error(f"❌ Error: {e}")

            # === OPTION B: DATA ANALYSIS (THE FIX) ===
            elif "Data" in intent:
                if file_ext != "csv":
                    st.error("⚠️ For Data Analysis (Charts), we currently ONLY support CSV files.")
                else:
                    # 🛑 STOP THE LOOP: Check if we already did this!
                    if st.session_state.last_processed_file != uploaded_file.name:
                        with open(DATA_PATH_CSV, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        # Mark this file as "Done" so we don't reload it next time
                        st.session_state.last_processed_file = uploaded_file.name
                        
                        st.toast("📊 Data loaded for Analyst!")
                        st.rerun()

        # Load existing Analysis CSV if available
        if os.path.exists(DATA_PATH_CSV):
            st.markdown("---")
            df = pd.read_csv(DATA_PATH_CSV)
            st.caption(f"📊 Active Analysis Data: {len(df)} rows")
            
            if st.button("❌ Unload Data", use_container_width=True):
                os.remove(DATA_PATH_CSV)
                # Reset the memory so we can upload the same file again if needed
                st.session_state.last_processed_file = None 
                st.rerun()

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
            db_conn = Chroma(persist_directory="vector_db", embedding_function=embeddings)
            return db_conn
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
    # 7. LAYOUT & RENDERING
    # ==========================================================================
    
    st.markdown("### 💬 Central Command")
    
    chat_container = st.container()   
    voice_container = st.container() 
    
    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                if isinstance(msg["content"], dict) and msg["content"].get("type") == "image":
                    st.image(msg["content"]["path"])
                    if msg["content"]["text"]: st.write(msg["content"]["text"])
                else:
                    st.write(msg["content"])

    with voice_container:
        voice_text = voice.record_voice_widget()
    
    chat_input = st.chat_input("Type a message...")

    # ==========================================================================
    # 8. PROCESSING LOGIC
    # ==========================================================================
    
    if chat_input:
        prompt = chat_input
    elif voice_text:
        prompt = voice_text
    else:
        prompt = None

    if prompt:
        if st.session_state.current_session_id is None:
            st.session_state.current_session_id = db.create_session(prompt)

        st.session_state.messages.append({"role": "user", "content": prompt})
        db.save_message(st.session_state.current_session_id, "user", prompt)
        
        with chat_container:
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

        st.session_state.messages.append({"role": "assistant", "content": response_content})
        db.save_message(st.session_state.current_session_id, "assistant", response_content)
        
        with chat_container:
            with st.chat_message("assistant"):
                if isinstance(response_content, dict) and response_content.get("type") == "image":
                    st.image(response_content["path"])
                    if response_content["text"]: st.write(response_content["text"])
                else:
                    st.write(response_content)