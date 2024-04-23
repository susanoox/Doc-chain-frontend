import logging
from pathlib import Path

from django.apps import apps
from django.contrib.auth import get_user_model
from django.db import OperationalError

from ..models.document_models import Document, Summary

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
    obj = Document.objects.get(id=document.id)
    Content = readFile(obj)
    print(Content)
    print("Content printed...!")
    #----------------------------------------------------Summery-----------------------------------------------
    payload = {
        'file_content': Content,
        'language': obj.language,
        'num_lines': 30
    }
    summeryContent = UploadSummary(payload).get('summary')
    print(summeryContent)
    new_summary = Summary(
        doc_id=obj.id,
        name=obj.label,
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
    upload_to_blockchain(obj.file_latest.file.open('rb').read(),obj.id)
    print("BlockChain Uploaded Complete..!")
    #----------------------------------------------------------------------------------------------------------
    ###########################################   End Upload    ###############################################

