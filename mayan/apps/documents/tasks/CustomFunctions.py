
############################# custom Imports ##########################################
import requests
import json, os, cv2, io
import hashlib, base64
import language_tool_python
from requests.exceptions import ConnectionError, Timeout, RequestException
from dotenv import load_dotenv

########################################################################################
from pdf2image import convert_from_path
from pdf2image import convert_from_path, pdfinfo_from_path
from pdf2image.exceptions import PDFPageCountError
from PIL import Image
from django.db import models
import pytesseract
import PyPDF2, numpy as np
########################################################################################
from ..models.document_models import Document
############################ URL Variables #############################################
load_dotenv()

try:
    baseAi = os.getenv('AI_API')
    BlockUrl = os.getenv('BLOCK_CHAIN_API') + '/filehash'
    Ocrurl = os.getenv('AI_API') + '/V2/ocr'
    url_BOT = os.getenv('AI_API') + '/v2/upload'
    SummaryUrl = os.getenv('AI_API') + "/V2/summary"
    RequestTimeOut = int(os.getenv('REQUEST_TIMEOUT'))
except Exception as e:
    print("env file not found ..!", e)
    url = "env_file_not_found"

################################### Upload Functions ###################################


#################################### Custom Functions ##################################

def Bot_Content_Upload(data_for_BOT):
    try:
        print(data_for_BOT, url_BOT)
        response = requests.post(url_BOT, json=data_for_BOT, headers={'Content-Type': 'application/json'}, timeout=RequestTimeOut)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        if response.status_code == 200:
            print("File uploaded for Bot")
        else:
            print("Upload failed for bot")
    except ConnectionError as ce:
        print("Connection Error:", ce)
        # Handle connection errors here, such as retrying the request
    except Timeout as te:
        print("Timeout Error:", te)
        # Handle timeout errors here
    except requests.exceptions.RequestException as e:
        print("Request Exception:", e)
        # Handle other types of request exceptions here
        

            
def upload_to_blockchain(file_content, file_id):
    try:
        hash_value = hashlib.md5(file_content).hexdigest()
        url_BC = BlockUrl
        data_for_BC = {
            "fileHash": hash_value,
            "fileId": str(file_id)
        }
        print(data_for_BC)
        json_data = json.dumps(data_for_BC)
        response = requests.post(url_BC, data=json_data, headers={'Content-Type': 'application/json'}, timeout=RequestTimeOut)
        if response.status_code == 200:
            print("File uploaded for BlockChain")
        else:
            print("Upload failed for BlockChain")
    except Exception as e:
        print("Error uploading to blockchain:", e)

def UploadSummary(payload):  
    print("SummaryUrl", SummaryUrl)
    response = requests.post(SummaryUrl, json=payload, timeout=RequestTimeOut)
    print("payload",payload, response)
    response_json = response.json()
    return response_json.get('response')

#--------------------------------------- Tools -----------------------------------------------
def calculate_grammar_percentage(text):
        # Initialize LanguageTool outside the function
        global language_tool
        if 'language_tool' not in globals():
            language_tool = language_tool_python.LanguageTool('en-US')
        # Split text once to avoid multiple split operations
        words = text.split()
        total_words = len(words)
        # Batch process the text in chunks of 100 words
        batch_size = 100
        error_count = 0
        for i in range(0, total_words, batch_size):
            chunk = ' '.join(words[i:i+batch_size])
            matches = language_tool.check(chunk)
            error_count += len(matches)
        correct_words = total_words - error_count
        try:
            grammar_percentage = (correct_words / total_words) * 100
        except ZeroDivisionError:
            return 0
        print("grammar_percentage:", str(grammar_percentage))
        return grammar_percentage

def extract_text_from_image_google(content):
    file_base64 = base64.b64encode(content).decode('utf-8')
    payload = {'file': file_base64}
    print(Ocrurl)
    response = requests.post(Ocrurl, json=payload, timeout=int(os.getenv('REQUEST_TIMEOUT')))
    json = response.json()
    content_text = json.get("response")
    if content_text:
        return content_text
    else:
        print("No text found in the image.")
        return None

##################################### End of Functions ##################################################


def readFile(Data:Document):
    document_file = Data.file_latest
    #-------------------------------------------- Extract From Text ---------------------------------------------------------
    if str(document_file).lower().endswith(('.jpg', '.jpeg', '.png')):
        with document_file.file.open('rb') as img_file:
            img = Image.open(img_file)
            image = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)  # Convert to grayscale
            _, threshold_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            denoised_image = cv2.fastNlMeansDenoising(threshold_image, None, h=10, templateWindowSize=7, searchWindowSize=21)
            enhanced_image = cv2.convertScaleAbs(denoised_image, alpha=1.5, beta=30)
            config = r'--oem 3 -c tessedit_char_whitelist=௦௧௨௩௪௫௬௭௮௯ௐஂஃஅஆஇஈஉஊஎஏஐஒஓஔகஙசஞடணதநனபமயரலவஷஸஹாிீுூேைொோௌௐௗ்0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz --psm 6'
            if Data.language == ("tam" or "eng"):
                text = pytesseract.image_to_string(enhanced_image, lang=Data.language, config=config)
            else:
                text = pytesseract.image_to_string(enhanced_image, lang=Data.language)
            if text:
                print("language: ", Data.language)
                print(Data.language == "eng" and (80 > calculate_grammar_percentage(text)), (80 < calculate_grammar_percentage(text)))
                if Data.language == "eng" and (80 < calculate_grammar_percentage(text)):
                    # with document_file.file.open('rb') as img_file:
                    #     file_base64 = base64.b64encode(img_file.read()).decode('utf-8')
                    #     payload = {'file': file_base64}
                    #     print(url)
                    #     response = requests.post(url, json=payload, timeout=int(os.getenv('REQUEST_TIMEOUT')))
                    #     json = response.json()
                    #     content_text = json.get("response")
                    #     if content_text is not None:
                    #         ReadContent = content_text
                    #     else:
                            ReadContent = text
                else:
                    with document_file.file.open('rb') as img_file:
                        content_text = extract_text_from_image_google(img_file.read())
                        if content_text is not None:
                            ReadContent = content_text
            return ReadContent
    #----------------------------------- Extract From Pdf -----------------------------------------------------------------------------
    elif str(document_file).lower().endswith('.pdf'):
        temp_content = ""
        with document_file.file.open('rb') as file_handle:
                pdf_reader = PyPDF2.PdfReader(file_handle)
                # Iterate through all pages of the PDF
                for page_number in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_number]
                    # Extract text from the PDF page
                    text = page.extract_text()
                    temp_content = temp_content + text +"\n\n"
        print(temp_content)
        if 50 > calculate_grammar_percentage(temp_content) and len(temp_content.replace(" ", "")) < 40 :
            try:
                images = convert_from_path(document_file.file.path)
                for i, image in enumerate(images):
                        try:
                            text = pytesseract.image_to_string(image)
                            if 80 > calculate_grammar_percentage(text) and len(temp_content.replace(" ", "")) < 40:
                                rgb_image = image.convert("RGB")
                                image_bytes = io.BytesIO()
                                rgb_image.save(image_bytes, format="JPEG")  # You can change the format if needed
                                image_bytes = image_bytes.getvalue()
                                content_text = document_file.extract_text_from_image_google(image_bytes)
                                text_content = text_content + content_text
                            else:
                                text_content = text_content + text
                        except Exception as e:
                            print("error while reading image",e)
                content = text_content
                return content
            except Exception as pdf_processing_error:
                    print(f"Error processing PDF: {pdf_processing_error}")
                    return None