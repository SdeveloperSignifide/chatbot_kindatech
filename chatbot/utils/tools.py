import frappe



def looks_like_inventory_question(text: str) -> bool:
    patterns = [
        r"do you have",
        r"is there",
        r"available",
        r"in stock",
        r"have any",
    ]
    return any(p in text for p in patterns)

def extract_product_candidate(text: str) -> str | None:
    stop_words = {"do", "you", "have", "any", "is", "there", "in", "stock"}
    words = text.split()
    candidates = [w for w in words if w not in stop_words]
    return " ".join(candidates) if candidates else None


