import sys
from litellm import completion

# --- CONFIGURATION ---
# We use Qwen because it follows strict "classification" instructions perfectly.
ROUTER_MODEL = "ollama/qwen2.5-coder:32b" 

def route_query(user_query):
    """
    Analyzes the user's input and decides which agent should handle it.
    Returns: 'legal', 'data', or 'general'
    """
    
    # 1. THE ROUTING SYSTEM PROMPT
    # We give the AI a "Persona" of a Traffic Controller.
    system_prompt = """
    You are an intelligent Router Agent. Your ONLY job is to classify user queries.
    
    CATEGORIES:
    1. 'legal': Questions about laws, acts (Industrial Disputes, etc), drafting notices, contracts, courts, or firing employees.
    2. 'data': Questions about CSV files, sales numbers, plotting charts, trends, or datasets.
    3. 'general': Simple greetings like "hi", "hello", or questions unrelated to law/data.

    RULES:
    - Return ONLY one word: 'legal', 'data', or 'general'.
    - Do NOT write explanations.
    - Do NOT output markdown or punctuation.
    """

    try:
        # 2. CALL THE LOCAL MODEL
        response = completion(
            model=ROUTER_MODEL, 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            api_base="http://localhost:11434"
        )
        
        # 3. CLEAN THE OUTPUT
        # Qwen is usually good, but we lowercase and strip spaces just in case.
        decision = response['choices'][0]['message']['content'].strip().lower()
        
        # 4. VALIDATION
        if "legal" in decision: return "legal"
        if "data" in decision: return "data"
        return "general"

    except Exception as e:
        print(f"❌ Router Error: {e}")
        return "general"

# --- TEST AREA (This runs only when you execute this file directly) ---
if __name__ == "__main__":
    print(f"🤖 Manager Agent Online (Brain: {ROUTER_MODEL})\n")
    print("Type a command to see where I send it (or 'exit').")
    
    while True:
        user_input = input("\n🗣️ User: ")
        if user_input.lower() == 'exit': break
        
        # Run the Router
        destination = route_query(user_input)
        
        # Visual Feedback
        if destination == "legal":
            print("   ↳ ⚖️ Routing to LEGAL AGENT...")
        elif destination == "data":
            print("   ↳ 📊 Routing to DATA ANALYST...")
        else:
            print("   ↳ 🤖 Routing to GENERAL CHAT...")