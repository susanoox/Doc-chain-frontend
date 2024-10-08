from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from mayan.apps.acls.models import AccessControlList
from mayan.apps.documents.models.document_models import Document, Summary
from mayan.apps.documents.views.document_views import DocumentListView

from mayan.apps.views.exceptions import ActionError
from mayan.apps.views.generics import (
    MultipleObjectConfirmActionView, MultipleObjectFormActionView,
    SingleObjectDetailView
)

from .exceptions import DocumentAlreadyCheckedOut, DocumentNotCheckedOut
from .forms import DocumentCheckOutDetailForm, DocumentCheckOutForm
from .icons import (
    icon_check_in_document, icon_check_out_document, icon_check_out_info,
    icon_check_out_list
)
from .models import DocumentCheckout, Document

from .permissions import (
    permission_document_check_in, permission_document_check_in_override,
    permission_document_check_out, permission_document_check_out_detail_view
)
from mayan.apps.documents.tasks.document_tasks import PROCESSING_FILE_QUEUE
import requests


SummaryUrl = "http://13.233.48.180:8080/v2/summary" 
RequestTimeOut = 1200

def UploadSummary(payload):  
    try:
        print("SummaryUrl", SummaryUrl)
        response = requests.post(SummaryUrl, json=payload, timeout=RequestTimeOut)
        print("payload",payload, response)
        
        response_json = response.json()
        return response_json.get('response')
    except Exception as e:
        print("Error upload summary:", e)

class DocumentCheckInView(MultipleObjectConfirmActionView):
    error_message = _(
        'Unable to check in document "%(instance)s"; %(exception)s'
    )
    pk_url_kwarg = 'document_id'
    success_message_plural = _(
        '%(count)d documents checked in successfully.'
    )
    success_message_single = _(
        'Document "%(object)s" checked in successfully.'
    )
    success_message_singular = _(
        '%(count)d document checked in successfully.'
    )
    title_plural = _(message='Check in %(count)d documents.')
    title_single = _(message='Check in document "%(object)s".')
    title_singular = _(message='Check in %(count)d document.')
    view_icon = icon_check_in_document

    def get_extra_context(self):
        context = {}

        if self.object_list.count() == 1:
            context.update(
                {
                    'object': self.object_list.first()
                }
            )

        return context

    def get_post_object_action_url(self):
        if self.action_count == 1:
            return reverse(
                viewname='checkouts:check_out_info', kwargs={
                    'document_id': self.action_id_list[0]
                }
            )
        else:
            super().get_post_action_redirect()

    def get_source_queryset(self):
        # object_permission is None to disable restricting queryset mixin
        # and restrict the queryset ourselves from two permissions.
        queryset_documents = Document.valid.all()

        queryset_check_ins = AccessControlList.objects.restrict_queryset(
            permission=permission_document_check_in,
            queryset=queryset_documents, user=self.request.user
        )

        queryset_check_in_overrides = AccessControlList.objects.restrict_queryset(
            permission=permission_document_check_in_override,
            queryset=queryset_documents, user=self.request.user
        )

        return queryset_check_ins | queryset_check_in_overrides

    def object_action(self, form, instance):
        try:
            DocumentCheckout.business_logic.check_in_document(
                document=instance, user=self.request.user
            )
        except DocumentNotCheckedOut as exception:
            raise ActionError(exception)


class DocumentCheckOutView(MultipleObjectFormActionView):
    error_message = _(
        'Unable to checkout document "%(instance)s"; %(exception)s'
    )
    form_class = DocumentCheckOutForm
    object_permission = permission_document_check_out
    pk_url_kwarg = 'document_id'
    source_queryset = Document.valid.all()
    success_message_plural = _(
        '%(count)d documents checked out successfully.'
    )
    success_message_single = _(
        'Document "%(object)s" checked out successfully.'
    )
    success_message_singular = _(
        '%(count)d document checked out successfully.'
    )
    title_plural = _(message='Checkout %(count)d documents.')
    title_single = _(message='Checkout document "%(object)s".')
    title_singular = _(message='Checkout %(count)d document.')
    view_icon = icon_check_out_document

    def get_extra_context(self):
        context = {}

        if self.object_list.count() == 1:
            context.update(
                {
                    'object': self.object_list.first()
                }
            )

        return context

    def get_post_object_action_url(self):
        if self.action_count == 1:
            return reverse(
                viewname='checkouts:check_out_info', kwargs={
                    'document_id': self.action_id_list[0]
                }
            )
        else:
            super().get_post_action_redirect()

    def object_action(self, form, instance):
        try:
            DocumentCheckout.objects.check_out_document(
                block_new_file=form.cleaned_data['block_new_file'],
                document=instance,
                expiration_datetime=form.cleaned_data['expiration_datetime'],
                user=self.request.user
            )
        except DocumentAlreadyCheckedOut as exception:
            raise ActionError(exception)


