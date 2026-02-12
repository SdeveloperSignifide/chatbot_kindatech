import requests
from chatbot.providers.base_provider import BaseProvider
from chatbot.utils.logger import log_error
from chatbot.configurations import FALLBACK_MESSAGE



class OpenAIProvider(BaseProvider):

    def __init__(self, api_key, api_url):
        self.api_key = api_key
        self.api_url = api_url

    def generate_response(self, message: str) -> str:
        try:
            response = requests.post(
                self.api_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-4o-mini",
                    "messages": [{"role": "user", "content": message}]
                },
                timeout=30
            )

            if response.status_code != 200:
                log_error(f"OpenAI Error {response.status_code}: {response.text}")
                return FALLBACK_MESSAGE

            data = response.json()
            # Safely get content
            choices = data.get("choices")
            if choices and len(choices) > 0:
                return choices[0].get("message", {}).get("content", FALLBACK_MESSAGE)

            return FALLBACK_MESSAGE

        except Exception as e:
            log_error(f"OpenAI Exception: {str(e)}")
            return FALLBACK_MESSAGE
