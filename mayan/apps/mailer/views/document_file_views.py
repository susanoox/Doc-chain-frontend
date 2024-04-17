from django.utils.translation import gettext_lazy as _

from mayan.apps.documents.models.document_file_models import DocumentFile

from ..icons import (
    icon_document_file_attachment_send_single,
    icon_document_file_link_send_single
)

from .base import MailingObjectAttachmentSendView, MailingObjectLinkSendView


class MailDocumentFileAttachmentView(MailingObjectAttachmentSendView):
    pk_url_kwarg = 'document_file_id'
    source_queryset = DocumentFile.valid.all()
    success_message = _(
        message='%(count)d document file queued for email delivery'
    )
    success_message_plural = _(
        '%(count)d document files queued for email delivery'
    )
    title = 'Email document file'
    title_document = 'Email document file: %s'
    title_plural = 'Email document files'
    view_icon = icon_document_file_attachment_send_single


class MailDocumentFileLinkView(MailingObjectLinkSendView):
    pk_url_kwarg = 'document_file_id'
    source_queryset = DocumentFile.valid.all()
    success_message = _(
        '%(count)d document file link queued for email delivery'
    )
    success_message_plural = _(
        '%(count)d document file links queued for email delivery'
    )
    title = 'Email document file link'
    title_document = 'Email link for document file: %s'
    title_plural = 'Email document file links'
    view_icon = icon_document_file_link_send_single
