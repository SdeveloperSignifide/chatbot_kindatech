import frappe
import frappe
import io
from PIL import Image
from pypdf import PdfReader
import docx2txt
from chatbot.core.engine import process_message

MAX_FILE_BYTES = 10 * 1024 * 1024  # 10 MB
MAX_CHUNK = 4000  # characters per file chunk
import io
from chatbot.core.engine import process_message,extract_text_from_image

@frappe.whitelist(allow_guest=True)
def receive_user_input(message: str):
    """
    Receive plain text message from user and return chatbot response.
    """
    if not message:
        return {"message": "Please enter a message."}
    
    reply = process_message(message)
    return reply



@frappe.whitelist(allow_guest=True)
def upload_file():
    """
    Handle file upload in memory, parse content, and return chatbot response.
    Supports: txt, csv, pdf, docx, png, jpg, jpeg.
    """
    uploaded_file = frappe.request.files.get("files")
    if not uploaded_file:
        return "No file uploaded."

    try:
        filename = uploaded_file.filename
        content_bytes = uploaded_file.read()
        parsed_text = parse_file_content(filename, content_bytes)

        if not parsed_text:
            return "I couldn't read the file or it contains no text."

        reply = process_message(parsed_text)
        return reply

    except Exception as e:
        frappe.log_error(message=str(e), title="Chatbot File Upload Error")
        return "Something went wrong while processing the file."



def parse_file_content(filename, content_bytes):
    """
    Parse text from uploaded files in memory.
    Supports txt, csv, pdf, docx, png, jpg, jpeg.
    """
    ext = filename.lower().split('.')[-1]

    try:
        if ext in ["txt", "csv"]:
            return content_bytes.decode("utf-8", errors="ignore")

        if ext == "pdf":
            reader = PdfReader(io.BytesIO(content_bytes))
            return "\n".join(page.extract_text() or "" for page in reader.pages)

        if ext == "docx":
            return docx2txt.process(io.BytesIO(content_bytes))

        if ext in ["png", "jpg", "jpeg"]:
            parsed_text = extract_text_from_image(content_bytes)
            return parsed_text

        return None
    except Exception as e:
        frappe.log_error(str(e), f"File Parsing Error: {filename}")
        return None




@frappe.whitelist(allow_guest=True)
def upload_file_with_text():
    """
    Handles file uploads + user instructions.
    Returns chatbot response.
    """
    uploaded_files = frappe.request.files.getlist("files")
    user_text = frappe.form_dict.get("text", "").strip()

    if not uploaded_files and not user_text:
        return {"message": "No file or text provided."}

    parsed_texts = []
    for uploaded_file in uploaded_files:
        if uploaded_file.content_length > MAX_FILE_BYTES:
            return {"message": f"File {uploaded_file.filename} is too large."}

        content_bytes = uploaded_file.read()
        parsed = parse_file_content(uploaded_file.filename, content_bytes)
        if parsed:
            parsed_texts.append(parsed[:MAX_CHUNK])

    combined_file_text = "\n\n".join(parsed_texts)

    if combined_file_text:
        combined_text = f"""
        User Instruction:
        {user_text}

        Extracted File Content:
        {combined_file_text}

        Please analyze the file content and respond according to the user's instruction.
        """
    else:
        combined_text = user_text or "No text or readable content found."
    reply = process_message(combined_text)
    return reply