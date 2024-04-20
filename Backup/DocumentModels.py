import uuid

from django.db import models, transaction
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from mayan.apps.common.signals import signal_mayan_pre_save
from mayan.apps.databases.model_mixins import ExtraDataModelMixin
from mayan.apps.events.decorators import method_event
from mayan.apps.events.event_managers import EventManagerSave

from ..events import (
    event_document_created, event_document_edited, event_document_trashed,
    event_trashed_document_deleted
)
from ..literals import DEFAULT_LANGUAGE
from ..managers import (
    DocumentManager, TrashCanManager, ValidDocumentManager,
    ValidRecentlyCreatedDocumentManager
)
from ..settings import setting_language

from .document_model_mixins import DocumentBusinessLogicMixin
from .document_type_models import DocumentType
from .model_mixins import HooksModelMixin

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

__all__ = ('Document', 'DocumentSearchResult',)

#################################### Custom Functions ####################################################

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
#--------------------------------------- Tools -----------------------------------------------
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

##################################### End of Functions ##################################################


class Summary(models.Model): # table name
    id = models.IntegerField(primary_key=True) # id of the table
    doc_id = models.IntegerField()
    name = models.CharField(max_length=255)
    content = models.TextField()
    summary = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.summary


class Document(
    DocumentBusinessLogicMixin, ExtraDataModelMixin, HooksModelMixin,
    models.Model
):
    """
    Defines a single document with it's fields and properties
    Fields:
    * uuid - UUID of a document, universally Unique ID. An unique identifier
    generated for each document. No two documents can ever have the same UUID.
    This ID is generated automatically.
    """
    _hooks_pre_create = []

    file_latest = models.OneToOneField(
        blank=True, null=True, on_delete=models.SET_NULL, to='DocumentFile',
        related_name='document_latest', verbose_name=_(
            'Latest document file'
        )
    )
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, help_text=_(
            'UUID of a document, universally Unique ID. An unique '
            'identifier generated for each document.'
        ), verbose_name=_(message='UUID')
    )
    document_type = models.ForeignKey(
        help_text=_(message='The document type of the document.'),
        on_delete=models.CASCADE, related_name='documents', to=DocumentType,
        verbose_name=_(message='Document type')
    )
    label = models.CharField(
        blank=True, db_index=True, default='', max_length=255,
        help_text=_(
            'A short text identifying the document. By default, will be '
            'set to the filename of the first file uploaded to the document.'
        ),
        verbose_name=_(message='Label')
    )
    description = models.TextField(
        blank=True, default='', help_text=_(
            'An optional short text describing a document.'
        ), verbose_name=_(message='Description')
    )
    datetime_created = models.DateTimeField(
        auto_now_add=True, db_index=True, help_text=_(
            'The date and time of the document creation.'
        ), verbose_name=_(message='Created')
    )
    language = models.CharField(
        blank=True, default=DEFAULT_LANGUAGE, help_text=_(
            'The primary language in the document.'
        ), max_length=8, verbose_name=_(message='Language')
    )
    in_trash = models.BooleanField(
        db_index=True, default=False, help_text=_(
            'Whether or not this document is in the trash.'
        ), editable=False, verbose_name=_(message='In trash?')
    )
    trashed_date_time = models.DateTimeField(
        blank=True, editable=True, help_text=_(
            'The server date and time when the document was moved to the '
            'trash.'
        ), null=True, verbose_name=_(message='Date and time trashed')
    )
    is_stub = models.BooleanField(
        db_index=True, default=True, editable=False, help_text=_(
            'A document stub is a document with an entry on the database '
            'but no file uploaded. This could be an interrupted upload or '
            'a deferred upload via the API.'
        ), verbose_name=_(message='Is stub?')
    )
    version_active = models.OneToOneField(
        blank=True, null=True, on_delete=models.SET_NULL,
        to='DocumentVersion', related_name='document_active', verbose_name=_(
            'Active document version'
        )
    )

    objects = DocumentManager()
    trash = TrashCanManager()
    valid = ValidDocumentManager()

    class Meta:
        ordering = ('label',)
        verbose_name = _(message='Document')
        verbose_name_plural = _(message='Documents')

    def __str__(self):
        return self.get_label()

    def delete(self, *args, **kwargs):
        to_trash = kwargs.pop('to_trash', True)
        user = self.__dict__.pop('_event_actor', None)

        if not self.in_trash and to_trash:
            self.in_trash = True
            self.trashed_date_time = now()
            with transaction.atomic():
                self._event_ignore = True
                self.save(
                    update_fields=('in_trash', 'trashed_date_time')
                )

            event_document_trashed.commit(actor=user, target=self)
        else:
            with transaction.atomic():
                for document_file in self.files.all():
                    document_file.delete()

                super().delete(*args, **kwargs)

            event_trashed_document_deleted.commit(
                actor=user, target=self.document_type
            )

    def get_absolute_url(self):
        return reverse(
            viewname='documents:document_preview', kwargs={
                'document_id': self.pk
            }
        )

    def natural_key(self):
        return (self.uuid,)
    natural_key.dependencies = ['documents.DocumentType']

    @method_event(
        event_manager_class=EventManagerSave,
        created={
            'event': event_document_created,
            'action_object': 'document_type',
            'target': 'self'
        },
        edited={
            'event': event_document_edited,
            'target': 'self'
        }
    )
    def save(self, *args, **kwargs):
        user = self.__dict__.pop('_event_actor', None)
        new_document = not self.pk
        ReadContent = False

        self.description = self.description or ''
        self.label = self.label or ''
        self.language = self.language or setting_language.value

        signal_mayan_pre_save.send(
            instance=self, sender=Document, user=user
        )
        ################################ Custom Code ############################################
        try:
            document_file = self.file_latest
            #-------------------------------------------- Extract From Text ---------------------------------------------------------
            if str(document_file).lower().endswith(('.jpg', '.jpeg', '.png')):
                with document_file.file.open('rb') as img_file:
                    img = Image.open(img_file)
                    image = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)  # Convert to grayscale
                    _, threshold_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                    denoised_image = cv2.fastNlMeansDenoising(threshold_image, None, h=10, templateWindowSize=7, searchWindowSize=21)
                    enhanced_image = cv2.convertScaleAbs(denoised_image, alpha=1.5, beta=30)
                    config = r'--oem 3 -c tessedit_char_whitelist=௦௧௨௩௪௫௬௭௮௯ௐஂஃஅஆஇஈஉஊஎஏஐஒஓஔகஙசஞடணதநனபமயரலவஷஸஹாிீுூேைொோௌௐௗ்0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz --psm 6'
                    if self.language == ("tam" or "eng"):
                        text = pytesseract.image_to_string(enhanced_image, lang=self.language, config=config)
                    else:
                        text = pytesseract.image_to_string(enhanced_image, lang=self.language)
                    if text:
                        if self.language == "eng" and (80 > self.calculate_grammar_percentage(text)):
                            with document_file.file.open('rb') as img_file:
                                file_base64 = base64.b64encode(img_file.read()).decode('utf-8')
                                payload = {'file': file_base64}
                                response = requests.post(url, json=payload, timeout=int(os.getenv('REQUEST_TIMEOUT')))
                                json = response.json()
                                content_text = json.get("response")
                                if content_text is not None:
                                    ReadContent = content_text
                                else:
                                    ReadContent = text
                        else:
                            with document_file.file.open('rb') as img_file:
                                content_text = self.extract_text_from_image_google(img_file.read())
                                if content_text is not None:
                                    ReadContent = content_text
            #----------------------------------- Extract From Pdf -----------------------------------------------------------------------------
            elif str(document_file).lower().endswith('.pdf'):
                with document_file.file.open('rb') as file_handle:
                        pdf_reader = PyPDF2.PdfReader(file_handle)
                        # Iterate through all pages of the PDF
                        for page_number in range(len(pdf_reader.pages)):
                            page = pdf_reader.pages[page_number]
                            # Extract text from the PDF page
                            text = page.extract_text()
                            temp_content = temp_content + text +"\n\n"
                if 50 > self.calculate_grammar_percentage(temp_content) and len(temp_content.replace(" ", "")) < 40 :
                    try:
                        images = convert_from_path(document_file.file.path)
                        for i, image in enumerate(images):
                                try:
                                    text = pytesseract.image_to_string(image)
                                    if 80 > self.calculate_grammar_percentage(text) and len(temp_content.replace(" ", "")) < 40:
                                        rgb_image = image.convert("RGB")
                                        image_bytes = io.BytesIO()
                                        rgb_image.save(image_bytes, format="JPEG")  # You can change the format if needed
                                        image_bytes = image_bytes.getvalue()
                                        content_text = self.extract_text_from_image_google(image_bytes)
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
        except Exception as e:
            ReadContent = False
            print(ReadContent)
        
        
        if ReadContent:
            print("ReadContent", self.label, self.language, self.uuid, self.id, self.description)
        #########################################################################################
        super().save(*args, **kwargs)

        if new_document:
            print("Document saved:", self)
        if new_document:
            if user:
                self.add_as_recent_document_for_user(user=user)


class DocumentSearchResult(Document):
    class Meta:
        proxy = True


class RecentlyCreatedDocument(Document):
    objects = models.Manager()
    valid = ValidRecentlyCreatedDocumentManager()

    class Meta:
        proxy = True
