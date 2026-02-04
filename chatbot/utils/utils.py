import frappe
import html
import re

@frappe.whitelist(allow_guest=True)

def receive_user_input(message):

    if not isinstance(message, str):
        frappe.throw("Invalid message ")

    clean_input = html.escape(message.strip())
    if len(clean_input) ==0:
        return {"message": "Please enter text "}
        
    sql_injection_patterns = [
        r"(\b)(SELECT|INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|EXEC|UNION|GRANT|TRUNCATE)(\b)",
        r"(--|;|')",  # comments, semicolons, single quotes
    ]

    for pattern in sql_injection_patterns:
        if re.search(pattern, clean_input, re.IGNORECASE):
            return {"message": "Invalid Input "}
        


    
    
