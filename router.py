import os
import json
from litellm import completion
from config import CURRENT_CONFIG  # <--- NEW IMPORT

def route_query(query):
    """
    Decides whether to send the user to 'legal', 'data', or 'general'.
    """
    
    # 1. Use the Model defined in Config
    MODEL_NAME = f"ollama/{CURRENT_CONFIG['manager_model']}"

    prompt = f"""
    You are an Intelligent Router. Classify the user's query into one of three categories:
    1. 'legal': Questions about law, the Industrial Disputes Act, drafting notices, or regulations.
    2. 'data': Requests to analyze CSV files, plot charts, calculate averages, or visualize data.
    3. 'general': Anything else (greetings, resume help, general questions).

    User Query: "{query}"

    OUTPUT ONLY A JSON OBJECT: {{"category": "..."}}
    """
    
    try:
        response = completion(
            model=MODEL_NAME,  # <--- USES CONFIG NOW
            messages=[{"role": "user", "content": prompt}],
            api_base=os.getenv("OLLAMA_API_BASE", "http://localhost:11434"),
            options={"num_gpu": 0} 
        )
        
        content = response['choices'][0]['message']['content']
        
        # Clean the response to ensure valid JSON
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
            
        decision = json.loads(content)
        return decision.get("category", "general")

    except Exception as e:
        print(f"Router Error: {e}")
        return "general"