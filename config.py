# config.py

# =========================================================
# 🎛️ THE SOVEREIGN AGENCY CONTROL PANEL
# =========================================================
# CHANGE THIS TO SWITCH VERSIONS:
# Options: "PRO" (Requires 32GB RAM) or "LITE" (Runs on 8GB RAM)
VERSION_TIER = "PRO" 

# =========================================================
# ⚙️ CONFIGURATION RULES
# =========================================================
SETTINGS = {
    "LITE": {
        # TIER A: Software-Only (The "Budget" Version)
        # Uses only Llama 3.1 for everything. No Qwen, No Gemma.
        "manager_model": "llama3.1",       
        "resume_model": "llama3.1",        # Less creative, but functional
        "data_agent_model": "llama3.1",    # Weaker at coding
        "allow_data_analysis": False,      # DISABLES the Data Agent (Upsell feature)
        "system_name": "AI Agency LITE"
    },
    
    "PRO": {
        # TIER B: The AI Box (The "Premium" Version)
        # Uses specific specialist models for maximum performance.
        "manager_model": "qwen2.5-coder:32b", # The Big Brain
        "resume_model": "gemma2:9b",          # The Creative Writer
        "data_agent_model": "qwen2.5-coder:32b",
        "allow_data_analysis": True,          # ENABLES Python execution
        "system_name": "AI Agency PRO (Sovereign Edition)"
    }
}

# Load the active configuration
CURRENT_CONFIG = SETTINGS[VERSION_TIER]