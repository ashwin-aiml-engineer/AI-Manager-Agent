import streamlit as st
import whisper
import os
import tempfile

# Load the model only once
@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")

def record_voice_widget():
    """
    Uses the NATIVE Streamlit Audio Input with Auto-Cleanup.
    """
    audio_value = st.audio_input("Click the mic to record")

    if audio_value:
        # 1. Create a placeholder for the status message
        status_box = st.empty()
        
        # 2. Show the message inside the box
        status_box.info("🎧 Transcribing... (Please wait)")
        
        try:
            model = load_whisper_model()
            
            # Save raw audio
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
                temp_audio.write(audio_value.read())
                temp_audio_path = temp_audio.name
            
            # Transcribe
            result = model.transcribe(temp_audio_path)
            text = result["text"].strip()
            
            # Cleanup File
            os.remove(temp_audio_path)
            
            # --- 🛡️ HALLUCINATION FILTER ---
            hallucinations = [
                "Subtitles by", "Amara.org", "Thank you", "you", 
                "Sunscreen", "traffic", "Guide", "MBC"
            ]
            
            # Check for garbage output
            if any(h.lower() in text.lower() for h in hallucinations) and len(text.split()) < 5:
                status_box.warning(f"⚠️ Ignored background noise.")
                return None
            
            if len(text) < 2:
                status_box.empty() # Clear box if empty
                return None

            # 3. SUCCESS! Clear the "Transcribing" message immediately
            status_box.empty() 
            return text
            
        except Exception as e:
            status_box.error(f"Error: {e}")
            return None
            
    return None