import logging

from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from mayan.apps.documents.models.document_models import Document, Summary
from mayan.apps.documents.models.document_type_models import DocumentType
from mayan.apps.documents.permissions import permission_document_create
from mayan.apps.views.utils import request_is_ajax
from mayan.apps.views.view_mixins import ExternalObjectViewMixin

from ..forms import NewDocumentForm
from ..icons import icon_document_upload_wizard

from .base import UploadBaseView

logger = logging.getLogger(name=__name__)


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

############################ URL Variables #############################################
load_dotenv()

try:
    baseAi = os.getenv('AI_API')
    BlockUrl = os.getenv('BLOCK_CHAIN_API') + '/filehash'
    Ocrurl = os.getenv('AI_API') + '/v1/ocr'
    SummaryUrl = os.getenv('AI_API') + "/v1/summary"
    RequestTimeOut = int(os.getenv('REQUEST_TIMEOUT'))
except Exception as e:
    print("env file not found ..!", e)
    url = "env_file_not_found"

################################### Upload Functions ###################################

def Bot_Content_Upload(url_BOT, data_for_BOT):
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

def read_and_print_document_content():
    document = Document.objects.last()
    print(document, document.id, document.file_latest, document.file_latest.file)
    
    content = False
    # Check if the document has a latest file associated with it
    if document.file_latest.file:
        # Get the file name and extension
        file_name, file_extension = os.path.splitext(document.file_latest.filename)
        # Check if the file is an image
        if file_extension.lower() in ('.jpg', '.jpeg', '.png'):
            # Open the image file
            print("Start reading... in image")
            with document.file_latest.file.open('rb') as img_file:
                img = Image.open(img_file)
                # int("img", img)
                # if len(np.array(img)) > 1:
                image = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)  # Convert to grayscale
                _, threshold_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                denoised_image = cv2.fastNlMeansDenoising(threshold_image, None, h=10, templateWindowSize=7,
                                                        searchWindowSize=21)
                enhanced_image = cv2.convertScaleAbs(denoised_image, alpha=1.5, beta=30)
                config = r'--oem 3 -c tessedit_char_whitelist=௦௧௨௩௪௫௬௭௮௯ௐஂஃஅஆஇஈஉஊஎஏஐஒஓஔகஙசஞடணதநனபமயரலவஷஸஹாிீுூேைொோௌௐௗ்0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz --psm 6'
                if document.language == ("tam" or "eng"):
                    text = pytesseract.image_to_string(enhanced_image, lang=document.language, config=config)
                else:
                    text = pytesseract.image_to_string(enhanced_image, lang=document.language)
                print("text : ", text)
                if text:
                    print("text present..!")
                    if document.language == "eng":
                        if 80 > document.calculate_grammar_percentage(text):
                            print("image extract from API...!")
                            with document.file.open('rb') as img_file:
                                file_base64 = base64.b64encode(img_file.read()).decode('utf-8')
                                payload = {'file': file_base64}
                                response = requests.post(url, json=payload, timeout=int(os.getenv('REQUEST_TIMEOUT')))
                                json = response.json()
                                content_text = json.get("response")
                                if content_text is not None:
                                    content = content_text
                                    print(content)
                        else:
                            content = text
                            
                    else:
                        with document.file.open('rb') as img_file:
                                content_text = document.extract_text_from_image_google(img_file.read())
                                if content_text is not None:
                                    content = content_text
                print("inner content", content)
        elif str(document).lower().endswith('.pdf'):
            print("Working in the pdf..!")
            # Open the PDF file using PyPDF2
            temp_content = ""
            with document.file.open('rb') as file_handle:
                print("pdf reading..!")
                pdf_reader = PyPDF2.PdfReader(file_handle)
                # Iterate through all pages of the PDF
                for page_number in range(len(pdf_reader.pages)):
                    print("in for loop")
                    page = pdf_reader.pages[page_number]
                    # Extract text from the PDF page
                    text = page.extract_text()
                    temp_content = temp_content + text +"\n\n"
            print(temp_content)
            if 50 > document.calculate_grammar_percentage(temp_content) and len(temp_content.replace(" ", "")) < 40 :
                print(document.file.path, "working pdf to image")
                try:
                    try:
                        pdfinfo_from_path(document.file.path)
                    except PDFPageCountError:
                        # Handle the case when the PDF file is not valid
                        print(f"Invalid PDF file: {document.file.path}")
                        return None
                    # Convert the PDF content to images
                    images = convert_from_path(document.file.path)
                    text_content = ""
                    print(images)
                    for i, image in enumerate(images):
                        # Perform OCR to extract text from the image 
                        try:
                            text = pytesseract.image_to_string(image)
                            if 80 > document.calculate_grammar_percentage(text) and len(temp_content.replace(" ", "")) < 40:
                                print("google image are working...")
                                rgb_image = image.convert("RGB")
                                image_bytes = io.BytesIO()
                                rgb_image.save(image_bytes, format="JPEG")  # You can change the format if needed
                                image_bytes = image_bytes.getvalue()
                                content_text = document.extract_text_from_image_google(image_bytes)
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
                content = temp_content
        elif str(document).lower().endswith('.txt'):
            text = ""
            # Open the file and read its content for non-image files
            with document.file.open('r') as file_handle:
                text = file_handle.read()
            # except Exception as e:
            #     print(f"Error reading document content: {e}")
        return content
    else:
        return "Document Not Found..!"
            
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

