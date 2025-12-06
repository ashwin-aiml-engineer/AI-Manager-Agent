import os
import shutil
from langchain.vectorstores import Chroma
from langchain.embeddings import OllamaEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# --- CONFIGURATION ---
PDF_FILE = "data.pdf"
DB_FOLDER = "vector_db"
MODEL_NAME = "nomic-embed-text"

def main():
    print("🧠 STARTING BRAIN RE-BUILD...")
    
    # 1. Clean up old mess
    if os.path.exists(DB_FOLDER):
        print(f"🗑️ Deleting incompatible '{DB_FOLDER}'...")
        shutil.rmtree(DB_FOLDER)

    # 2. Load PDF
    if not os.path.exists(PDF_FILE):
        print(f"❌ ERROR: '{PDF_FILE}' not found. Please copy it here.")
        return
    
    print(f"📄 Loading '{PDF_FILE}'...")
    loader = PyPDFLoader(PDF_FILE)
    docs = loader.load()
    print(f"   - Found {len(docs)} pages.")

    # 3. Split Text
    print("✂️ Splitting text into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(docs)
    print(f"   - Created {len(chunks)} chunks.")

    # 4. Create Database (using the STABLE libraries)
    print("💾 Saving to Vector Database (this works with your current setup)...")
    embeddings = OllamaEmbeddings(model=MODEL_NAME)
    
    # Create and Persist
    vector_store = Chroma.from_documents(
        documents=chunks, 
        embedding=embeddings, 
        persist_directory=DB_FOLDER
    )
    vector_store.persist()
    
    print("✅ SUCCESS! New compatible brain created.")

if __name__ == "__main__":
    main()