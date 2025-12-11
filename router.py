import os
from litellm import completion
from config import CURRENT_CONFIG

def route_query(query):
    """
    Determines if the query is for the 'legal' (Knowledge Base), 'data' dept, or 'general' chat.
    """
    model_name = f"ollama/{CURRENT_CONFIG['manager_model']}"
    ollama_url = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")

    # 🧠 SYSTEM PROMPT: The Routing Logic (UPDATED)
    system_prompt = """
    You are the Manager of an AI Agency. Route the user's query to the correct department.
    
    DEPARTMENTS:
    1. 'legal': Use this for ANY question that requires looking up documents, laws, the "Industrial Disputes Act", OR information about "Project Sovereign" or the agency itself.
    2. 'data': ONLY for requests to "plot", "graph", "chart", "analyze csv", or "calculate" numbers from a file.
    3. 'general': For casual greetings like "hello", "hi", or questions unrelated to the business context.
    
    CRITICAL RULES:
    - If the user asks "Who founded Project Sovereign?", route to 'legal' (so it checks the files).
    - If unsure, route to 'general'.
    
    OUTPUT FORMAT:
    Return ONLY one word: 'legal', 'data', or 'general'. Do not add punctuation.
    """
    
    try:
        response = completion(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            api_base=ollama_url,
            options={"num_gpu": 0}
        )
        
        # Clean the output (remove spaces, punctuation)
        decision = response['choices'][0]['message']['content'].strip().lower()
        
        # Fallback if the model gives a weird answer
        if "legal" in decision: return "legal"
        if "data" in decision: return "data"
        return "general"

    except Exception as e:
        print(f"Router Error: {e}")
        return "general" # Safety net