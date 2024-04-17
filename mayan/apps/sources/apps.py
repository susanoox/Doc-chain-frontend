from django.apps import apps
from django.db.models.signals import pre_delete
from django.utils.translation import gettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.acls.permissions import (
    permission_acl_edit, permission_acl_view
)
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.classes import MissingItem
from mayan.apps.common.menus import (
    menu_list_facet, menu_object, menu_return, menu_secondary, menu_setup
)
from mayan.apps.common.signals import signal_post_upgrade
from mayan.apps.converter.links import link_transformation_list
from mayan.apps.databases.classes import ModelProperty
from mayan.apps.documents.menus import menu_documents
from mayan.apps.documents.permissions import (
    permission_document_create, permission_document_file_new
)
from mayan.apps.events.classes import EventModelRegistry, ModelEventType
from mayan.apps.logging.classes import ErrorLog
from mayan.apps.navigation.classes import SourceColumn
from mayan.apps.rest_api.fields import DynamicSerializerField
from mayan.apps.views.column_widgets import TwoStateWidget

from .classes import DocumentCreateWizardStep
from .events import event_source_edited
from .handlers import (
    handler_delete_interval_source_periodic_task,
    handler_initialize_periodic_tasks
)
from .links import (
    link_document_file_source_metadata_list, link_document_file_upload,
    link_document_upload_wizard, link_source_backend_selection,
    link_source_delete, link_source_edit, link_source_list,
    link_source_setup, link_source_test
)
from .permissions import (
    permission_sources_delete, permission_sources_edit,
    permission_sources_metadata_view, permission_sources_view
)
from .property_helpers import (
    DocumentSourceMetadataHelper, DocumentFileSourceMetadataHelper
)
from .source_backends.base import SourceBackend


class SourcesApp(MayanAppConfig):
    app_namespace = 'sources'
    app_url = 'sources'
    has_rest_api = True
    has_static_media = False
    has_tests = True
    name = 'mayan.apps.sources'
    verbose_name = _(message='Sources')

    def ready(self):
        super().ready()

        DocumentCreateWizardStep.load_modules()

        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )
        DocumentFile = apps.get_model(
            app_label='documents', model_name='DocumentFile'
        )
        DocumentType = apps.get_model(
            app_label='documents', model_name='DocumentType'
        )
        DocumentFileSourceMetadata = self.get_model(
            model_name='DocumentFileSourceMetadata'
        )
        Source = self.get_model(model_name='Source')

        SourceBackend.load_modules()

        DynamicSerializerField.add_serializer(
            klass=Source,
            serializer_class='mayan.apps.sources.serializers.SourceSerializer'
        )

        Document.add_to_class(
            name='source_metadata_value_of',
            value=DocumentSourceMetadataHelper.constructor
        )

        DocumentFile.add_to_class(
            name='source_metadata_value_of',
            value=DocumentFileSourceMetadataHelper.constructor
        )

        error_log = ErrorLog(app_config=self)
        error_log.register_model(model=Source)

        EventModelRegistry.register(model=Source)

        ModelEventType.register(
            model=Source, event_types=(event_source_edited,)
        )

        MissingItem(
            label=_(message='Create a document source'),
            description=_(
                'Document sources are the way in which new documents are '
                'feed to Mayan EDMS, create at least a web form source to '
                'be able to upload documents from a browser.'
            ),
            condition=lambda: not Source.objects.exists(),
            view='sources:source_list'
        )

        ModelPermission.register(
            model=DocumentFile, permissions=(
                permission_sources_metadata_view,
            )
        )
        ModelPermission.register(
            model=Source, permissions=(
                permission_acl_edit, permission_acl_view,
                permission_document_create, permission_document_file_new,
                permission_sources_delete, permission_sources_edit,
                permission_sources_metadata_view, permission_sources_view
            )
        )

        ModelProperty(
            description=_(
                'Return the value of a specific source metadata for '
                'the document\'s latest file.'
            ), label=_(message='Source metadata value of'), model=Document,
            name='source_metadata_value_of.< key >'
        )

        ModelProperty(
            description=_(
                'Return the value of a specific source metadata.'
            ), label=_(message='Source metadata value of'), model=DocumentFile,
            name='source_metadata_value_of.< key >'
        )

        SourceColumn(
            attribute='key', is_identifier=True,
            source=DocumentFileSourceMetadata
        )
        SourceColumn(
            attribute='value', include_label=True,
            source=DocumentFileSourceMetadata
        )
        SourceColumn(
            attribute='label', is_identifier=True, is_sortable=True,
            source=Source
        )
        SourceColumn(
            attribute='get_backend_class_label', include_label=True,
            label=_(message='Type'), source=Source
        )
        SourceColumn(
            attribute='enabled', include_label=True, is_sortable=True,
            source=Source, widget=TwoStateWidget
        )

        menu_documents.bind_links(
            links=(link_document_upload_wizard,)
        )

        menu_list_facet.bind_links(
            links=(link_document_file_source_metadata_list,),
            sources=(DocumentFile,)
        )
        menu_list_facet.bind_links(
            links=(link_transformation_list,), sources=(Source,)
        )

        menu_object.bind_links(
            links=(link_source_delete, link_source_edit), sources=(Source,)
        )

        menu_object.bind_links(
            links=(link_source_test,), sources=(Source,)
        )
        menu_return.bind_links(
            links=(link_source_list,), sources=(
                Source, 'sources:source_backend_selection',
                'sources:source_create', 'sources:source_list'
            )
        )
        menu_secondary.bind_links(
            links=(link_source_backend_selection,), sources=(
                Source, 'sources:source_backend_selection',
                'sources:source_create', 'sources:source_list'
            )
        )
        menu_secondary.bind_links(
            links=(link_document_file_upload,),
            sources=(
                'documents:document_file_list',
                'sources:document_file_upload'
            )
        )
        menu_setup.bind_links(
            links=(link_source_setup,)
        )
        pre_delete.connect(
            dispatch_uid='sources_handler_delete_interval_source_periodic_task',
            receiver=handler_delete_interval_source_periodic_task,
            sender=DocumentType
        )
        signal_post_upgrade.connect(
            dispatch_uid='sources_handler_initialize_periodic_tasks',
            receiver=handler_initialize_periodic_tasks
        )
