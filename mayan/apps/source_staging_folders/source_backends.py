from django.utils.translation import gettext_lazy as _

from mayan.apps.appearance.classes import Icon
from mayan.apps.source_compressed.source_backends.mixins import SourceBackendMixinCompressed
from mayan.apps.source_interactive.source_backends.mixins import SourceBackendMixinInteractive
from mayan.apps.source_stored_files.source_backends.filesystem_source_mixins import SourceBackendMixinStoredFileLocationFilesystem
from mayan.apps.source_stored_files.source_backends.stored_file_source_mixins import SourceBackendMixinStoredFileInteractive
from mayan.apps.sources.source_backends.base import SourceBackend
from mayan.apps.sources.source_backends.mixins import SourceBackendMixinRegularExpression


class SourceBackendStagingFolder(
    SourceBackendMixinCompressed,
    SourceBackendMixinStoredFileLocationFilesystem,
    SourceBackendMixinInteractive, SourceBackendMixinRegularExpression,
    SourceBackendMixinStoredFileInteractive, SourceBackend
):
    icon = Icon(driver_name='fontawesome', symbol='file')
    label = _(message='Staging folder')
