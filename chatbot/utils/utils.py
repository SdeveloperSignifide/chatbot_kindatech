import frappe
import html
import re

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

