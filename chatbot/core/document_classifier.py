import re

def detect_document_type(text: str) -> str:
    if not text:
        return "unknown"

    text_lower = text.lower()

    patterns = {
        "invoice": [
            r"invoice\s*no",
            r"invoice\s*number",
            r"tax\s*invoice",
            r"vat",
            r"total\s*amount",
        ],
        "receipt": [
            r"receipt\s*no",
            r"thank\s*you\s*for\s*your\s*purchase",
            r"cashier",
            r"amount\s*paid",
        ],
        "contract": [
            r"agreement",
            r"this\s*contract",
            r"terms\s*and\s*conditions",
            r"party\s*a",
            r"party\s*b",
        ],
        "quotation": [
            r"quotation",
            r"quote\s*no",
            r"valid\s*until",
        ]
    }

    for doc_type, regex_list in patterns.items():
        for pattern in regex_list:
            if re.search(pattern, text_lower):
                return doc_type

    return "unknown"
