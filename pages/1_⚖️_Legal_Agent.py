import streamlit as st
from litellm import completion

# 1. Page Configuration
st.set_page_config(page_title="Legal Advisor Agent", page_icon="⚖️", layout="wide")

st.title("⚖️ Legal Advisor Agent")
st.markdown("Powered by **Llama 3.1** (Local AI)")
st.info("⚠️ **Disclaimer:** I am an AI, not a human lawyer. Use my answers for information only, not as professional legal advice.")

# 2. Sidebar Task Selector
with st.sidebar:
    st.header("Legal Toolkit")
    task_type = st.radio("Select Task:", ["General Legal Advice", "Contract Review", "Draft Legal Letter"])

# 3. Main Logic
# A. Contract Review Mode
if task_type == "Contract Review":
    st.subheader("📝 Contract Reviewer")
    contract_text = st.text_area("Paste the contract text here:", height=300)
    user_question = st.text_input("What specific risks should I look for?", value="Identify key risks, termination clauses, and indemnity obligations.")
    
    if st.button("Review Contract"):
        if contract_text:
            with st.spinner("🤖 Llama 3.1 is reading the contract..."):
                try:
                    # Specialized Prompt for Contracts
                    prompt = f"""
                    You are a Senior Corporate Lawyer. Review the following contract text.
                    
                    Contract Text:
                    "{contract_text}"
                    
                    User Request: {user_question}
                    
                    Please provide a professional legal review.
                    Structure your answer with:
                    1. 🚩 **Key Risks** (Bullet points)
                    2. 🛑 **Red Flags** (Clauses to watch out for)
                    3. ✅ **Recommendations** (What to negotiate)
                    
                    Keep the tone professional, objective, and precise.
                    """
                    
                    response = completion(
                        model="ollama/llama3.1", 
                        messages=[{"role": "user", "content": prompt}],
                        api_base="http://localhost:11434",
                        stream=True
                    )
                    
                    # Stream the output for a "typing" effect
                    st.write_stream(chunk['choices'][0]['delta']['content'] for chunk in response if chunk['choices'][0]['delta']['content'])
                    
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please paste some contract text first.")

# B. General Advice & Drafting Modes
else:
    if task_type == "Draft Legal Letter":
        st.subheader("✍️ Legal Drafter")
        query = st.text_area("Describe the situation (e.g., 'Draft a cease and desist for copyright infringement'):")
    else:
        st.subheader("⚖️ General Legal Q&A")
        query = st.text_area("Ask a legal question:")

    if st.button("Submit"):
        if query:
            with st.spinner("🤖 Llama 3.1 is thinking..."):
                try:
                    # Specialized Prompt for General Law
                    system_role = "You are a professional lawyer. Provide clear, accurate legal information based on general legal principles. Always include a disclaimer."
                    
                    response = completion(
                        model="ollama/llama3.1", 
                        messages=[
                            {"role": "system", "content": system_role},
                            {"role": "user", "content": query}
                        ],
                        api_base="http://localhost:11434",
                        stream=True
                    )
                    
                    st.write_stream(chunk['choices'][0]['delta']['content'] for chunk in response if chunk['choices'][0]['delta']['content'])
                    
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter a prompt.")