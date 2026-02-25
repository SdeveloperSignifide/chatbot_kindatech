import frappe
import os
import io
from chatbot.core.engine import process_message

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
    import os
    import io

    ext = os.path.splitext(filename)[1].lower()

    try:
        if ext in [".txt", ".csv"]:
            return content_bytes.decode("utf-8", errors="ignore")

        if ext == ".pdf":
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(content_bytes))
            return "\n".join(page.extract_text() or "" for page in reader.pages)

        if ext == ".docx":
            import docx2txt
            return docx2txt.process(io.BytesIO(content_bytes))

        if ext in [".png", ".jpg", ".jpeg"]:
            from PIL import Image
            import pytesseract
            img = Image.open(io.BytesIO(content_bytes))
            return pytesseract.image_to_string(img)

        return None

    except Exception:
        return None

@frappe.whitelist(allow_guest=True)
def upload_file_with_text():

    uploaded_files = frappe.request.files.getlist("files")
    text = frappe.form_dict.get("text", "").strip()

    if not uploaded_files and not text:
        return {"message": "No file or text provided."}

    parsed_texts = []

    for uploaded_file in uploaded_files:
        content_bytes = uploaded_file.read()
        parsed = parse_file_content(
            uploaded_file.filename,
            content_bytes
        )
        if parsed:
            parsed_texts.append(parsed[:4000])

    combined_file_text = "\n\n".join(parsed_texts)
    print("The kinuthia combined text is ", text)
    if combined_file_text:
        combined_text = f"""
            User Instruction:
            {text}

            Extracted File Content:
            {combined_file_text}

            Please analyze the file content and respond according to the user's instruction.
            """
    else:
        combined_text = text  
    reply = process_message(combined_text)
    print("The combined text is ", combined_text)
    print("The reply is ", reply)

    return reply