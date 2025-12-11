import os
import glob
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import (
    PyPDFLoader, 
    Docx2txtLoader, 
    UnstructuredPowerPointLoader,
    TextLoader,     
    CSVLoader     
)
from langchain_text_splitters import RecursiveCharacterTextSplitter

# --- CONFIGURATION ---
DATA_PATH = "data"
DB_PATH = "vector_db"
OLLAMA_URL = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")
BATCH_SIZE = 5

def get_existing_files(vector_store):
    """Asks the database: 'What files do you already have?'"""
    try:
        data = vector_store.get(include=['metadatas'])
        existing_sources = set()
        for meta in data['metadatas']:
            if meta and 'source' in meta:
                existing_sources.add(meta['source'])
        return existing_sources
    except Exception:
        return set() 

def load_documents(existing_files):
    documents = []
    all_files = glob.glob(os.path.join(DATA_PATH, "*.*"))
    new_files = [f for f in all_files if f not in existing_files]
    
    if not new_files:
        return []

    print(f"📂 Found {len(new_files)} NEW files to process...")

    for file_path in new_files:
        ext = os.path.splitext(file_path)[1].lower()
        loader = None
        try:
            if ext == ".pdf":
                print(f"   - Loading PDF: {file_path}")
                loader = PyPDFLoader(file_path)
            elif ext == ".docx":
                print(f"   - Loading Word: {file_path}")
                loader = Docx2txtLoader(file_path)
            elif ext == ".pptx":
                print(f"   - Loading PPT: {file_path}")
                loader = UnstructuredPowerPointLoader(file_path)
            elif ext == ".txt":
                print(f"   - Loading Text: {file_path}")
                loader = TextLoader(file_path, encoding="utf-8")
            elif ext == ".csv":
                print(f"   - Loading CSV as Text: {file_path}")
                loader = CSVLoader(file_path)    
            
            if loader:
                documents.extend(loader.load())
        except Exception as e:
            print(f"❌ Error loading {file_path}: {e}")
            
    return documents

def ingest():
    print("🚀 STARTING INCREMENTAL INGESTION...")
    embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url=OLLAMA_URL)
    
    # 1. Connect to Existing DB
    vector_store = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
    
    # 2. Check & Load
    existing_files = get_existing_files(vector_store)
    raw_docs = load_documents(existing_files)
    
    if not raw_docs:
        print("✅ System is up to date. No new files to digest.")
        return

    # 3. Split & Embed
    print(f"🔪 Splitting {len(raw_docs)} new documents...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(raw_docs)
    total_chunks = len(chunks)
    
    print("🧠 Embedding new data...")
    for i in range(0, total_chunks, BATCH_SIZE):
        batch = chunks[i : i + BATCH_SIZE]
        vector_store.add_documents(batch)
        vector_store.persist()
        print(f"   ⏳ Added {min(i + BATCH_SIZE, total_chunks)}/{total_chunks} chunks...")

    print("✅ SUCCESS! Knowledge Base Updated.")

if __name__ == "__main__":
    ingest()