import frappe


@frappe.whitelist(allow_guest=True)
def receive_user_input(message):
    user= frappe.session.user
    current_path= frappe.form_dict.get("route")
    # TODO: Replace with OpenAI / local LLM
    reply = f"Hello {user}, you asked: for something like this  {message}"
    return reply
