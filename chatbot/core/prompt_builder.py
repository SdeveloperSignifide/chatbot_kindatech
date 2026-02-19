from chatbot.core.document_classifier import detect_document_type
from chatbot.core.memory import get_memory
from chatbot.utils.helpers import limit_tokens

def build_prompt(user_text, file_text=""):
    user_text = limit_tokens(user_text, 2000)
    file_text = limit_tokens(file_text, 6000)

    doc_type = detect_document_type(file_text)

    memory = get_memory()
    memory_text = ""
    for m in memory:
        memory_text += f"""
Previous User: {m['user']}
Previous Bot: {m['bot']}
"""

    prompt = f"""
        You are an ERPNext AI Assistant.

        Conversation History:
        {memory_text}

        Document Type Detected: {doc_type}

        User Instruction:
        {user_text}

        Extracted Document Content:
        {file_text}

        Instructions:
        - If document type is invoice or receipt, extract structured financial details.
        - If contract, summarize key clauses.
        - Always prioritize user instruction.
        - Be concise but professional.
        """

    return prompt
