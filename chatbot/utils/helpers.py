import random
import re
from chatbot.configurations import GREETING_RESPONSES, HOW_ARE_YOU_RESPONSES

def random_greeting():
    return random.choice(GREETING_RESPONSES)

def random_how_are_you():
    return random.choice(HOW_ARE_YOU_RESPONSES)


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def preprocess_input(text: str) -> str:
    return normalize_text(text)

    
def limit_tokens(text: str, max_chars=8000):
    if not text:
        return ""
    return text[:max_chars]
