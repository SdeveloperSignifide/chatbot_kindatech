import frappe
import json

MEMORY_LIMIT = 5  # last 5 exchanges

def get_session_id():
    return frappe.session.sid or "guest"

def get_memory():
    sid = get_session_id()
    cache = frappe.cache()
    memory = cache.get_value(f"chatbot_memory:{sid}")
    return json.loads(memory) if memory else []

def save_memory(user_msg, bot_reply):
    sid = get_session_id()
    cache = frappe.cache()

    memory = get_memory()
    memory.append({
        "user": user_msg,
        "bot": bot_reply
    })

    memory = memory[-MEMORY_LIMIT:]
    cache.set_value(f"chatbot_memory:{sid}", json.dumps(memory))