class DocumentCheckOutDetailView(SingleObjectDetailView):
    form_class = DocumentCheckOutDetailForm
    object_permission = permission_document_check_out_detail_view
    pk_url_kwarg = 'document_id'
    source_queryset = Document.valid.all()
    view_icon = icon_check_out_info

    def get_extra_context(self):
        return {
            'object': self.object,
            'title': _(
                'Check out details for document: %s'
            ) % self.object
        }


class DocumentCheckOutListView(DocumentListView):
    object_permission = permission_document_check_out_detail_view
    view_icon = icon_check_out_list

    def get_document_queryset(self):
        queryset = DocumentCheckout.objects.checked_out_documents()
        return Document.valid.filter(
            pk__in=queryset.values('pk')
        )

    def get_extra_context(self):
        context = super().get_extra_context()
        context.update(
            {
                'no_results_icon': icon_check_out_info,
                'no_results_text': _(
                    'Checking out a document, blocks certain operations '
                    'for a predetermined amount of time.'
                ),
                'no_results_title': _(message='No documents have been checked out'),
                'title': _(message='Checked out documents')
            }
        )
        return context


# Custom
        
class summery(SingleObjectDetailView):
    template_name = 'summery_view.html'  # Set your custom template path
    form_class = DocumentCheckOutDetailForm
    object_permission = permission_document_check_out_detail_view
    pk_url_kwarg = 'document_id'
    source_queryset = Document.valid.all()
    
    view_icon = icon_check_out_info
    file_format_available = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp','.pptx','.pdf','.txt','.xls', '.xlsx', '.xlsm', '.xlsb','.doc', '.docx')

    def get_extra_context(self):
        document_id = self.kwargs['document_id']
        try:
            obj = Document.objects.get(id=document_id)
            filetry = obj.file_latest.file
            document_file = obj.file_latest
            print("filetry", filetry, document_id)
            try:
                summary_data = Summary.objects.get(doc_id=document_id)
                content = summary_data.summary
                if content is None or content == "" or content.strip() == "":
                    content = "🔄️ Summary is generating please wait !"
                    summeryContent = UploadSummary(summary_data.content).get('summary')
                    print(summeryContent)
                    summary_data.summary = summeryContent
                    summary_data.save()
            except Summary.DoesNotExist:
                try:
                    if (document_id != None) and (int(document_id) in PROCESSING_FILE_QUEUE):
                        content = "Summary is generating please wait !"
                    elif not str(document_file).lower().endswith(self.file_format_available):
                        content = "Summary text is not available for this file format."
                    else:
                        content = "Summary is generating please wait !"
                except:
                    content = "Summary text is not available in this file."
                    print("error..")
        except:
            content = "Summary text is not available in this file."
            print("error..")
        print("content :", content)
        
        return {
            'object': self.object,
            'title': _('Summary Details of: %s') % self.object,
            'content': content, 
            'doc_id':document_id
        }

class Ocr(SingleObjectDetailView):
    template_name = 'summery_view.html'  # Set your custom template path
    form_class = DocumentCheckOutDetailForm
    object_permission = permission_document_check_out_detail_view
    pk_url_kwarg = 'document_id'
    source_queryset = Document.valid.all()
    
    view_icon = icon_check_out_info
    file_format_available = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp','.pptx','.pdf','.txt','.xls', '.xlsx', '.xlsm', '.xlsb','.doc', '.docx')

    def get_extra_context(self):
        document_id = self.kwargs['document_id']
        try:
            obj = Document.objects.get(id=document_id)
            filetry = obj.file_latest.file
            document_file = obj.file_latest
            try:
                ocr_data = Summary.objects.get(doc_id=document_id)
                content = ocr_data.content
            except Summary.DoesNotExist:
                try:
                    if (document_id != None) and (int(document_id) in PROCESSING_FILE_QUEUE):
                        content = "OCR is generating please wait !"
                    elif not str(document_file).lower().endswith(self.file_format_available):
                        content = "Ocr text is not available for this file format."
                    else:
                        content = "OCR is generating please wait !"
                except:
                    content = "OCR not found for this document."
        except:
            content = "OCR not found for this document."
        return {
            'object': self.object,
            'title': _('OCR Details of: %s') % self.object,
            'content': content, 
            'type':'ocr',
            'doc_id':document_id
        }
