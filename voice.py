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
    Uses the NATIVE Streamlit Audio Input widget.
    """
    # This creates the official Streamlit recording widget
    audio_value = st.audio_input("Click the mic to record")

    if audio_value:
        # If the user recorded something, save and transcribe it
        st.info("🎧 Transcribing...")
        
        try:
            model = load_whisper_model()
            
            # Save the recorded bytes to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
                temp_audio.write(audio_value.read())
                temp_audio_path = temp_audio.name
            
            # Run Whisper
            result = model.transcribe(temp_audio_path)
            text = result["text"]
            
            # Cleanup
            os.remove(temp_audio_path)
            return text
            
        except Exception as e:
            st.error(f"Error processing audio: {e}")
            return None
            
    return None