def UploadSummary(text):
    try:
        length_obj = 20 # Can Modify from DB
        # length_obj=obj.last_length
    except:
        length_obj = 20
    payload = {
        'file_content': text,
        'language': self.language,
        'num_lines': length_obj
    }
    response = requests.post(SummaryUrl, json=payload, timeout=RequestTimeOut)
    print("payload",payload, response)
    response_json = response.json()
    return response_json.get('response')

################################ Tools ###################################################
def calculate_grammar_percentage(text):
        print("In check grammar")
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
    response = requests.post(url, json=payload, timeout=int(os.getenv('REQUEST_TIMEOUT')))
    json = response.json()
    content_text = json.get("response")
    if content_text:
        return content_text
    else:
        print("No text found in the image.")
        return None


##########################################################################################
class DocumentUploadView(ExternalObjectViewMixin, UploadBaseView):
    document_form = NewDocumentForm
    external_object_class = DocumentType
    external_object_permission = permission_document_create
    object_permission = permission_document_create
    source_link_view_name = 'sources:document_upload'
    view_icon = icon_document_upload_wizard
    view_source_action = 'document_upload'

    def forms_valid(self, forms):
        action = self.source.get_action(name='document_upload')

        interface_load_kwargs = {
            'document_type': self.external_object, 'forms': forms,
            'request': self.request, 'view': self
        }

        try:
            Document.execute_pre_create_hooks(
                kwargs={
                    'document_type': self.external_object,
                    'file_object': None,
                    'user': self.request.user
                }
            )
            a=action.execute(
                interface_name='View',
                interface_load_kwargs=interface_load_kwargs
            )
            print("Document Uploaded..!", a)
            doc_data = Document.objects.last()
            if doc_data:
                print("File Upload Started..!", doc_data.id)
                
                # Access the file associated with the document
                uploaded_file = doc_data.file_field_name  # Replace 'file_field_name' with the name of your file field
                # Do something with the uploaded file, such as accessing its path or content
                file_path = uploaded_file.path
                file_content = uploaded_file.read()

                # Now you can process or use the file content as needed
                print("File Path:", file_path)
                print("File Content:", file_content)

                # Proceed with blockchain upload if content is valid
                if file_content:
                    upload_to_blockchain(file_content, doc_data.id)

            

        except Exception as exception:
            message = _(
                'Error processing source document upload; '
                '%(exception)s'
            ) % {
                'exception': exception,
            }
            logger.critical(msg=message, exc_info=True)
            if request_is_ajax(request=self.request):
                return JsonResponse(
                    data={
                        'error': str(message)
                    }, status=500
                )
            else:
                messages.error(
                    message=message.replace('\n', ' '),
                    request=self.request
                )
                raise type(exception)(message) from exception
            
        else:
            messages.success(
                message=_(
                    'New document queued for upload and will be '
                    'available shortly.'
                ), request=self.request
            )

            return HttpResponseRedirect(
                redirect_to='{}?{}'.format(
                    reverse(
                        viewname=self.request.resolver_match.view_name,
                        kwargs=self.request.resolver_match.kwargs
                    ), self.request.META['QUERY_STRING']
                ),
            )



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'document_type': self.external_object,
                'title': _(
                    'Upload a document of type "%(document_type)s" from '
                    'source: %(source)s'
                ) % {
                    'document_type': self.external_object,
                    'source': self.source.label
                }
            }
        )

        return context

    def get_form_extra_kwargs__document_form(self):
        return {
            'document_type': self.external_object
        }

    def get_form_extra_kwargs__source_form(self):
        return {
            'source': self.source
        }

    def get_pk_url_kwargs(self):
        return {
            'pk': self.request.GET.get(
                'document_type_id', self.request.POST.get('document_type_id')
            )
        }
