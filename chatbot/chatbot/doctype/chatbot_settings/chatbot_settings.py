# chatbot/chatbot/doctype/chatbot_settings/chatbot_settings.py

import frappe
from frappe.model.document import Document


class ChatbotSettings(Document):
    def validate(self):
        """
        Ensure only one Chatbot Settings is active.
        If this record is active, deactivate all others.
        """
        if self.is_active:
            # Fetch all other active settings
            active_settings = frappe.get_all(
                "Chatbot Settings",
                filters={"is_active": 1, "name": ["!=", self.name]},
                fields=["name"]
            )

            # Deactivate them
            for s in active_settings:
                frappe.db.set_value(
                    "Chatbot Settings",
                    s.name,
                    "is_active",
                    0,
                    update_modified=True
                )
