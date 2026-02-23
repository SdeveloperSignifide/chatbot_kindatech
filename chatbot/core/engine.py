from chatbot.core.response_router import route
from chatbot.utils.logger import log_info


def process_message(message: str):
    log_info(f"User message length: {len(message)}")

    reply = route(message)

    log_info(f"Bot reply length: {len(reply)}")
    log_info(f"Bot reply preview: {reply[:300]}")

    return reply
