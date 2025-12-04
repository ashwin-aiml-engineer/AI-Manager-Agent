import streamlit as st
import pandas as pd
import os
import re
import sys
from io import StringIO
from contextlib import redirect_stdout
from litellm import completion

# 1. Page Configuration
st.set_page_config(page_title="Data Analyst Agent", page_icon="📊", layout="wide")
st.title("📊 Data Analyst Agent")
st.markdown("Powered by **Llama 3.1** & Python (Local)")

# 2. File Uploader
with st.sidebar:
    st.header("Data Center")
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

# 3. Helper Functions
def extract_code(text):
    """Pulls python code out of the AI's response"""
    pattern = r"```python(.*?)```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text

# 4. Main Logic
if uploaded_file is not None:
    # Load Data
    df = pd.read_csv(uploaded_file)
    
    # Create export folder if missing
    chart_folder = "exports/charts"
    if not os.path.exists(chart_folder):
        os.makedirs(chart_folder)
        
    with st.expander("🔍 Preview Data"):
        st.dataframe(df.head())

    # Chat Interface
    query = st.text_area("🗣️ Ask a question:", placeholder="e.g., What are the total sales? OR Plot a chart of sales.")

    if st.button("Analyze"):
        if query:
            # --- FIX 1: CLEANUP OLD FILES BEFORE RUNNING ---
            # This prevents "Ghost Charts" from appearing when you didn't ask for them
            chart_path = f"{chart_folder}/output_chart.png"
            if os.path.exists(chart_path):
                os.remove(chart_path)

            with st.spinner("🤖 Llama 3.1 is thinking..."):
                try:
                    # --- STEP 1: CONSTRUCT THE PROMPT ---
                    prompt = f"""
                    You are a Python Data Analyst. 
                    You are given a pandas DataFrame named `df`.
                    
                    Data Schema:
                    {df.dtypes}
                    
                    User Request: {query}
                    
                    Write a PYTHON script to solve this. 
                    RULES:
                    1. Use the variable `df` directly.
                    2. If the user asks for a visualization:
                       - Create it using matplotlib
                       - Save it to '{chart_folder}/output_chart.png' using plt.savefig()
                       - Do NOT use plt.show()
                    3. If the user asks for a number (like "Total Sales"):
                       - PRINT the breakdown first (e.g., "Sales for A: X, Sales for B: Y")
                       - Then PRINT the final answer.
                       - DO NOT generate a chart unless explicitly asked.
                    4. OUTPUT ONLY CODE. No explanations.
                    5. DO NOT use SQL. Use Pandas.
                    """

                    # --- STEP 2: CALL LLAMA 3.1 ---
                    response = completion(
                        model="ollama/llama3.1", 
                        messages=[{"role": "user", "content": prompt}],
                        api_base="http://localhost:11434"
                    )
                    
                    ai_reply = response['choices'][0]['message']['content']
                    code_to_run = extract_code(ai_reply)
                    code_to_run = code_to_run.replace("plt.show()", "")

                    # --- STEP 3: EXECUTE & CAPTURE OUTPUT ---
                    output_buffer = StringIO()
                    
                    with st.expander("view code"):
                        st.code(code_to_run, language='python')
                    
                    exec_globals = {
                        "df": df, 
                        "pd": pd, 
                        "plt": __import__("matplotlib.pyplot"),
                        "sns": __import__("seaborn")
                    }

                    with redirect_stdout(output_buffer):
                        exec(code_to_run, exec_globals)
                    
                    st.success("Analysis Complete!")

                    # --- STEP 4: DISPLAY RESULTS ---
                    
                    # A. Check for Text Output (The Answer)
                    text_result = output_buffer.getvalue()
                    if text_result:
                        st.info(f"**Answer:**\n\n{text_result}")
                    
                    # B. Check for Chart Output (Only if new file exists)
                    if os.path.exists(chart_path):
                        st.image(chart_path, caption="Generated Chart")
                    
                    # C. Fallback
                    if not text_result and not os.path.exists(chart_path):
                        st.warning("The code ran, but didn't print anything or save a chart.")

                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter a question.")
else:
    st.info("Please upload a CSV file to begin.")