import frappe
import requests

def get_ai_reply(text: str, intent: str) -> str:
    """
    Generate AI response using DeepSeek based on detected intent.
    Fetches the last Chatbot Settings record.
    """
    settings_list = frappe.get_all(
        "Chatbot Settings",
        fields=["name", "api_keys"],
        order_by="creation desc",
        limit_page_length=1
    )

    if not settings_list:
        frappe.throw("No Chatbot Settings record found")

    settings_name = settings_list[0].name
    settings = frappe.get_doc("Chatbot Settings", settings_name)
    api_key = settings.api_keys

    if not api_key:
        frappe.throw("DeepSeek API key not configured in the last Chatbot Settings record")

    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    system_prompt = (
        "You are Kindatech AI, an ERPNext assistant. "
        f"The detected intent is: {intent}. "
        "Respond professionally and helpfully."
    )

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ],
        "temperature": 0.7,
        "max_tokens": 300
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        print("Status Code:", response.status_code)
        print("Response Text:", response.text)
        response.raise_for_status()
        data = response.json()
        print("Response JSON:", data)
        return data["choices"][0]["message"]["content"]

    except Exception as e:
        frappe.log_error(str(e), "DeepSeek Response Error")
        return "Sorry, I'm experiencing an issue generating a response."


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


