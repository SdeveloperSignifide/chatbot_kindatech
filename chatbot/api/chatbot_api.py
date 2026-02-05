import frappe

from chatbot.utils.utils import sanitize_user_input, conversation

@frappe.whitelist(allow_guest=True)
def receive_user_input(message):
    """
    Entry point for chatbot API.
    - Sanitizes input
    - Handles conversation
    - Returns a structured JSON response
    """
    user = frappe.session.user if frappe.session.user != "Guest" else "Guest"
    clean_input = sanitize_user_input(message)
    reply = conversation(clean_input, user)
    return reply

