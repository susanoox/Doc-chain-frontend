
############################# custom Imports ##########################################
import requests
import json, cv2, io, hashlib
import language_tool_python
from requests.exceptions import ConnectionError, Timeout
from requests.exceptions import JSONDecodeError

########################################################################################
from pdf2image import convert_from_path
from PIL import Image
import pytesseract, hashlib
import PyPDF2, numpy as np
########################################################################################
from ..models.document_models import Document
############################ URL Variables #############################################

try:
    BlockUrl = 'http://3.27.232.173/filehash'
    Ocrurl = 'http://3.107.59.224:8080/v2/ocr'
    url_BOT = 'http://3.107.59.224:8080/v2/upload'
    SummaryUrl = "http://3.107.59.224:8080/v2/summary" 
    RequestTimeOut = 1200
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
            response = requests.post(url_BC, data=json_data, headers={'Content-Type': 'application/json'}, timeout=RequestTimeOut)
            if response.status_code == 200:
                print("File uploaded for BlockChain")
            else:
                print("Upload failed for BlockChain")
    except Exception as e:
        print("Error uploading to blockchain:", e)

def UploadSummary(payload):  
    try:
        print("SummaryUrl", SummaryUrl)
        response = requests.post(SummaryUrl, json=payload, timeout=RequestTimeOut)
        print("payload",payload, response)
        
        response_json = response.json()
        return response_json.get('response')
    except Exception as e:
        print("Error upload summary:", e)
    
        

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
    except JSONDecodeError:
        print("Failed to decode JSON response")
        return None
    
##################################### End of Functions ##################################################


def readFile(Data:Document):
    document_file = Data.file_latest
    print('document_file', document_file)
    ReadContent = ""
    #-------------------------------------------- Extract From Text ---------------------------------------------------------
    if str(document_file).lower().endswith(('.jpg', '.jpeg', '.png')):
        with document_file.file.open('rb') as img_file:
            img = Image.open(img_file)
            try:
                image = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)  # Convert to grayscale4
            except:
                image=np.array(img)
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
                    ReadContent = text
                else:
                    with document_file.file.open('rb') as img_file:
                        content_text = extract_text_from_image_google(img_file.read())
                        print(content_text)
                        if content_text is not None:
                            ReadContent = content_text
            return ReadContent
    #----------------------------------- Extract From Pdf -----------------------------------------------------------------------------
    elif str(document_file).lower().endswith('.pdf'):
        temp_content = ""
        print('document_file', document_file.file)
        with document_file.file.open('rb') as file_handle:
                pdf_reader = PyPDF2.PdfReader(file_handle)
                # Iterate through all pages of the PDF
                for page_number in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_number]
                    # Extract text from the PDF page
                    text = page.extract_text()
                    temp_content = temp_content + text +"\n\n"
                    print(temp_content)
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
                                content_text = extract_text_from_image_google(image_bytes)
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
        else:
            return temp_content
