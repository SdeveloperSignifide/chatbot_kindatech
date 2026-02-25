import re

def classify_intent(message: str, file_content: str = None):
    """
    Advanced intent classification with:
    - Word boundary protection
    - Pattern matching
    - File-aware logic
    - Priority-based scoring
    """

    if not message:
        return "llm"

    msg = message.lower().strip()

    msg = re.sub(r"\s+", " ", msg)

    if file_content and file_content.strip():
        if any(word in msg for word in [
            "analyze", "review", "summarize", "extract",
            "look at", "check", "read", "interpret"
        ]):
            return "file_analysis"

    if re.search(r"\b(hi|hello|hey|good morning|good afternoon)\b", msg):
        return "greeting"

    if re.search(r"\b(how are you|how are you doing|how are you feeling)\b", msg):
        return "how_are_you"

    if file_content and file_content.strip():
        return "file_analysis"

    return "llm"