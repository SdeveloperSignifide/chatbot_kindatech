import requests
from chatbot.providers.base_provider import BaseProvider
from chatbot.utils.logger import log_error
from chatbot.configurations import FALLBACK_MESSAGE

class GrokProvider(BaseProvider):

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
                    "model": "grok-1",
                    "messages": [{"role": "user", "content": message}]
                },
                timeout=30
            )

            if response.status_code != 200:
                log_error(f"Grok Error {response.status_code}: {response.text}")
                return FALLBACK_MESSAGE

            return response.json()["choices"][0]["message"]["content"]

        except Exception as e:
            log_error(f"Grok Exception: {str(e)}")
            return FALLBACK_MESSAGE
