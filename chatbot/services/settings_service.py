import frappe
from typing import Optional

class ChatbotSettings:
    def __init__(self, model_provider: str, api_key: str, api_url: Optional[str] = None):
        self.model_provider = model_provider
        self.api_key = api_key
        self.api_url = api_url


def get_chatbot_settings() -> ChatbotSettings:
    """
    Fetch the latest active Chatbot Settings (is_active=1) using get_all only.
    Assumes API key is a normal field (not password field).
    """
    settings_list = frappe.get_all(
        "Chatbot Settings",
        filters={"is_active": 1},
        fields=["model_provider", "api_key", "api_url"],
        order_by="creation desc",
        limit_page_length=1
    )

    if not settings_list:
        frappe.throw("No active Chatbot Settings found. Please activate one.")

    settings = settings_list[0]

    if not (settings.get("model_provider") and settings.get("api_key")):
        frappe.throw("Active Chatbot Settings must have a model_provider and an api_key configured.")

    return ChatbotSettings(
        model_provider=settings["model_provider"],
        api_key=settings["api_key"],
        api_url=settings.get("api_url")
    )

CACHE_KEY = "chatbot_conversation_context"


def get_user_context(user: str) -> dict:
    cached = frappe.cache().get(f"{CACHE_KEY}:{user}")
    if cached:
        import json
        return json.loads(cached)
    return {}

def set_user_context(user: str, context: dict):
    import json
    key = f"{CACHE_KEY}:{user}"
    serialized = json.dumps(context)
    frappe.cache().set(key, serialized)
    frappe.cache().expire(key, 3600)