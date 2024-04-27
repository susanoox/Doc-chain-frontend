import logging, time
from pathlib import Path

from django.apps import apps
from django.contrib.auth import get_user_model
from django.db import OperationalError

from ..models.document_models import Document, Summary, DocErrorHandling

from mayan.celery import app

from .document_file_tasks import task_document_file_create
from .utils import execute_callback

############################################## Custom Function Import ############################################
from .CustomFunctions import readFile, UploadSummary, upload_to_blockchain, Bot_Content_Upload
####################################################### End ######################################################

logger = logging.getLogger(name=__name__)

# obj = Summary.objects.all()
# for i in obj:
#     print(i.id, i.summary, i.doc_id)

@app.task(bind=True, ignore_results=True, retry_backoff=True)
def task_document_upload(
    self, document_type_id, shared_uploaded_file_id,
    callback_dict=None, description=None, label=None, language=None,
    user_id=None
):
    callback_dict = callback_dict or {}

    DocumentType = apps.get_model(
        app_label='documents', model_name='DocumentType'
    )
    SharedUploadedFile = apps.get_model(
        app_label='storage', model_name='SharedUploadedFile'
    )
    User = get_user_model()

    try:
        document_type = DocumentType.objects.get(pk=document_type_id)
        shared_uploaded_file = SharedUploadedFile.objects.get(
            pk=shared_uploaded_file_id
        )
        if user_id:
            user = User.objects.get(pk=user_id)
        else:
            user = None
    except OperationalError as exception:
        raise self.retry(exc=exception)

    description = description or ''

    label = label or Path(
        str(shared_uploaded_file)
    ).name

    try:
        document = document_type.documents_create(
            description=description, label=label, language=language,
            user=user
        )
        print("document Datas : ",document.id)
    except OperationalError as exception:
        logger.error(
            'Operational error creating new document of type: %s, '
            'label: %s; %s. Retrying.', document_type, label, exception
        )
        raise self.retry(exc=exception)
    except Exception as exception:
        logger.critical(
            'Unexpected exception while creating new document of type: %s, '
            'label: %s; %s', document_type, label, exception
        )
        raise
    else:
        execute_callback(
            callback_dict=callback_dict, document=document,
            name='post_document_create'
        )

        task_document_file_create.apply_async(
            kwargs={
                'callback_dict': callback_dict,
                'document_id': document.pk,
                'filename': label,
                'is_document_upload_sequence': True,
                'shared_uploaded_file_id': shared_uploaded_file_id,
                'user_id': user_id
            }
        )
    ############################################ Custom Uploding ##############################################
    print("Sample print..")
    print('document.id', document.id)
    time.sleep(8)
    obj = Document.objects.get(id=document.pk)

    field_names = [field.name for field in obj._meta.fields]
    # Print field names and values
    for field_name in field_names:
        field_value = getattr(obj, field_name)
        print(f"{field_name}: {field_value}")
        
    #---------------------------------------------- Create Checkpoint ------------------------------------------
    doc_checkpoint = DocErrorHandling.objects.create(doc_id = document.pk)
    
    print("-"*50+"\ncheck point created..!\n"+"-"*50)
    
    Content = readFile(obj)
    print(Content)
    print("Content printed...!")
    #---------------------------------------------------- Summery -----------------------------------------------
    
    payload = {
        'file_content': Content,
        'language': obj.language,
        'num_lines': 30
    }
    print('payload', payload)
    summeryContent = UploadSummary(payload).get('summary')
    print(summeryContent)
    summary_id = document.pk
    summary_label = getattr(obj, "label")
    new_summary = Summary(
        id = document.pk,
        doc_id=summary_id,
        name=summary_label,
        content=Content,
        summary=summeryContent
    )
    new_summary.save() 
    print("Summary Upload complete..!")
    #--------------------------------------------------BotUpload-----------------------------------------------
    data_for_BOT = {
        "file_content": Content,
        "meta_data": {
            "id": str(obj.id),
            "language": str(obj.language),
            "file_latest": str(obj.file_latest),
            "datetime_created": str(obj.datetime_created),
            "description": obj.description,
            "label": obj.label,
            "document_type": str(obj.document_type)
        },
        "namespace": "",
        "doc_id": str(obj.id)
    }
    Bot_Content_Upload(data_for_BOT)
    print("Bot Upload Complete...!")
    #---------------------------------------------------Blockchain---------------------------------------------
    file_content = obj.file_latest.file.open('rb').read()
    upload_to_blockchain(file_content, document.pk)
    print("BlockChain Uploaded Complete..!")
    #----------------------------------------------------------------------------------------------------------
    ###########################################   End Upload    ###############################################

