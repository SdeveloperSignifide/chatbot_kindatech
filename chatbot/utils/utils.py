import frappe
import html
import re
from .tools import get_deepseek_intent
import json
import os
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



def preprocess_text(text: str) -> str:
    """
    Clean and normalize user input.
    """
    return text.lower().strip()



def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)  # keep only letters and spaces
    text = re.sub(r"\s+", " ", text)      # collapse multiple spaces
    return text.strip()


def check_short_keywords(text: str) -> str | None:
    """
    Detects simple intents like greetings, thanks, goodbye.
    Uses fuzzy matching (keyword is in input) rather than exact match.
    ERP/business intents (like inventory_query, invoice_query) 
    are now handled dynamically by the ML model.
    """

    keywords = {
        "greeting": ["hello", "hi", "hey", "greetings", "good morning", "good afternoon"],
        "thanks": ["thanks", "thank you", "thx", "appreciate it"],
        "goodbye": ["bye", "goodbye", "see you", "see ya"]
    }

    text_clean = normalize_text(text)
    print(f"[DEBUG] Checking keywords for: '{text_clean}'")  

    for intent, words in keywords.items():
        for w in words:
            if w in text_clean:  
                print(f"[DEBUG] Matched intent '{intent}' with keyword '{w}'")
                return intent

    return None



def predict_intent_ml(model, text: str) -> tuple[str, float]:
    """
    Predict intent using ML model and return (intent, confidence).
    """
    probs = model.predict_proba([text])[0]
    labels = model.classes_
    best_idx = probs.argmax()
    return labels[best_idx], probs[best_idx]


def set_user_context(user: str, context: dict):
    key = f"{CACHE_KEY}:{user}"
    serialized = json.dumps(context)    
    frappe.cache().set(key, serialized)
    frappe.cache().expire(key, 3600)  


from typing import Dict, Any
import joblib
from functools import lru_cache

CONFIDENCE_THRESHOLD = 0.5  # tweakable

import os
import re
import joblib
from functools import lru_cache
from typing import Dict, Any

CONFIDENCE_THRESHOLD <= 0.5  

@lru_cache(maxsize=1)
def load_intent_model():
    base_dir = os.path.dirname(os.path.abspath(__file__))  
    model_path = os.path.join(base_dir, "../ml/intent_model.joblib")
    model_path = os.path.abspath(model_path)

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Intent model not found at {model_path}")

    return joblib.load(model_path)


def preprocess_input(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)  
    text = re.sub(r"\s+", " ", text)  
    return text.strip()


def user_intent(clean_input: str, context: dict) -> str:
    """
    Detect user intent using DeepSeek REST API.
    """
    text = preprocess_input(clean_input)
    print("The user text is:", text)

    # 1️⃣ Check short keywords first
    intent = check_short_keywords(text)
    if intent:
        return intent

    # 2️⃣ Call DeepSeek API
    prediction = get_deepseek_intent(text)
    intent = prediction.get("label", "unknown")
    confidence = prediction.get("score", 0.0)

    if confidence < 0.5:  # fallback if low confidence
        last_intent = context.get("last_intent")
        if last_intent not in ["greeting", "thanks", "goodbye"]:
            return last_intent
        return "unknown"

    return intent



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

    print("Hello the intent captured is", intent)

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
    

