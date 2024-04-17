from django.utils.translation import gettext_lazy as _

from mayan.apps.navigation.classes import Link
from mayan.apps.navigation.utils import factory_condition_queryset_access

from .icons import (
    icon_announcement_create, icon_announcement_delete,
    icon_announcement_edit, icon_announcement_list, icon_set_line_size
)
from .permissions import (
    permission_announcement_create, permission_announcement_delete,
    permission_announcement_edit, permission_announcement_view
)

link_announcement_create = Link(
    icon=icon_announcement_create, permission=permission_announcement_create,
    text=_(message='Create announcement'),
    view='announcements:announcement_create'
)
link_announcement_multiple_delete = Link(
    icon=icon_announcement_delete, tags='dangerous',
    text=_(message='Delete'),
    view='announcements:announcement_multiple_delete'
)
link_announcement_single_delete = Link(
    args='object.pk', icon=icon_announcement_delete,
    permission=permission_announcement_delete,
    tags='dangerous', text=_(message='Delete'),
    view='announcements:announcement_single_delete'
)
link_announcement_edit = Link(
    args='object.pk', icon=icon_announcement_edit,
    permission=permission_announcement_edit, text=_(message='Edit'),
    view='announcements:announcement_edit'
)
link_announcement_list = Link(
    icon=icon_announcement_list, text=_(message='Announcements'),
    view='announcements:announcement_list'
)
link_announcement_setup = Link(
    condition=factory_condition_queryset_access(
        app_label='announcements', model_name='Announcement',
        object_permission=permission_announcement_view,
        view_permission=permission_announcement_create,
    ), icon=icon_announcement_list,
    text=_(message='Announcements'), view='announcements:announcement_list'
)
link_line_setup = Link(
    condition=factory_condition_queryset_access(
        app_label='announcements', model_name='Announcement',
        object_permission=permission_announcement_view,
        view_permission=permission_announcement_create,
    ), icon=icon_set_line_size,
    text=_('Summary Config'), view='create_config'
)