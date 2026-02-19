import frappe

logger = frappe.logger("chatbot", allow_site=True)

def log_info(message):
    # Log to file only (safe)
    logger.info(str(message)[:2000])

def log_error(message, title="Chatbot Error"):
    # Only real errors go to Error Log
    frappe.log_error(str(message)[:5000], title)
