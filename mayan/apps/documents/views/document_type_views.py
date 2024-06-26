import logging

from django.template import RequestContext
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _

from mayan.apps.views.generics import (
    SingleObjectCreateView, SingleObjectDeleteView, SingleObjectEditView,
    SingleObjectListView
)
from mayan.apps.views.view_mixins import ExternalObjectViewMixin

from ..forms.document_type_forms import (
    DocumentTypeFilenameForm_create, DocumentTypeFilenameGeneratorForm
)
from ..icons import (
    icon_document_type_create, icon_document_type_delete,
    icon_document_type_document_list, icon_document_type_edit,
    icon_document_type_filename, icon_document_type_filename_create,
    icon_document_type_filename_delete, icon_document_type_filename_edit,
    icon_document_type_filename_generator, icon_document_type_filename_list,
    icon_document_type_list, icon_document_type_setup
)
from ..links.document_type_links import (
    link_document_type_create, link_document_type_filename_create
)
from ..models.document_type_models import DocumentType, DocumentTypeFilename
from ..permissions import (
    permission_document_type_create, permission_document_type_delete,
    permission_document_type_edit, permission_document_type_view
)

from .document_views import DocumentListView

logger = logging.getLogger(name=__name__)


class DocumentTypeDocumentListView(
    ExternalObjectViewMixin, DocumentListView
):
    external_object_class = DocumentType
    external_object_permission = permission_document_type_view
    external_object_pk_url_kwarg = 'document_type_id'
    view_icon = icon_document_type_document_list

    def get_document_queryset(self):
        return self.external_object.documents.all()

    def get_extra_context(self):
        context = super().get_extra_context()
        context.update(
            {
                'object': self.external_object,
                'title': _(message='Documents of type: %s') % self.external_object
            }
        )
        return context


class DocumentTypeListView(SingleObjectListView):
    model = DocumentType
    object_permission = permission_document_type_view
    view_icon = icon_document_type_list

    def get_extra_context(self):
        return {
            'hide_link': True,
            'hide_object': True,
            'no_results_icon': icon_document_type_setup,
            'no_results_main_link': link_document_type_create.resolve(
                context=RequestContext(request=self.request)
            ),
            'no_results_text': _(
                'Document types are the most basic units of configuration. '
                'Everything in the system will depend on them. '
                'Define a document type for each type of physical '
                'document you intend to upload. Example document types: '
                'invoice, receipt, manual, prescription, balance sheet.'
            ),
            'no_results_title': _(message='No document types available'),
            'title': _(message='Document types')
        }


class DocumentTypeCreateView(SingleObjectCreateView):
    fields = ('label',)
    model = DocumentType
    post_action_redirect = reverse_lazy(
        viewname='documents:document_type_list'
    )
    view_icon = icon_document_type_create
    view_permission = permission_document_type_create

    def get_extra_context(self):
        return {
            'title': _(message='Create document type')
        }

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class DocumentTypeDeleteView(SingleObjectDeleteView):
    model = DocumentType
    object_permission = permission_document_type_delete
    pk_url_kwarg = 'document_type_id'
    post_action_redirect = reverse_lazy(
        viewname='documents:document_type_list'
    )
    view_icon = icon_document_type_delete

    def get_extra_context(self):
        return {
            'message': _(message='All documents of this type will be deleted too.'),
            'object': self.object,
            'title': _(message='Delete the document type: %s?') % self.object
        }


