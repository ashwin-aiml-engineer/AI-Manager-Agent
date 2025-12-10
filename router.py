import os
from litellm import completion
from config import CURRENT_CONFIG

def route_query(query):
    """
    Determines if the query is for the 'legal' dept, 'data' dept, or 'general' chat.
    """
    model_name = f"ollama/{CURRENT_CONFIG['manager_model']}"
    ollama_url = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")

    # 🧠 SYSTEM PROMPT: The Routing Logic
    system_prompt = """
    You are the Manager of an AI Agency. Route the user's query to the correct department.
    
    DEPARTMENTS:
    1. 'legal': ONLY for questions about the "Industrial Disputes Act", laws, sections, courts, or legal drafting.
    2. 'data': ONLY for requests to "plot", "graph", "chart", "analyze csv", or "calculate" numbers from a file.
    3. 'general': For everything else.
    
    CRITICAL RULES:
    - If the user asks for BOTH (e.g., "Graph this AND explain law"), route to 'general'.
    - If the query is messy, unclear, or gibberish, route to 'general'.
    - If the query is just "Hello" or conversational, route to 'general'.
    
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