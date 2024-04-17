from django.utils.translation import gettext_lazy as _

from mayan.apps.smart_settings.settings import setting_cluster

from .literals import (
    DEFAULT_VIEWS_PAGINATE_BY, DEFAULT_VIEWS_PAGING_ARGUMENT,
    DEFAULT_VIEWS_SHOW_DROPZONE_SUBMIT_BUTTON
)

setting_namespace = setting_cluster.do_namespace_add(
    label=_(message='Views'), name='views'
)

setting_paginate_by = setting_namespace.do_setting_add(
    default=DEFAULT_VIEWS_PAGINATE_BY, global_name='VIEWS_PAGINATE_BY',
    help_text=_(
        'The number objects that will be displayed per page.'
    )
)
setting_paging_argument = setting_namespace.do_setting_add(
    default=DEFAULT_VIEWS_PAGING_ARGUMENT,
    global_name='VIEWS_PAGING_ARGUMENT', help_text=_(
        'A string specifying the name to use for the paging parameter.'
    )
)
setting_show_dropzone_submit_button = setting_namespace.do_setting_add(
    default=DEFAULT_VIEWS_SHOW_DROPZONE_SUBMIT_BUTTON,
    global_name='VIEWS_SHOW_DROPZONE_SUBMIT_BUTTON', help_text=_(
        'Display a submit button and wait for the submit button to be '
        'pressed before processing up the upload.'
    )
)
