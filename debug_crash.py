import os
import sys

print("--- DEBUG START ---")

print("1. Importing libraries...")
try:
    from langchain_community.vectorstores import Chroma
    from langchain_community.embeddings import OllamaEmbeddings
    print("   ✅ Imports successful.")
except Exception as e:
    print(f"   ❌ Import Failed: {e}")
    sys.exit()

print("2. Checking folder...")
if os.path.exists("vector_db"):
    print("   ✅ 'vector_db' folder found.")
else:
    print("   ❌ 'vector_db' folder MISSING.")
    sys.exit()

print("3. Loading Brain (This is where it usually crashes)...")
try:
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    db = Chroma(persist_directory="vector_db", embedding_function=embeddings)
    print("   ✅ Brain loaded.")
except Exception as e:
    print(f"   ❌ Brain Load Failed: {e}")
    sys.exit()

print("4. Testing Search...")
try:
    results = db.similarity_search("test", k=1)
    print("   ✅ Search worked!")
except Exception as e:
    print(f"   ❌ Search Failed: {e}")

print("--- DEBUG FINISHED: SUCCESS ---")