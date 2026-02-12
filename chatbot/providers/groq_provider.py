import requests
from chatbot.providers.base_provider import BaseProvider
from chatbot.utils.logger import log_error
from chatbot.configurations import FALLBACK_MESSAGE



class GroqProvider(BaseProvider):
    """
    Groq AI provider integration.
    Expects API key and optional custom API URL.
    """

    def __init__(self, api_key: str, api_url: str = "https://api.groq.com/openai/v1/chat/completions"):
        self.api_key = api_key
        self.api_url = api_url

    def generate_response(self, message: str) -> str:
        try:
            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": message}]
            }

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)

            if response.status_code != 200:
                log_error(f"Groq Error {response.status_code}: {response.text}")
                return FALLBACK_MESSAGE

            data = response.json()

            # Safely extract the assistant message
            choices = data.get("choices")
            if choices and len(choices) > 0:
                return choices[0].get("message", {}).get("content", FALLBACK_MESSAGE)

            return FALLBACK_MESSAGE

        except Exception as e:
            log_error(f"Groq Exception: {str(e)}")
            return FALLBACK_MESSAGE
