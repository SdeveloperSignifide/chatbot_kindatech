def classify_intent(message: str):

    msg = message.lower().strip()

    greetings = ["hi", "hello", "hey"]
    how_are_you = ["how are you", "how are you doing", "how are you feeling"]

    if any(g in msg for g in greetings):
        return "greeting"

    if any(q in msg for q in how_are_you):
        return "how_are_you"

    return "llm"
