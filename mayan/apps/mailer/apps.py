from django.apps import apps
from django.utils.translation import gettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.acls.permissions import (
    permission_acl_edit, permission_acl_view
)
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.classes import ModelCopy
from mayan.apps.common.menus import (
    menu_multi_item, menu_object, menu_return, menu_secondary, menu_setup
)
from mayan.apps.events.classes import EventModelRegistry, ModelEventType
from mayan.apps.logging.classes import ErrorLog
from mayan.apps.navigation.classes import SourceColumn
from mayan.apps.views.column_widgets import TwoStateWidget

from .classes import (
    MailerBackend, ModelMailingActionAttachment, ModelMailingActionLink
)
from .events import event_email_sent, event_mailing_profile_edited
from .links import (
    link_mailing_profile_create, link_mailing_profile_delete,
    link_mailing_profile_edit, link_mailing_profile_list,
    link_mailing_profile_setup, link_mailing_profile_test,
    link_send_document_file_attachment_multiple,
    link_send_document_file_attachment_single,
    link_send_document_file_link_multiple,
    link_send_document_file_link_single, link_send_document_link_multiple,
    link_send_document_link_single,
    link_send_document_version_attachment_multiple,
    link_send_document_version_attachment_single,
    link_send_document_version_link_multiple,
    link_send_document_version_link_single
)
from .literals import (
    DOCUMENT_FILE_CONTENT_FUNCTION_DOTTED_PATH,
    DOCUMENT_FILE_MIME_TYPE_FUNCTION_DOTTED_PATH,
    DOCUMENT_VERSION_CONTENT_FUNCTION_DOTTED_PATH,
    DOCUMENT_VERSION_MIME_TYPE_FUNCTION_DOTTED_PATH
)
from .permissions import (
    permission_send_document_file_attachment,
    permission_send_document_file_link, permission_send_document_link,
    permission_send_document_version_attachment,
    permission_send_document_version_link,
    permission_mailing_profile_delete, permission_mailing_profile_edit,
    permission_mailing_profile_use, permission_mailing_profile_view
)


class MailerApp(MayanAppConfig):
    app_namespace = 'mailer'
    app_url = 'mailer'
    has_rest_api = True
    has_tests = True
    name = 'mayan.apps.mailer'
    verbose_name = _(message='Mailer')

    def ready(self):
        super().ready()

        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )
        DocumentFile = apps.get_model(
            app_label='documents', model_name='DocumentFile'
        )
        DocumentVersion = apps.get_model(
            app_label='documents', model_name='DocumentVersion'
        )

        UserMailer = self.get_model(model_name='UserMailer')

        error_log = ErrorLog(app_config=self)
        error_log.register_model(model=UserMailer, register_permission=True)

        EventModelRegistry.register(model=UserMailer)

        MailerBackend.load_modules()

        ModelCopy(
            model=UserMailer, bind_link=True, register_permission=True
        ).add_fields(
            field_names=(
                'label', 'enabled', 'backend_path', 'backend_data'
            ), field_values={
                'default': False
            }
        )

        ModelEventType.register(
            model=UserMailer, event_types=(
                event_email_sent, event_mailing_profile_edited
            )
        )

        ModelMailingActionLink(
            manager_name='valid', model=Document,
            permission=permission_send_document_link
        )

        ModelMailingActionAttachment(
            content_function_dotted_path=DOCUMENT_FILE_CONTENT_FUNCTION_DOTTED_PATH,
            manager_name='valid',
            mime_type_function_dotted_path=DOCUMENT_FILE_MIME_TYPE_FUNCTION_DOTTED_PATH,
            model=DocumentFile,
            permission=permission_send_document_file_attachment
        )
        ModelMailingActionLink(
            manager_name='valid',
            model=DocumentFile,
            permission=permission_send_document_file_link
        )

        ModelMailingActionAttachment(
            content_function_dotted_path=DOCUMENT_VERSION_CONTENT_FUNCTION_DOTTED_PATH,
            manager_name='valid',
            mime_type_function_dotted_path=DOCUMENT_VERSION_MIME_TYPE_FUNCTION_DOTTED_PATH,
            model=DocumentVersion,
            permission=permission_send_document_version_attachment
        )
        ModelMailingActionLink(
            manager_name='valid',
            model=DocumentVersion,
            permission=permission_send_document_version_link
        )

        ModelPermission.register(
            model=UserMailer, permissions=(
                permission_acl_edit, permission_acl_view,
                permission_mailing_profile_delete,
                permission_mailing_profile_edit,
                permission_mailing_profile_use,
                permission_mailing_profile_view
            )
        )

        SourceColumn(
            attribute='label', is_identifier=True, is_sortable=True,
            source=UserMailer
        )
        SourceColumn(
            attribute='default', include_label=True, is_sortable=True,
            source=UserMailer, widget=TwoStateWidget
        )
        SourceColumn(
            attribute='enabled', include_label=True, is_sortable=True,
            source=UserMailer, widget=TwoStateWidget
        )
        SourceColumn(
            attribute='get_backend_class_label', include_label=True,
            source=UserMailer
        )

        # Document

        menu_multi_item.bind_links(
            links=(
                link_send_document_link_multiple,
            ), sources=(Document,)
        )

        menu_object.bind_links(
            links=(
                link_send_document_link_single,
            ), sources=(Document,)
        )

        # Document file

        menu_multi_item.bind_links(
            links=(
                link_send_document_file_attachment_multiple,
                link_send_document_file_link_multiple
            ), sources=(DocumentFile,)
        )

        menu_object.bind_links(
            links=(
                link_send_document_file_link_single,
                link_send_document_file_attachment_single
            ), sources=(DocumentFile,)
        )

        # Document version

        menu_multi_item.bind_links(
            links=(
                link_send_document_version_attachment_multiple,
                link_send_document_version_link_multiple
            ), sources=(DocumentVersion,)
        )

        menu_object.bind_links(
            links=(
                link_send_document_version_link_single,
                link_send_document_version_attachment_single
            ), sources=(DocumentVersion,)
        )

        # Mailing profile

        menu_object.bind_links(
            links=(
                link_mailing_profile_delete, link_mailing_profile_edit,
                link_mailing_profile_test
            ), sources=(UserMailer,)
        )

        menu_return.bind_links(
            links=(link_mailing_profile_list,), sources=(
                UserMailer, 'mailer:mailing_profile_list',
                'mailer:mailing_profile_create'
            )
        )

        menu_secondary.bind_links(
            links=(link_mailing_profile_create,), sources=(
                UserMailer, 'mailer:mailing_profile_list',
                'mailer:mailing_profile_create'
            )
        )

        menu_setup.bind_links(
            links=(link_mailing_profile_setup,)
        )
