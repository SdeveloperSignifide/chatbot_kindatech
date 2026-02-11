from .tools import get_ai_reply
import frappe
import html
import re
import json
import random
CACHE_KEY = "chatbot_conversation_context"


def sanitize_user_input(message: str) -> str:
    """
    Sanitizes and validates user input.
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


def get_user_context(user: str) -> dict:
    cached = frappe.cache().get(f"{CACHE_KEY}:{user}")
    if cached:
        return json.loads(cached)
    return {}


def set_user_context(user: str, context: dict):
    key = f"{CACHE_KEY}:{user}"
    serialized = json.dumps(context)
    frappe.cache().set(key, serialized)
    frappe.cache().expire(key, 3600)


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def check_short_keywords(text: str) -> str | None:
    """
    Detect simple intents like greetings, thanks, goodbye.
    Extended greetings include "how are you", "how are you doing", etc.
    """
    text_clean = normalize_text(text)

    greeting_keywords = [
        "hello", "hi", "hey", "greetings", "good morning", "good afternoon",
        "how are you", "how are you doing", "how's it going", "how are you feeling"
    ]
    thanks_keywords = ["thanks", "thank you", "thx", "appreciate it"]
    goodbye_keywords = ["bye", "goodbye", "see you", "see ya"]

    for kw in greeting_keywords:
        if kw in text_clean:
            return "greeting"
    for kw in thanks_keywords:
        if kw in text_clean:
            return "thanks"
    for kw in goodbye_keywords:
        if kw in text_clean:
            return "goodbye"

    return None




def user_intent(clean_input: str, context: dict) -> str:
    """
    Detect intent. All greeting keywords return 'greeting' directly.
    Other intents are determined via LLM.
    """
    intent = check_short_keywords(clean_input)
    if intent == "greeting":
        # Always return 'greeting' without calling LLM
        return "greeting"

    if intent:
        return intent

    # Non-greeting intents: call LLM
    ai_response = get_ai_reply(clean_input, "determine_intent")
    return normalize_text(ai_response) or "unknown"



def conversation(clean_input: str, user: str) -> str:
    """
    Main conversation flow with random greetings.
    """
    context = get_user_context(user)

    intent = user_intent(clean_input, context)
    print("Intent captured:", intent)

    if intent == "greeting":
        greeting_replies = [
            "Hello! How can I assist you today?",
            "Hi there! What can I do for you?",
            "Hey! How's it going?",
            "Greetings! How may I help you?",
            "Good day! How can I be of service?",
            "Hello! Ready to help you with anything you need.",
            "Hi! What can I help you with today?",
            "Hey! Hope you're doing well today.",
            "Hello! How are you feeling today?"
        ]
        reply = random.choice(greeting_replies)
    elif intent == "thanks":
        thanks_replies = [
            "You're welcome!", "No problem!", "Happy to help!", "Anytime!"
        ]
        reply = random.choice(thanks_replies)
    elif intent == "goodbye":
        goodbye_replies = [
            "Goodbye! Have a great day!", "See you later!", "Bye! Take care!"
        ]
        reply = random.choice(goodbye_replies)
    else:
        # Non-greeting intents: call LLM
        reply = get_ai_reply(clean_input, intent)

    context["last_intent"] = intent
    set_user_context(user, context)

    return reply

