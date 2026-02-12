from chatbot.core.response_router import route
from chatbot.utils.logger import log_info


def process_message(message: str):
    log_info(f"User message: {message}")
    reply = route(message)
    log_info(f"Bot reply: {reply}")
    return reply


