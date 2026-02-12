from chatbot.services.settings_service import get_chatbot_settings
from chatbot.providers.deepseek_provider import DeepSeekProvider
from chatbot.providers.openai_provider import OpenAIProvider
from chatbot.providers.grok_provider import GrokProvider
from chatbot.providers.groq_provider import GroqProvider


class AIService:

    @staticmethod
    def generate(message: str):

        settings = get_chatbot_settings()

        provider_map = {
            "DeepSeek": DeepSeekProvider,
            "OpenAI": OpenAIProvider,
            "Grok": GrokProvider,
            "Groq": GroqProvider
        }

        provider_class = provider_map.get(settings.model_provider)

        if not provider_class:
            return "Invalid AI provider configured."

        provider = provider_class(settings.api_key, settings.api_url)

        return provider.generate_response(message)
