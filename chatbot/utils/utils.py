import frappe
import html
import re
import json
from typing import Dict, Any, List


def sanitize_user_input(message: str) -> str:
    """
    Sanitizes and validates user input.
    Returns clean text or raises an exception.
    """
    if not isinstance(message, str):
        frappe.throw("Invalid input type")
    clean_input = html.escape(message.strip())
    if not clean_input:
        return
    sql_injection_patterns = [
        r"\b(SELECT|INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|EXEC|UNION|GRANT|TRUNCATE)\b",
        r"(--|;|')",
    ]
    for pattern in sql_injection_patterns:
        if re.search(pattern, clean_input, re.IGNORECASE):
            frappe.throw("Invalid or unsafe input detected")
    if re.search(r"[\x00-\x08\x0B\x0C\x0E-\x1F]", clean_input):
        frappe.throw("Invalid characters detected")

    return clean_input


CACHE_KEY = "chatbot_conversation_context"
def get_user_context(user: str) -> dict:
    """
    Retrieve user context from cache and deserialize
    """
    cached = frappe.cache().get(f"{CACHE_KEY}:{user}")
    if cached:
        return json.loads(cached)
    return {}

def set_user_context(user: str, context: dict):
    key = f"{CACHE_KEY}:{user}"
    serialized = json.dumps(context)    
    frappe.cache().set(key, serialized)
    frappe.cache().expire(key, 3600)  


def user_intent(clean_input: str, context: Dict[str, Any]) -> str:
    """
    Determines user intent using pattern matching and context.
    Can later integrate ML/NLP models here.
    """
    text = clean_input.lower()

    # Basic intent patterns (can be replaced with ML model prediction)
    patterns = {
        "greeting": r"\b(hello|hi|hey|greetings)\b",
        "help_request": r"\b(help|support|assist|guide|how to)\b",
        "invoice_query": r"\b(invoice|bill|payment|receipt)\b",
        "product_query": r"\b(product|item|stock|price|availability)\b",
        "thanks": r"\b(thank|thanks|thank you)\b",
        "goodbye": r"\b(bye|goodbye|see you)\b",
    }

    for intent, pattern in patterns.items():
        if re.search(pattern, text):
            return intent

    # Fallback: check previous context for follow-up questions
    last_intent = context.get("last_intent")
    if last_intent in ["invoice_query", "product_query"]:
        return last_intent

    return "unknown"

def conversation(clean_input: str, user: str) -> str:
    """
    Handles a conversation turn:
    1. Gets context
    2. Detects intent
    3. Generates response
    4. Updates context
    """
    context = get_user_context(user)
    intent = user_intent(clean_input, context)

    # Define production-ready responses per intent
    responses = {
        "greeting": "Hello 👋! I’m your Kindatech AI assistant. How can I help you today?",
        "help_request": (
            "I can assist you with invoices, products, or general Kindatech questions. "
            "You can ask me things like 'Check invoice status' or 'Tell me about a product'."
        ),
        "invoice_query": "Please provide the invoice number or the customer name so I can check it for you.",
        "product_query": "I can provide product details, stock levels, and pricing. What product are you interested in?",
        "thanks": "You’re welcome! 😊 Do you have any other questions?",
        "goodbye": "Goodbye! If you need assistance again, just click the chatbot.",
        "unknown": "I’m not sure I understand. Could you please rephrase your question?"
    }

    # Update context
    context["last_intent"] = intent
    set_user_context(user, context)

    return responses.get(intent, responses["unknown"])
    
