import json
import markdown


def parse_ai_response(response):
    """
    Safely parse AI provider response
    and format Markdown properly for frontend rendering.
    """

    if not response:
        return "I'm sorry, I couldn't generate a response."

    content = ""

    if isinstance(response, str):
        try:
            parsed = json.loads(response)
            content = parsed.get("message", response)
        except Exception:
            content = response
    elif isinstance(response, dict):
        content = response.get("message") or response.get("content") or str(response)
    else:
        content = str(response)
    return markdown.markdown(content)
