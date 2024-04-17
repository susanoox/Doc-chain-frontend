import logging

import sh

from django.core.files import File
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from mayan.apps.common.serialization import yaml_load
from mayan.apps.source_generated_files.source_backend_actions.generated_file_actions import (
    SourceBackendActionGenerateFileDocumentFileUpload,
    SourceBackendActionGenerateFileDocumentUpload
)
from mayan.apps.source_interactive.source_backends.mixins import SourceBackendMixinInteractive
from mayan.apps.sources.settings import setting_backend_arguments
from mayan.apps.sources.source_backends.base import SourceBackend
from mayan.apps.storage.utils import NamedTemporaryFile, touch

from .literals import DEFAULT_BINARY_SCANIMAGE_PATH

logger = logging.getLogger(name=__name__)


class SourceBackendSANEScanner(SourceBackendMixinInteractive, SourceBackend):
    action_class_list = (
        SourceBackendActionGenerateFileDocumentFileUpload,
        SourceBackendActionGenerateFileDocumentUpload
    )
    label = _(message='SANE Scanner')
    widgets = {
        'arguments': {
            'class': 'django.forms.widgets.Textarea', 'kwargs': {
                'attrs': {
                    'rows': 10
                }
            }
        }
    }

    @classmethod
    def get_form_fields(cls):
        fields = super().get_form_fields()
        fields.update(
            {
                'device_name': {
                    'class': 'django.forms.CharField',
                    'help_text': _(
                        'Device name as returned by the SANE backend.'
                    ),
                    'kwargs': {'max_length': 255},
                    'label': _(message='Device name'),
                    'required': True
                },
                'arguments': {
                    'class': 'django.forms.CharField',
                    'help_text': _(
                        'YAML formatted arguments to pass to the `scanimage` '
                        'command. The arguments will change depending on the '
                        'device. Execute `scanimage --help --device-name=DEVICE` '
                        'for the list of supported arguments.'
                    ),
                    'label': _(message='Arguments'),
                    'required': False
                }
            }
        )

        return fields

    @classmethod
    def get_form_fieldsets(cls):
        fieldsets = super().get_form_fieldsets()

        fieldsets += (
            (
                _(message='SANE client'), {
                    'fields': ('device_name', 'arguments')
                },
            ),
        )

        return fieldsets

    def action_file_get(self, file_identifier):
        with NamedTemporaryFile() as file_object:
            # The output_file argument is only supported in version 1.0.28
            # https://gitlab.com/sane-project/backends/-/releases/1.0.28
            # Using redirection make this compatible with more versions.
            try:
                self.call_command_scanimage(_out=file_object.name)
            except sh.ErrorReturnCode:
                # The shell command is deleting the temporary file on errors.
                # Recreate it so that `NamedTemporaryFile` is able to delete
                # it when the context exits.
                touch(filename=file_object.name)
                raise
            else:
                file_object.seek(0)

                filename = 'scan {}'.format(
                    now()
                )
                yield {
                    'file': File(file=file_object, name=filename)
                }

    def call_command_scanimage(self, **kwargs):
        command_path = setting_backend_arguments.value.get(
            'mayan.apps.sources.source_backends.SourceBackendSANEScanner', {}
        ).get('scanimage_path', DEFAULT_BINARY_SCANIMAGE_PATH)

        command_scanimage = sh.Command(path=command_path)

        command_scanimage = command_scanimage.bake(
            device_name=self.kwargs['device_name'],
            format='tiff'
        )

        loaded_arguments = yaml_load(
            stream=self.kwargs.get('arguments', '{}')
        ) or {}

        loaded_arguments.update(**kwargs)

        command_scanimage(**loaded_arguments)

    def get_view_context(self, context, request):
        return {
            'subtemplates_list': [
                {
                    'context': {
                        'forms': context['forms'],
                        'is_multipart': True,
                        'title': _(message='Document properties'),
                        'submit_label': _(message='Scan')
                    },
                    'name': 'appearance/partials/form/multiple.html'
                }
            ]
        }
