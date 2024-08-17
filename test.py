import pdfplumber
from pdf2image import convert_from_path
import pytesseract
import io
import requests

Ocrurl = 'http://13.233.48.180:8080/v2/ocr'


def extract_text_from_image_google(content):
    files = {'file': content}
    
    # Make a POST request to the OCR endpoint
    response = requests.post(Ocrurl, files=files)
    
    print(response)  # Print response status code for debugging
    
    try:
        # Attempt to parse the JSON response
        json_response = response.json()
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Extract the text from the response JSON
            text = json_response.get("response").get("ocr_text")
            return text
        else:
            print("Error:", response.status_code)
            return None
    except requests.exceptions.JSONDecodeError:
        print("Failed to decode JSON response")
        return None

def process_pdf(file_path):
    if str(file_path).lower().endswith('.pdf'):
        print("Working with document...")

        content = ""

        try:
            # Extract text content from PDF
            with pdfplumber.open(file_path) as pdf:
                temp_content = ""
                for page in pdf.pages:
                    extracted_text = page.extract_text(layout=True)
                    if extracted_text:
                        temp_content += '\n' + extracted_text.strip()

            # Check if the PDF might contain images (if extracted text is too short or empty)
            if not temp_content.strip() or len(temp_content.replace(" ", "")) < 40:
                print("PDF contains images or very little text, processing images...")
                images = convert_from_path(file_path)
                text_content = ""

                for i, image in enumerate(images):
                    print("Processing image", i)
                    try:
                        text = pytesseract.image_to_string(image)
                        if len(text.replace(" ", "")) < 40:
                            rgb_image = image.convert("RGB")
                            image_bytes = io.BytesIO()
                            rgb_image.save(image_bytes, format="JPEG")
                            image_bytes = image_bytes.getvalue()
                            # Assuming you have a function `extract_text_from_image_google` to extract text
                            text_content += extract_text_from_image_google(image_bytes)
                        else:
                            text_content += text
                    except Exception as e:
                        print(f"Error while reading image {i}: {e}")

                content = text_content
            else:
                content = temp_content

            return content

        except Exception as pdf_processing_error:
            print(f"Error processing PDF: {pdf_processing_error}")
            return None

# Reading a PDF file using open() function and passing its path to the process_pdf function
file_path = "/mnt/g/UthayaAnna/Doc-chain-frontend/carbon (16).pdf"
with open(file_path, 'rb') as document_file:
    result = process_pdf(file_path)
    if result:
        print(result)
    else:
        print("Failed to process the PDF content")
