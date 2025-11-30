# core/ai_client.py
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

# choose a model you have access to
MODEL_NAME = "gemini-2.5-flash"

_model = genai.GenerativeModel(MODEL_NAME)

def ask_model(prompt: str, max_output_chars: int = 4000) -> str:
    """
    Send prompt to Gemini and return the text output.
    """
    try:
        resp = _model.generate_content(prompt)
        # resp may have text accessible in .text or .output_text depending on SDK; handle common cases
        if hasattr(resp, "text"):
            return resp.text
        if hasattr(resp, "output_text"):
            return resp.output_text
        # fallback to string conversion:
        return str(resp)
    except Exception as e:
        return f"[Error] {e}"
