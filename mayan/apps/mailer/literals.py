from django.utils.translation import gettext_lazy as _

DEFAULT_DOCUMENT_BODY_TEMPLATE = _(
    message='Attached to this email is the {{ object_name }}: {{ object }}\n\n '
    '--------\n '
    'This email has been sent from %(project_title)s (%(project_website)s)'
)
DEFAULT_DOCUMENT_SUBJECT_TEMPLATE = _(
    message='{{ object_name }}: {{ object }}'
)
DEFAULT_LINK_BODY_TEMPLATE = _(
    message='To access this {{ object_name }} click on the following link: '
    '{{ link }}\n\n--------\n '
    'This email has been sent from %(project_title)s (%(project_website)s)'
)
DEFAULT_LINK_SUBJECT_TEMPLATE = _(
    message='Link for {{ object_name }}: {{ object }}'
)
EMAIL_SEPARATORS = (',', ';')

DOCUMENT_FILE_CONTENT_FUNCTION_DOTTED_PATH = 'mayan.apps.mailer.utils.get_document_file_content'
DOCUMENT_FILE_MIME_TYPE_FUNCTION_DOTTED_PATH = 'mayan.apps.mailer.utils.get_document_file_mime_type'

DOCUMENT_VERSION_CONTENT_FUNCTION_DOTTED_PATH = 'mayan.apps.mailer.utils.get_document_version_content'
DOCUMENT_VERSION_MIME_TYPE_FUNCTION_DOTTED_PATH = 'mayan.apps.mailer.utils.get_document_version_mime_type'
