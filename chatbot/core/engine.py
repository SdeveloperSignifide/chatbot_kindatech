from chatbot.core.response_router import route
import frappe
from chatbot.utils.logger import log_info


def process_message(message: str):
    log_info(f"User message length: {len(message)}")

    reply = route(message)

    log_info(f"Bot reply length: {len(reply)}")
    log_info(f"Bot reply preview: {reply[:300]}")

    return reply

from PIL import Image, ImageOps
import pytesseract
import io

def extract_text_from_image(content_bytes):
    try:
        img = Image.open(io.BytesIO(content_bytes))
        img = img.convert("RGB")
        img = ImageOps.grayscale(img)
        text = pytesseract.image_to_string(img)
        return text.strip() if text.strip() else None
    except Exception as e:
        frappe.log_error(str(e), "Image OCR Error")
        return None