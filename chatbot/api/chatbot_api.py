import frappe

from chatbot.utils.utils import sanitize_user_input

@frappe.whitelist(allow_guest=True)
def receive_user_input(message):
    user = frappe.session.user if frappe.session.user != "Guest" else "Guest"
    clean_input = sanitize_user_input(message)
    reply = f"Hello {user}, you asked: {clean_input}"
    return reply
