from django.utils.translation import gettext_lazy as _

from mayan.apps.navigation.classes import Link
from mayan.apps.user_management.link_conditions import condition_user_is_not_super_user
from mayan.apps.user_management.permissions import permission_user_edit

from .icons import icon_impersonate_start, icon_logout, icon_password_change
from .permissions import permission_users_impersonate


def _condition_user_has_usable_password_and_can_change_password(user):
    if user.is_authenticated:
        return user.has_usable_password() and not user.user_options.block_password_change
    else:
        return False


def condition_user_has_usable_password_and_can_change_password(context, resolved_object):
    user = context['request'].user

    return _condition_user_has_usable_password_and_can_change_password(
        user=user
    )


def condition_user_has_usable_password_and_can_change_password_and_is_not_admin(context, resolved_object):
    return _condition_user_has_usable_password_and_can_change_password(
        user=resolved_object
    ) and condition_user_is_not_super_user(
        context=context, resolved_object=resolved_object
    )


link_logout = Link(
    html_extra_classes='non-ajax', icon=icon_logout, text=_(message='Logout'),
    view='authentication:logout_view'
)
link_password_change = Link(
    condition=condition_user_has_usable_password_and_can_change_password,
    icon=icon_password_change, text=_(message='Change password'),
    view='authentication:password_change_view'
)
link_user_impersonate_form_start = Link(
    icon=icon_impersonate_start,
    permission=permission_users_impersonate, text=_(message='Impersonate user'),
    view='authentication:user_impersonate_form_start'
)
link_user_impersonate_start = Link(
    args='object.id', condition=condition_user_is_not_super_user, icon=icon_impersonate_start,
    permission=permission_users_impersonate, text=_(message='Impersonate'),
    view='authentication:user_impersonate_start'
)
link_user_multiple_set_password = Link(
    icon=icon_password_change, permission=permission_user_edit,
    text=_(message='Set password'), view='authentication:user_multiple_set_password'
)
link_user_set_password = Link(
    args='object.id', condition=condition_user_has_usable_password_and_can_change_password_and_is_not_admin,
    icon=icon_password_change, permission=permission_user_edit,
    text=_(message='Set password'), view='authentication:user_set_password'
)
