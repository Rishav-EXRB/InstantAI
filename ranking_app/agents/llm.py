import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class GroqClient:
    def __init__(self, model="llama-3.3-70b-versatile"):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        self.client = Groq(api_key=self.api_key)
        self.model = model

    def chat(self, messages, temperature=0.1, max_tokens=2048, response_format=None):
        """
        Send a chat completion request to Groq.
        """
        try:
            params = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
            }
            if response_format:
                params["response_format"] = response_format
                
            completion = self.client.chat.completions.create(**params)
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error calling Groq API: {str(e)}"

# Singleton instance
_llm_instance = None

def get_llm():
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = GroqClient()
    return _llm_instance
