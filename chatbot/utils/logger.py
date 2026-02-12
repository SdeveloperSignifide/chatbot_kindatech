import frappe

def log_info(message):
    frappe.logger("chatbot").info(message)

def log_error(message):
    frappe.logger("chatbot").error(message)



def log_info(message: str):
    print("[INFO]", message)
    frappe.log_error(message, "Chatbot Info")

def log_error(message: str):
    print("[ERROR]", message)
    frappe.log_error(message, "Chatbot Error")
