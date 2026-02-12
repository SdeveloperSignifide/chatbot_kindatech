from chatbot.core.intent_classifier import classify_intent
from chatbot.services.ai_service import AIService
from chatbot.utils.helpers import random_greeting, random_how_are_you
from chatbot.utils.response_parser import parse_ai_response


def route(message: str):

    intent = classify_intent(message)

    if intent == "greeting":
        return random_greeting()

    if intent == "how_are_you":
        return random_how_are_you()
    ai_response = AIService.generate(message)
    return parse_ai_response(ai_response)
