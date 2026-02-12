import frappe

import json

def get_user_context(user: str) -> dict:
    """
    Retrieve user-specific conversation context from DB.
    """
    doc = frappe.get_all(
        "Chatbot Conversation",
        filters={"user": user},
        fields=["name", "context"],
        limit_page_length=1,
        order_by="modified desc"
    )
    if not doc:
        return {}

    context_str = doc[0].get("context", "{}")
    try:
        return json.loads(context_str)
    except Exception:
        return {}


def set_user_context(user: str, context: dict):
    """
    Save user-specific conversation context in DB.
    """
    context_str = json.dumps(context)

    # Check if a conversation already exists
    existing = frappe.get_all(
        "Chatbot Conversation",
        filters={"user": user},
        fields=["name"],
        limit_page_length=1
    )

    if existing:
        # Update existing record
        doc = frappe.get_doc("Chatbot Conversation", existing[0]["name"])
        doc.context = context_str
        doc.save()
    else:
        # Create new record
        doc = frappe.get_doc({
            "doctype": "Chatbot Conversation",
            "user": user,
            "context": context_str
        })
        doc.insert()