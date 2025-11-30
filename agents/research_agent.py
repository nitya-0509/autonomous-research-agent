from core.ai_client import ask_model

class ResearchAgent:
    def __init__(self):
        pass

    def process(self, prompt: str):
        """
        Simply passes user request to Gemini model.
        """
        return ask_model(prompt)