class DocumentTypeEditView(SingleObjectEditView):
    fields = ('label',)
    model = DocumentType
    object_permission = permission_document_type_edit
    pk_url_kwarg = 'document_type_id'
    post_action_redirect = reverse_lazy(
        viewname='documents:document_type_list'
    )
    view_icon = icon_document_type_edit

    def get_extra_context(self):
        return {
            'object': self.object,
            'title': _(message='Edit document type: %s') % self.object
        }

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class DocumentTypeFilenameCreateView(
    ExternalObjectViewMixin, SingleObjectCreateView
):
    external_object_class = DocumentType
    external_object_permission = permission_document_type_edit
    external_object_pk_url_kwarg = 'document_type_id'
    form_class = DocumentTypeFilenameForm_create
    view_icon = icon_document_type_filename_create

    def get_extra_context(self):
        return {
            'document_type': self.external_object,
            'navigation_object_list': ('document_type',),
            'title': _(
                'Create quick label for document type: %s'
            ) % self.external_object
        }

    def get_instance_extra_data(self):
        return {'document_type': self.external_object}


class DocumentTypeFilenameDeleteView(SingleObjectDeleteView):
    model = DocumentTypeFilename
    object_permission = permission_document_type_edit
    pk_url_kwarg = 'document_type_filename_id'
    view_icon = icon_document_type_filename_delete

    def get_extra_context(self):
        return {
            'document_type': self.object.document_type,
            'filename': self.object,
            'navigation_object_list': ('document_type', 'filename',),
            'title': _(
                'Delete the quick label: %(label)s, from document type '
                '"%(document_type)s"?'
            ) % {
                'document_type': self.object.document_type,
                'label': self.object
            }
        }

    def get_post_action_redirect(self):
        return reverse(
            viewname='documents:document_type_filename_list', kwargs={
                'document_type_id': self.object.document_type.pk
            }
        )


class DocumentTypeFilenameEditView(SingleObjectEditView):
    fields = ('enabled', 'filename',)
    model = DocumentTypeFilename
    object_permission = permission_document_type_edit
    pk_url_kwarg = 'document_type_filename_id'
    view_icon = icon_document_type_filename_edit

    def get_extra_context(self):
        return {
            'document_type': self.object.document_type,
            'filename': self.object,
            'navigation_object_list': ('document_type', 'filename',),
            'title': _(
                'Edit quick label "%(filename)s" from document type '
                '"%(document_type)s"'
            ) % {
                'document_type': self.object.document_type,
                'filename': self.object
            }
        }

    def get_post_action_redirect(self):
        return reverse(
            viewname='documents:document_type_filename_list', kwargs={
                'document_type_id': self.object.document_type.pk
            }
        )


class DocumentTypeFilenameListView(
    ExternalObjectViewMixin, SingleObjectListView
):
    external_object_class = DocumentType
    external_object_permission = permission_document_type_view
    external_object_pk_url_kwarg = 'document_type_id'
    view_icon = icon_document_type_filename_list

    def get_extra_context(self):
        return {
            'document_type': self.external_object,
            'hide_link': True,
            'hide_object': True,
            'navigation_object_list': ('document_type',),
            'no_results_icon': icon_document_type_filename,
            'no_results_main_link': link_document_type_filename_create.resolve(
                context=RequestContext(
                    dict_={
                        'document_type': self.external_object
                    }, request=self.request
                )
            ),
            'no_results_text': _(
                'Quick labels are predetermined filenames that allow '
                'the quick renaming of documents as they are uploaded '
                'by selecting them from a list. Quick labels can also '
                'be used after the documents have been uploaded.'
            ),
            'no_results_title': _(
                'There are no quick labels for this document type'
            ),
            'title': _(
                'Quick labels for document type: %s'
            ) % self.external_object
        }

    def get_source_queryset(self):
        return self.external_object.filenames.all()


class DocumentTypeFilenameGeneratorEditView(SingleObjectEditView):
    form_class = DocumentTypeFilenameGeneratorForm
    model = DocumentType
    object_permission = permission_document_type_edit
    pk_url_kwarg = 'document_type_id'
    post_action_redirect = reverse_lazy(
        viewname='documents:document_type_list'
    )
    view_icon = icon_document_type_filename_generator

    def get_extra_context(self):
        return {
            'object': self.object,
            'title': _(
                'Filename generation setup for document type: %s'
            ) % self.object
        }

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }
