import streamlit as st
import ollama
from pypdf import PdfReader

def extract_text(uploaded_file):
    """
    Reads the uploaded PDF file page by page and returns the raw text.
    """
    try:
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def optimize_resume(resume_text, job_description):
    """
    Sends the resume + JD to Gemma 2 (9b) for optimization.
    """
    
    # 🎯 The Prompt: We tell Gemma exactly how to behave.
    prompt = f"""
    You are an expert Career Consultant and Resume Writer specialized in beating ATS (Applicant Tracking Systems).
    
    TASK:
    Rewrite the 'Professional Summary' and 'Key Skills' sections of the candidate's resume to perfectly match the target Job Description.
    
    RULES:
    1. Do NOT invent false experiences. Use the candidate's existing background.
    2. Incorporate specific keywords from the Job Description naturally.
    3. Keep the tone professional, confident, and human.
    4. Provide the output in Markdown format.
    
    ------------
    TARGET JOB DESCRIPTION:
    {job_description}
    ------------
    CANDIDATE'S RESUME TEXT:
    {resume_text}
    ------------
    
    OPTIMIZED CONTENT:
    """

    # We use a spinner so the user knows the AI is thinking
    with st.spinner("✨ Gemma is analyzing your profile..."):
        try:
            response = ollama.chat(
                model='gemma2:9b', 
                messages=[{'role': 'user', 'content': prompt}]
            )
            return response['message']['content']
        except Exception as e:
            return f"Error connecting to AI: {str(e)}"

def render_ats_page():
    """
    This function renders the UI for the Resume tab.
    """
    st.header("📄 Resume ATS Optimizer")
    st.markdown("### beat the bot. Get the Interview.")
    st.info("Upload your current resume and paste the job description you want. Gemma 2 will rewrite your Summary & Skills to match.")

    # Two columns layout
    col1, col2 = st.columns(2)
    
    with col1:
        uploaded_file = st.file_uploader("1. Upload Resume (PDF)", type="pdf")
    
    with col2:
        job_desc = st.text_area("2. Paste Job Description", height=200, placeholder="Paste the LinkedIn/Naukri JD here...")

    # The Trigger Button
    if st.button("🚀 Optimize My Resume"):
        if uploaded_file and job_desc:
            # Step A: Extract Text
            raw_text = extract_text(uploaded_file)
            
            # Step B: Generate
            if len(raw_text) > 50: # Basic check to ensure PDF wasn't empty
                optimized_text = optimize_resume(raw_text, job_desc)
                
                # Step C: Display Result
                st.success("Optimization Complete!")
                st.subheader("Your New Profile Sections:")
                st.markdown(optimized_text)
                st.caption("Copy and paste these sections into your Word doc.")
            else:
                st.error("Could not read text from the PDF. Is it a scanned image?")
            
        else:
            st.warning("Please upload a PDF and paste a Job Description first.")