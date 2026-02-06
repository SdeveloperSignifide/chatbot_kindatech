import frappe

import requests

def get_deepseek_intent(text: str) -> dict:
    """
    Call DeepSeek REST API to get intent predictions.
    Returns a dict: {'label': intent_name, 'score': confidence}
    """
    settings = frappe.get_doc("Chatbot Settings")
    api_key = settings.api_keys  # adjust if your fieldname is different
    if not api_key:
        frappe.throw("DeepSeek API key is not configured in Chatbot Settings")

    url = "https://api.deepseek.ai/v1/intent"  # replace with actual DeepSeek endpoint
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "text": text
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=5)
        response.raise_for_status()
        data = response.json()

        # Example response: {"predictions": [{"label": "invoice_query", "score": 0.93}]}
        if "predictions" in data and data["predictions"]:
            return data["predictions"][0]
        return {"label": "unknown", "score": 0.0}

    except Exception as e:
        frappe.log_error(f"DeepSeek API error: {str(e)}", "Chatbot DeepSeek")
        return {"label": "unknown", "score": 0.0}





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


