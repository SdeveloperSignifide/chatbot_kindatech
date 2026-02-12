import frappe
import requests
from typing import Optional, Dict, Any

def parse_ai_response(data: dict, provider: str) -> str:
    if not data or "choices" not in data or len(data["choices"]) == 0:
        return ""
    choice = data["choices"][0]
    if provider in ["DeepSeek", "OpenAI"]:
        return choice.get("message", {}).get("content", "")
    elif provider == "Grok":
        return choice.get("text", "")
    return str(choice)

im good you ?

def get_ai_reply(text: str, intent: str) -> str:
    settings_list = frappe.get_all(
        "Chatbot Settings",
        fields=["name", "model_provider", "api_keys", "api_url"],
        order_by="creation desc",
        limit_page_length=1
    )

    if not settings_list:
        frappe.throw("No Chatbot Settings record found.")

    settings = frappe.get_doc("Chatbot Settings", settings_list[0].name)
    provider: str = settings.model_provider
    api_key: str = settings.api_keys
    api_url: Optional[str] = settings.api_url

    if not provider or not api_key:
        frappe.throw(f"{provider or 'AI provider'} API key not configured.")

    system_prompt = (
        "You are Kindatech AI, an ERPNext assistant. "
        f"The detected intent is: {intent}. "
        "Respond professionally, helpfully, and concisely."
    )

    provider_configs: Dict[str, Dict[str, Any]] = {
        "DeepSeek": {"url": api_url or "https://api.deepseek.com/v1/chat/completions", "model": "deepseek-chat"},
        "OpenAI": {"url": api_url or "https://api.openai.com/v1/chat/completions", "model": "gpt-3.5-turbo"},
        "Grok": {"url": api_url or "https://api.grok.ai/v1/chat/completions", "model": "grok-chat"}
    }

    if provider not in provider_configs:
        return f"Provider '{provider}' not supported."

    config = provider_configs[provider]
    url = config["url"]
    model = config["model"]
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ],
        "temperature": 0.7,
        "max_tokens": 300
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        data = response.json()
        return parse_ai_response(data, provider) or "Sorry, I'm experiencing an issue generating a response."

    except requests.HTTPError as e:
        status_code = e.response.status_code if e.response else "unknown"
        error_text = e.response.text if e.response else str(e)
        print(f"[ERROR] {provider} HTTP {status_code}: {error_text}")
        frappe.log_error(f"HTTP {status_code}: {error_text}", f"{provider} HTTPError")
        return f"Sorry, {provider} is currently unavailable (HTTP {status_code})."

    except Exception as e:
        print(f"[ERROR] {provider} GeneralError: {str(e)}")
        frappe.log_error(str(e), f"{provider} GeneralError")
        return f"Sorry, {provider} is experiencing an issue."


def looks_like_inventory_question(text: str) -> bool:
    patterns = [
        r"do you have",
        r"is there",
        r"available",
        r"in stock",
        r"have any",
    ]
    return any(p in text for p in patterns)

def extract_product_candidate(text: str) -> str | None:
    stop_words = {"do", "you", "have", "any", "is", "there", "in", "stock"}
    words = text.split()
    candidates = [w for w in words if w not in stop_words]
    return " ".join(candidates) if candidates else None

    


